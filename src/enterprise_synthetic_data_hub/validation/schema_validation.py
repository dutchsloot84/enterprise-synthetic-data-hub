"""Validation helpers for synthetic data structures."""
from __future__ import annotations

from typing import Iterable, Tuple

from enterprise_synthetic_data_hub.models.person import Person
from enterprise_synthetic_data_hub.models.vehicle import Vehicle


def validate_person_records(persons: Iterable[Person]) -> Tuple[bool, list[str]]:
    """Run lightweight structural checks on Person records."""

    errors: list[str] = []
    for index, person in enumerate(persons):
        if not person.person_id:
            errors.append(f"Person[{index}] is missing person_id")
        if len(person.driver_license_state) != 2:
            errors.append(f"Person[{index}] driver_license_state must be 2 characters")
        if person.country != "US":
            errors.append(f"Person[{index}] country must be 'US' in POC scope")
    return (len(errors) == 0, errors)


def validate_vehicle_records(vehicles: Iterable[Vehicle]) -> Tuple[bool, list[str]]:
    """Run lightweight structural checks on Vehicle records."""

    errors: list[str] = []
    for index, vehicle in enumerate(vehicles):
        if not vehicle.vehicle_id:
            errors.append(f"Vehicle[{index}] is missing vehicle_id")
        if len(vehicle.vin) != 17:
            errors.append(f"Vehicle[{index}] vin must be 17 characters")
        if not (1980 <= vehicle.model_year <= 2100):
            errors.append(f"Vehicle[{index}] model_year is out of range (1980-2100)")
    return (len(errors) == 0, errors)
