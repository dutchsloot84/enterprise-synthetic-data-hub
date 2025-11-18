#!/usr/bin/env python
"""Lightweight validation harness for demo snapshots."""
from __future__ import annotations

import argparse
from typing import Iterable, Sequence

from enterprise_synthetic_data_hub.config import demo_profiles
from enterprise_synthetic_data_hub.config.settings import settings
from enterprise_synthetic_data_hub.generation.generator import generate_snapshot_bundle
from enterprise_synthetic_data_hub.models.person import Person
from enterprise_synthetic_data_hub.models.profile import Profile
from enterprise_synthetic_data_hub.models.vehicle import Vehicle
from enterprise_synthetic_data_hub.validation import schema_validation


def _check_marker(records: Sequence[object], entity: str) -> list[str]:
    missing = []
    for index, record in enumerate(records):
        if getattr(record, "synthetic_source", None) != settings.synthetic_marker:
            missing.append(f"{entity}[{index}] missing synthetic marker")
    return missing


def _summarize(label: str, success: bool, errors: Iterable[str]) -> None:
    status = "PASS" if success else "FAIL"
    print(f"[{status}] {label}")
    for err in errors:
        print(f"  - {err}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate demo snapshot outputs")
    parser.add_argument("--profile", default=None, help="Demo profile name (default: baseline)")
    args = parser.parse_args()

    profile = demo_profiles.get_demo_profile(args.profile)
    seed = profile.seed
    bundle = generate_snapshot_bundle(num_records=profile.records_person, seed=seed)

    persons = [Person(**record) for record in bundle.persons]
    vehicles = [Vehicle(**record) for record in bundle.vehicles]
    profiles = [Profile(**record) for record in bundle.profiles]

    ok_persons, person_errors = schema_validation.validate_person_records(persons)
    ok_vehicles, vehicle_errors = schema_validation.validate_vehicle_records(vehicles)
    marker_errors = _check_marker(persons, "Person")
    marker_errors += _check_marker(vehicles, "Vehicle")
    marker_errors += _check_marker(profiles, "Profile")

    _summarize("Person schema checks", ok_persons, person_errors)
    _summarize("Vehicle schema checks", ok_vehicles, vehicle_errors)
    _summarize("Synthetic marker checks", not marker_errors, marker_errors)

    if ok_persons and ok_vehicles and not marker_errors:
        print("Demo validation completed successfully.")
        return 0
    print("Demo validation failed. See errors above.")
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
