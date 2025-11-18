"""Snapshot generation orchestrator for the synthetic data hub."""
from __future__ import annotations

import json
import random
import uuid
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List

from enterprise_synthetic_data_hub.config.settings import settings
from enterprise_synthetic_data_hub.generation import rules_person, rules_vehicle
from enterprise_synthetic_data_hub.generation.profiles import build_profiles
from enterprise_synthetic_data_hub.models.dataset_metadata import DatasetMetadata

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_OUTPUT_DIR = REPO_ROOT / "data" / "output"

FIRST_NAMES = ["Alex", "Jordan", "Taylor", "Casey", "Morgan", "Avery", "Logan"]
LAST_NAMES = ["Rivera", "Nguyen", "Patel", "Garcia", "Smith", "Zhou", "Thompson"]
STATE_CITY_POSTAL = {
    "CA": {"cities": ["Walnut Creek", "San Mateo"], "postal_range": (94596, 94950)},
    "AZ": {"cities": ["Phoenix", "Tempe"], "postal_range": (85001, 85299)},
    "NV": {"cities": ["Las Vegas", "Henderson"], "postal_range": (88901, 89199)},
    "OR": {"cities": ["Portland", "Eugene"], "postal_range": (97001, 97599)},
    "WA": {"cities": ["Seattle", "Tacoma"], "postal_range": (98001, 98599)},
}
STATES = list(STATE_CITY_POSTAL.keys())
LOB_DISTRIBUTION = {"Personal": 0.7, "Commercial": 0.3}
MAKES = ["Toyota", "Ford", "Honda", "Subaru", "Chevrolet"]
MODELS = {
    "Toyota": ["Camry", "Prius", "RAV4"],
    "Ford": ["Focus", "Escape", "Maverick"],
    "Honda": ["Civic", "CR-V", "Accord"],
    "Subaru": ["Outback", "Forester"],
    "Chevrolet": ["Equinox", "Malibu", "Trax"],
}
BODY_STYLES_BY_LOB: Dict[str, List[str]] = {
    "Personal": ["Sedan", "SUV"],
    "Commercial": ["SUV", "Truck"],
}
RISK_RATINGS_BY_LOB: Dict[str, List[str]] = {
    "Personal": ["Low", "Medium"],
    "Commercial": ["Medium", "High"],
}
VIN_CHARACTERS = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"
APARTMENT_SUFFIXES = ["Apt", "Suite", "Unit"]


@dataclass
class SnapshotBundle:
    """Container returned by the generator when implemented."""

    metadata: DatasetMetadata
    persons: List[dict]
    vehicles: List[dict]
    profiles: List[dict]


def describe_generation_plan() -> List[str]:
    """Summarize the high-level generation plan for documentation/testing."""

    plan = [
        f"Dataset version: {settings.dataset_version}",
        f"Target person records: {settings.target_person_records}",
        "Use deterministic seed for reproducibility.",
        "Generate Persons first, then attach Vehicles per rules (one-to-one).",
        "Persist JSON payload + metadata file under data/output/.",
        "Expose legacy shim via src/generator for compatibility.",
    ]
    plan.extend(rules_person.build_person_rules())
    plan.extend(rules_vehicle.build_vehicle_rules())
    return plan


def _generate_uuid(rng: random.Random) -> str:
    return str(uuid.UUID(int=rng.getrandbits(128)))


def _random_choice(rng: random.Random, values: List[str]) -> str:
    return values[rng.randrange(len(values))]


def _select_weighted_choice(rng: random.Random, distribution: Dict[str, float]) -> str:
    roll = rng.random()
    cumulative = 0.0
    for key, weight in distribution.items():
        cumulative += weight
        if roll <= cumulative:
            return key
    # Fallback in case of floating point rounding errors
    return next(iter(distribution.keys()))


def _generate_postal_code(rng: random.Random, state: str) -> str:
    postal_range = STATE_CITY_POSTAL[state]["postal_range"]
    postal_code = rng.randint(postal_range[0], postal_range[1])
    return f"{postal_code:05d}"


def _build_address_line_2(index: int) -> str | None:
    if index % 3 != 0:
        return None
    suffix = APARTMENT_SUFFIXES[index % len(APARTMENT_SUFFIXES)]
    return f"{suffix} {200 + index}"


def _generate_driver_license_number(rng: random.Random, state: str) -> str:
    return f"{state}{rng.randint(1000000, 9999999)}"


