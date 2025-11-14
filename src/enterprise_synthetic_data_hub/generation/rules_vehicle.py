"""Placeholder rule definitions for Vehicle generation."""
from __future__ import annotations

from typing import List

from enterprise_synthetic_data_hub.models.vehicle import Vehicle


def build_vehicle_rules() -> List[str]:
    """Describe high-level rules used to generate Vehicle records."""

    return [
        "Each Person must have at least one associated Vehicle.",
        "VINs must be 17 characters and exclude I/O/Q.",
        "model_year should fall between 2000 and the upcoming calendar year.",
        "lob_type should align with the owning Person's lob_type.",
    ]


def generate_vehicle_placeholder(person_id: str) -> Vehicle:
    """Return a static Vehicle object linked to the provided person_id."""

    return Vehicle(
        vehicle_id="00000000-0000-0000-0000-000000000101",
        person_id=person_id,
        vin="1HGBH41JXMN000001",
        make="Placeholder",
        model="Sedan",
        model_year=2020,
        garaging_postal_code="94105",
        lob_type="Personal",
    )
