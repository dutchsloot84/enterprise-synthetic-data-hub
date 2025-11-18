"""Export helpers for CLI + downstream consumers."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable, Sequence

from enterprise_synthetic_data_hub.generation.generator import (
    SnapshotBundle,
    write_snapshot_bundle,
)
from enterprise_synthetic_data_hub.models.person import Person
from enterprise_synthetic_data_hub.models.vehicle import Vehicle

PERSON_COLUMNS: Sequence[str] = (
    "person_id",
    "first_name",
    "last_name",
    "date_of_birth",
    "driver_license_number",
    "driver_license_state",
    "address_line_1",
    "address_line_2",
    "city",
    "state",
    "postal_code",
    "country",
    "lob_type",
    "synthetic_source",
)
VEHICLE_COLUMNS: Sequence[str] = (
    "vehicle_id",
    "person_id",
    "vin",
    "make",
    "model",
    "model_year",
    "body_style",
    "risk_rating",
    "lob_type",
    "garaging_state",
    "garaging_postal_code",
    "synthetic_source",
)


def _serialize_row(row: dict, columns: Sequence[str]) -> dict:
    return {column: ("" if row.get(column) is None else row.get(column)) for column in columns}


def _write_csv(path: Path, rows: Iterable[dict], columns: Sequence[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow(_serialize_row(row, columns))


def export_snapshot_bundle(bundle: SnapshotBundle, output_dir: Path | None = None) -> dict:
    """Persist governed CSV/JSON + manifest artifacts for the snapshot."""

    output_dir = Path(output_dir or Path("data") / "snapshots" / bundle.metadata.dataset_version)
    output_dir.mkdir(parents=True, exist_ok=True)

    version_slug = bundle.metadata.dataset_version.replace(".", "_")
    persons_path = output_dir / f"persons_{version_slug}.csv"
    vehicles_path = output_dir / f"vehicles_{version_slug}.csv"
    manifest_path = output_dir / f"snapshot_manifest_{version_slug}.json"
    readme_path = output_dir / f"README_SNAPSHOT_{version_slug.upper()}.md"

    _write_csv(persons_path, bundle.persons, PERSON_COLUMNS)
    _write_csv(vehicles_path, bundle.vehicles, VEHICLE_COLUMNS)

    dataset_path = write_snapshot_bundle(bundle, output_dir)
    metadata_path = dataset_path.with_name(dataset_path.name.replace("dataset_", "metadata_"))

    manifest = {
        "dataset_version": bundle.metadata.dataset_version,
        "generated_at": bundle.metadata.generated_at.isoformat(),
        "record_counts": {
            "persons": len(bundle.persons),
            "vehicles": len(bundle.vehicles),
            "profiles": len(bundle.profiles),
        },
        "files": {
            "persons_csv": persons_path.name,
            "vehicles_csv": vehicles_path.name,
            "dataset_json": dataset_path.name,
            "metadata_json": metadata_path.name,
        },
        "notes": bundle.metadata.notes,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    readme_path.write_text(
        "\n".join(
            [
                f"# Snapshot {bundle.metadata.dataset_version}",
                "",  # blank line
                "Files exported by the CLI:",
                f"- {persons_path.name} (persons CSV)",
                f"- {vehicles_path.name} (vehicles CSV)",
                f"- {dataset_path.name} (combined JSON bundle)",
                f"- {metadata_path.name} (metadata JSON)",
                f"- {manifest_path.name} (manifest)",
                "",
                "Re-generate via:",
                "```bash",
                "python -m enterprise_synthetic_data_hub.cli.main generate-snapshot",
                "```",
            ]
        ),
        encoding="utf-8",
    )

    return {
        "persons_csv": persons_path,
        "vehicles_csv": vehicles_path,
        "dataset_json": dataset_path,
        "metadata_json": metadata_path,
        "manifest_json": manifest_path,
        "readme": readme_path,
    }


def export_snapshot_stub(output_dir: Path, persons: Iterable[Person], vehicles: Iterable[Vehicle]) -> None:
    """Compatibility shim for legacy callers.

    The CLI and validators now route through :func:`export_snapshot_bundle`, but the
    stub is retained so older instructions do not break during the transition.
    """

    raise RuntimeError(
        "export_snapshot_stub is deprecated. Use export_snapshot_bundle with a full SnapshotBundle."
    )


__all__ = ["export_snapshot_bundle"]
