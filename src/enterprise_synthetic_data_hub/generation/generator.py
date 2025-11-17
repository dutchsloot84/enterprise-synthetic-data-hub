"""Snapshot generation orchestrator for the synthetic data hub."""
from __future__ import annotations

import json
import random
import uuid
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import List

from enterprise_synthetic_data_hub.config.settings import settings
from enterprise_synthetic_data_hub.generation import rules_person, rules_vehicle
from enterprise_synthetic_data_hub.models.dataset_metadata import DatasetMetadata

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_OUTPUT_DIR = REPO_ROOT / "data" / "output"

FIRST_NAMES = ["Alex", "Jordan", "Taylor", "Casey", "Morgan"]
LAST_NAMES = ["Rivera", "Nguyen", "Patel", "Garcia", "Smith"]
STATES = ["CA", "AZ", "NV", "OR", "WA"]
LOB_TYPES = ["Personal", "Commercial"]
MAKES = ["Toyota", "Ford", "Honda", "Subaru", "Chevrolet"]
MODELS = {
    "Toyota": ["Camry", "Prius"],
    "Ford": ["Focus", "Escape"],
    "Honda": ["Civic", "CR-V"],
    "Subaru": ["Outback", "Forester"],
    "Chevrolet": ["Equinox", "Malibu"],
}
BODY_STYLES = ["Sedan", "SUV", "Truck"]
RISK_RATINGS = ["Low", "Medium", "High"]


@dataclass
class SnapshotBundle:
    """Container returned by the generator when implemented."""

    metadata: DatasetMetadata
    persons: List[dict]
    vehicles: List[dict]


def describe_generation_plan() -> List[str]:
    """Summarize the high-level generation plan for documentation/testing."""

    plan = [
        f"Dataset version: {settings.dataset_version}",
        f"Target person records: {settings.target_person_records}",
        "Use deterministic seed for reproducibility.",
        "Generate Persons first, then attach Vehicles per rules.",
        "Persist snapshots under data/snapshots/<version>/.",
        "Expose legacy shim via src/generator for compatibility.",
    ]
    plan.extend(rules_person.build_person_rules())
    plan.extend(rules_vehicle.build_vehicle_rules())
    return plan


def _generate_uuid(rng: random.Random) -> str:
    return str(uuid.UUID(int=rng.getrandbits(128)))


def _random_choice(rng: random.Random, values: List[str]) -> str:
    return values[rng.randrange(len(values))]


def _generate_person(rng: random.Random, index: int) -> dict:
    state = _random_choice(rng, STATES)
    dob = date(1975, 1, 1) + timedelta(days=rng.randint(0, 18000))
    return {
        "person_id": _generate_uuid(rng),
        "first_name": _random_choice(rng, FIRST_NAMES),
        "last_name": _random_choice(rng, LAST_NAMES),
        "date_of_birth": dob.isoformat(),
        "driver_license_number": f"{state}{rng.randint(100000, 999999)}",
        "driver_license_state": state,
        "address_line_1": f"{100 + index} Main Street",
        "city": "Walnut Creek",
        "state": state,
        "postal_code": f"{rng.randint(90000, 96999)}",
        "country": "US",
        "lob_type": _random_choice(rng, LOB_TYPES),
    }


def _generate_vehicle(rng: random.Random, person_id: str) -> dict:
    make = _random_choice(rng, MAKES)
    model = _random_choice(rng, MODELS[make])
    model_year = rng.randint(2015, 2024)
    return {
        "vehicle_id": _generate_uuid(rng),
        "person_id": person_id,
        "vin": "".join(rng.choice("ABCDEFGHJKLMNPRSTUVWXYZ0123456789") for _ in range(17)),
        "make": make,
        "model": model,
        "model_year": model_year,
        "body_style": _random_choice(rng, BODY_STYLES),
        "risk_rating": _random_choice(rng, RISK_RATINGS),
        "lob_type": _random_choice(rng, LOB_TYPES),
        "garaging_state": _random_choice(rng, STATES),
    }


def generate_snapshot_bundle(
    num_records: int | None = None,
    seed: int | None = None,
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
        vehicle = _generate_vehicle(rng, person["person_id"])
        vehicles.append(vehicle)

    metadata = DatasetMetadata(
        dataset_version=settings.dataset_version,
        generated_at=settings.generation_timestamp,
        record_count_persons=len(persons),
        record_count_vehicles=len(vehicles),
        notes="Deterministic placeholder snapshot for pipeline scaffolding.",
    )
    return SnapshotBundle(metadata=metadata, persons=persons, vehicles=vehicles)


def write_snapshot_bundle(bundle: SnapshotBundle, output_dir: Path | None = None) -> Path:
    """Persist the snapshot bundle to disk for downstream consumers."""

    output_dir = output_dir or DATA_OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "metadata": bundle.metadata.model_dump(mode="json"),
        "persons": bundle.persons,
        "vehicles": bundle.vehicles,
    }
    snapshot_name = f"dataset_{bundle.metadata.dataset_version.replace('.', '_')}.json"
    snapshot_path = output_dir / snapshot_name
    snapshot_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return snapshot_path


__all__ = [
    "SnapshotBundle",
    "describe_generation_plan",
    "generate_snapshot_bundle",
    "write_snapshot_bundle",
]
