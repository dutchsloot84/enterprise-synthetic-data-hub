"""Placeholder rule definitions for Vehicle generation."""
from __future__ import annotations

from typing import List

from enterprise_synthetic_data_hub.config.settings import settings
from enterprise_synthetic_data_hub.models.vehicle import Vehicle


def build_vehicle_rules() -> List[str]:
    """Describe high-level rules used to generate Vehicle records."""

    return [
        "Each Person receives one vehicle in v0.1 to guarantee referential integrity.",
        "VINs are composed of governed characters (17 chars, excluding I/O/Q).",
        "Model years range from 2008 through 2024 to reflect late-model fleets.",
        "Body style + risk rating distributions change with the owning Person's lob_type.",
        "Garaging state/postal code mirror the owning Person's address to keep datasets coherent.",
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
        body_style="Sedan",
        risk_rating="Low",
        garaging_postal_code="94105",
        lob_type="Personal",
        garaging_state="CA",
        synthetic_source=settings.synthetic_marker,
    )