def _generate_person(rng: random.Random, index: int) -> dict:
    state = _random_choice(rng, STATES)
    dob = date(1970, 1, 1) + timedelta(days=rng.randint(0, 20000))
    city = _random_choice(rng, STATE_CITY_POSTAL[state]["cities"])
    postal_code = _generate_postal_code(rng, state)
    lob_type = _select_weighted_choice(rng, LOB_DISTRIBUTION)
    return {
        "person_id": _generate_uuid(rng),
        "first_name": _random_choice(rng, FIRST_NAMES),
        "last_name": _random_choice(rng, LAST_NAMES),
        "date_of_birth": dob.isoformat(),
        "driver_license_number": _generate_driver_license_number(rng, state),
        "driver_license_state": state,
        "address_line_1": f"{100 + index} Main Street",
        "address_line_2": _build_address_line_2(index),
        "city": city,
        "state": state,
        "postal_code": postal_code,
        "country": "US",
        "lob_type": lob_type,
        "synthetic_source": SYNTHETIC_MARKER,
    }


def _generate_vehicle_vin(rng: random.Random) -> str:
    return "".join(rng.choice(VIN_CHARACTERS) for _ in range(17))


def _generate_vehicle(rng: random.Random, person: dict) -> dict:
    make = _random_choice(rng, MAKES)
    model = _random_choice(rng, MODELS[make])
    model_year = rng.randint(2008, 2024)
    lob_type = person["lob_type"]
    body_styles = BODY_STYLES_BY_LOB[lob_type]
    risk_ratings = RISK_RATINGS_BY_LOB[lob_type]
    return {
        "vehicle_id": _generate_uuid(rng),
        "person_id": person["person_id"],
        "vin": _generate_vehicle_vin(rng),
        "make": make,
        "model": model,
        "model_year": model_year,
        "body_style": _random_choice(rng, body_styles),
        "risk_rating": _random_choice(rng, risk_ratings),
        "lob_type": lob_type,
        "garaging_state": person["state"],
        "garaging_postal_code": person["postal_code"],
        "synthetic_source": SYNTHETIC_MARKER,
    }


def generate_snapshot_bundle(
    num_records: int | None = None,
    seed: int | None = None,
    include_profiles: bool = True,
) -> SnapshotBundle:
    """Generate deterministic snapshot bundle used across the pipeline."""

    record_target = settings.target_person_records if num_records is None else num_records
    if record_target <= 0:
        raise ValueError("num_records must be positive")

    rng = random.Random(settings.random_seed if seed is None else seed)
    persons: List[dict] = []
    vehicles: List[dict] = []
    for index in range(record_target):
        person = _generate_person(rng, index)
        persons.append(person)
        vehicle = _generate_vehicle(rng, person)
        vehicles.append(vehicle)

    profiles = (
        build_profiles(persons, vehicles, synthetic_source=SYNTHETIC_MARKER)
        if include_profiles
        else []
    )

    metadata = DatasetMetadata(
        dataset_version=settings.dataset_version,
        generated_at=settings.generation_timestamp,
        record_count_persons=len(persons),
        record_count_vehicles=len(vehicles),
        record_count_profiles=len(profiles),
        notes=(
            "Deterministic snapshot generated from rule-based distributions "
            f"(seed={seed or settings.random_seed})."
        ),
    )
    return SnapshotBundle(
        metadata=metadata,
        persons=persons,
        vehicles=vehicles,
        profiles=profiles,
    )


def write_snapshot_bundle(bundle: SnapshotBundle, output_dir: Path | None = None) -> Path:
    """Persist the snapshot bundle to disk for downstream consumers."""

    output_dir = output_dir or DATA_OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    metadata_payload = bundle.metadata.model_dump(mode="json")
    payload = {
        "metadata": metadata_payload,
        "persons": bundle.persons,
        "vehicles": bundle.vehicles,
        "profiles": bundle.profiles,
    }
    version_slug = bundle.metadata.dataset_version.replace(".", "_")
    snapshot_name = f"dataset_{version_slug}.json"
    metadata_name = f"metadata_{version_slug}.json"
    snapshot_path = output_dir / snapshot_name
    metadata_path = output_dir / metadata_name
    snapshot_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    metadata_path.write_text(json.dumps(metadata_payload, indent=2), encoding="utf-8")
    return snapshot_path


__all__ = [
    "SnapshotBundle",
    "describe_generation_plan",
    "generate_snapshot_bundle",
    "write_snapshot_bundle",
]
SYNTHETIC_MARKER = settings.synthetic_marker

