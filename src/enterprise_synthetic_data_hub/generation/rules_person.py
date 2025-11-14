"""Placeholder rule definitions for Person generation."""
from __future__ import annotations

from typing import List

from enterprise_synthetic_data_hub.models.person import Person


def build_person_rules() -> List[str]:
    """Describe high-level rules used to generate Person records.

    Returns a list of rule descriptions for documentation/testing purposes.
    Implementation of the generator will consume these descriptions later.
    """

    return [
        "Use deterministic random seed for reproducibility.",
        "Assign UUIDv4-based person_id values.",
        "Ensure driver_license_number matches synthetic formats (e.g., 'X000-0000-0000').",
        "Derive lob_type values from a curated distribution (Personal vs Commercial).",
    ]


def generate_person_placeholder() -> Person:
    """Return a static Person object as a placeholder example."""

    return Person(
        person_id="00000000-0000-0000-0000-000000000001",
        first_name="Placeholder",
        last_name="Person",
        date_of_birth="1990-01-01",
        driver_license_number="D000-0000-0000",
        driver_license_state="CA",
        address_line_1="100 Placeholder Way",
        city="San Francisco",
        state="CA",
        postal_code="94105",
        country="US",
        lob_type="Personal",
    )
