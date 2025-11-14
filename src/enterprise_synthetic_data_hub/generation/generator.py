"""Snapshot generation orchestrator (stub)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

from enterprise_synthetic_data_hub.config.settings import settings
from enterprise_synthetic_data_hub.generation import rules_person, rules_vehicle
from enterprise_synthetic_data_hub.models.dataset_metadata import DatasetMetadata
from enterprise_synthetic_data_hub.models.person import Person
from enterprise_synthetic_data_hub.models.vehicle import Vehicle


@dataclass
class SnapshotBundle:
    """Container returned by the generator when implemented."""

    metadata: DatasetMetadata
    persons: List[Person]
    vehicles: List[Vehicle]


def describe_generation_plan() -> List[str]:
    """Summarize the high-level generation plan for documentation/testing."""

    plan = [
        f"Dataset version: {settings.dataset_version}",
        f"Target person records: {settings.target_person_records}",
        "Use deterministic seed for reproducibility.",
        "Generate Persons first, then attach Vehicles per rules.",
        "Persist snapshots under data/snapshots/<version>/",
    ]
    plan.extend(rules_person.build_person_rules())
    plan.extend(rules_vehicle.build_vehicle_rules())
    return plan


def generate_snapshot_stub() -> SnapshotBundle:
    """Return placeholder snapshot bundle until real generator is implemented."""

    # TODO: Replace with actual deterministic rule-based generation in future iteration.
    person = rules_person.generate_person_placeholder()
    vehicle = rules_vehicle.generate_vehicle_placeholder(person.person_id)
    metadata = DatasetMetadata(
        dataset_version=settings.dataset_version,
        generated_at=settings.generation_timestamp,
        record_count_persons=1,
        record_count_vehicles=1,
        notes="Placeholder snapshot only."
    )
    return SnapshotBundle(metadata=metadata, persons=[person], vehicles=[vehicle])
