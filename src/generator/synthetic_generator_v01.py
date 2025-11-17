"""Legacy shim that delegates to the package-level generator."""
from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

from enterprise_synthetic_data_hub.config.settings import settings
from enterprise_synthetic_data_hub.generation.generator import (
    SnapshotBundle,
    generate_snapshot_bundle,
    write_snapshot_bundle,
)
from enterprise_synthetic_data_hub.models.dataset_metadata import DatasetMetadata

SCHEMA_VERSION = settings.dataset_version


def generate_person_vehicle_dataset(
    num_records: int = 10, seed: int | None = 42
) -> Tuple[List[dict], List[dict]]:
    """Expose deterministic person + vehicle records for legacy consumers."""

    bundle = generate_snapshot_bundle(num_records=num_records, seed=seed)
    return bundle.persons, bundle.vehicles


def write_dataset_snapshot(
    persons: List[dict],
    vehicles: List[dict],
    output_dir: Path | None = None,
) -> Path:
    """Write dataset snapshot using the shared snapshot bundle helper."""

    metadata = DatasetMetadata(
        dataset_version=settings.dataset_version,
        generated_at=settings.generation_timestamp,
        record_count_persons=len(persons),
        record_count_vehicles=len(vehicles),
        notes="Legacy shim dataset snapshot.",
    )
    bundle = SnapshotBundle(metadata=metadata, persons=persons, vehicles=vehicles)
    return write_snapshot_bundle(bundle, output_dir)


__all__ = [
    "SCHEMA_VERSION",
    "generate_person_vehicle_dataset",
    "write_dataset_snapshot",
]
