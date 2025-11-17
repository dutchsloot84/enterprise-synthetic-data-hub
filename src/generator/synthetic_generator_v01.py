"""Deterministic synthetic data generator for version v0.1."""
from __future__ import annotations

import json
import random
import uuid
from dataclasses import dataclass, asdict
from datetime import date, timedelta
from pathlib import Path
from typing import Iterable, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_OUTPUT_DIR = REPO_ROOT / "data" / "output"
SCHEMA_VERSION = "v0.1"

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
class PersonRecord:
    person_id: str
    first_name: str
    last_name: str
    date_of_birth: str
    driver_license_number: str
    driver_license_state: str
    address_line_1: str
    city: str
    state: str
    postal_code: str
    country: str
    lob_type: str


@dataclass
class VehicleRecord:
    vehicle_id: str
    person_id: str
    vin: str
    make: str
    model: str
    model_year: int
    body_style: str
    risk_rating: str
    lob_type: str
    garaging_state: str


def _generate_uuid(rng: random.Random) -> str:
    return str(uuid.UUID(int=rng.getrandbits(128)))


def _random_choice(rng: random.Random, values: Iterable[str]) -> str:
    values_list = list(values)
    return values_list[rng.randrange(len(values_list))]


def _generate_person(rng: random.Random, index: int) -> PersonRecord:
    state = _random_choice(rng, STATES)
    dob = date(1975, 1, 1) + timedelta(days=rng.randint(0, 18000))
    return PersonRecord(
        person_id=_generate_uuid(rng),
        first_name=_random_choice(rng, FIRST_NAMES),
        last_name=_random_choice(rng, LAST_NAMES),
        date_of_birth=dob.isoformat(),
        driver_license_number=f"{state}{rng.randint(100000, 999999)}",
        driver_license_state=state,
        address_line_1=f"{100 + index} Main Street",
        city="Walnut Creek",
        state=state,
        postal_code=f"{rng.randint(90000, 96999)}",
        country="US",
        lob_type=_random_choice(rng, LOB_TYPES),
    )


def _generate_vehicle(rng: random.Random, person_id: str) -> VehicleRecord:
    make = _random_choice(rng, MAKES)
    model = _random_choice(rng, MODELS[make])
    model_year = rng.randint(2015, 2024)
    return VehicleRecord(
        vehicle_id=_generate_uuid(rng),
        person_id=person_id,
        vin="".join(rng.choice("ABCDEFGHJKLMNPRSTUVWXYZ0123456789") for _ in range(17)),
        make=make,
        model=model,
        model_year=model_year,
        body_style=_random_choice(rng, BODY_STYLES),
        risk_rating=_random_choice(rng, RISK_RATINGS),
        lob_type=_random_choice(rng, LOB_TYPES),
        garaging_state=_random_choice(rng, STATES),
    )


def generate_person_vehicle_dataset(
    num_records: int = 10, seed: int | None = 42
) -> Tuple[List[dict], List[dict]]:
    """Return deterministic lists of person + vehicle records."""
    if num_records <= 0:
        raise ValueError("num_records must be positive")
    rng = random.Random(seed)
    persons: List[dict] = []
    vehicles: List[dict] = []
    for idx in range(num_records):
        person = _generate_person(rng, idx)
        persons.append(asdict(person))
        vehicle = _generate_vehicle(rng, person.person_id)
        vehicles.append(asdict(vehicle))
    return persons, vehicles


def write_dataset_snapshot(
    persons: List[dict],
    vehicles: List[dict],
    output_dir: Path | None = None,
) -> Path:
    """Persist dataset metadata for downstream validation."""
    output_dir = output_dir or DATA_OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": SCHEMA_VERSION,
        "person_count": len(persons),
        "vehicle_count": len(vehicles),
        "persons": persons,
        "vehicles": vehicles,
    }
    snapshot_path = output_dir / f"dataset_{SCHEMA_VERSION.replace('.', '_')}.json"
    with snapshot_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
    return snapshot_path


def main() -> None:  # pragma: no cover
    persons, vehicles = generate_person_vehicle_dataset()
    path = write_dataset_snapshot(persons, vehicles)
    print(f"Snapshot written to {path}")


if __name__ == "__main__":  # pragma: no cover
    main()
