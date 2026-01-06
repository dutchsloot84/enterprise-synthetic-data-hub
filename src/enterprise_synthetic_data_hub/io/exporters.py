"""Export helpers for CLI + downstream consumers."""
from __future__ import annotations

import csv
import hashlib
import json
import logging
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import pandas as pd

from enterprise_synthetic_data_hub.config.settings import settings
from enterprise_synthetic_data_hub.generation.generator import (
    SnapshotBundle,
    write_snapshot_bundle,
)
from enterprise_synthetic_data_hub.models.person import Person
from enterprise_synthetic_data_hub.models.vehicle import Vehicle

logger = logging.getLogger(__name__)

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


def _write_ndjson(path: Path, rows: Iterable[dict]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row))
            handle.write("\n")


def _write_parquet(path: Path, rows: Iterable[dict]) -> None:
    df = pd.DataFrame(rows)
    df.to_parquet(path, index=False)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 64), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _age_stats(persons: Sequence[Mapping[str, str]]) -> dict:
    ages: list[int] = []
    lob_counts: dict[str, int] = {}
    for person in persons:
        dob = person.get("date_of_birth")
        try:
            age_years = int(
                (settings.generation_timestamp.date() - pd.to_datetime(dob).date()).days // 365
            )
            ages.append(age_years)
        except Exception:  # pragma: no cover - defensive for bad input
            continue
        lob = person.get("lob_type")
        if lob:
            lob_counts[lob] = lob_counts.get(lob, 0) + 1
    if not ages:
        return {}
    return {
        "min_age": min(ages),
        "max_age": max(ages),
        "average_age": round(sum(ages) / len(ages), 2),
        "lob_distribution": lob_counts,
    }


def _vehicle_stats(vehicles: Sequence[Mapping[str, str]]) -> dict:
    vin_prefix: dict[str, int] = {}
    make_counts: dict[str, int] = {}
    for vehicle in vehicles:
        vin = vehicle.get("vin", "")
        if vin:
            vin_prefix[vin[0]] = vin_prefix.get(vin[0], 0) + 1
        make = vehicle.get("make")
        if make:
            make_counts[make] = make_counts.get(make, 0) + 1
    return {"vin_prefix_distribution": vin_prefix, "make_distribution": make_counts}


def export_snapshot_bundle(
    bundle: SnapshotBundle,
    output_dir: Path | None = None,
    *,
    entity_filter: set[str] | None = None,
    output_formats: Sequence[str] | None = None,
) -> dict:
    """Persist governed CSV/JSON + manifest artifacts for the snapshot."""

    entity_filter = entity_filter or set()
    output_formats = output_formats or ["csv", "json"]

    output_dir = Path(output_dir or Path("data") / "snapshots" / bundle.metadata.dataset_version)
    output_dir.mkdir(parents=True, exist_ok=True)

    version_slug = bundle.metadata.dataset_version.replace(".", "_")
    persons_path = output_dir / f"persons_{version_slug}.csv"
    vehicles_path = output_dir / f"vehicles_{version_slug}.csv"
    persons_ndjson_path = output_dir / f"persons_{version_slug}.ndjson"
    vehicles_ndjson_path = output_dir / f"vehicles_{version_slug}.ndjson"
    persons_parquet_path = output_dir / f"persons_{version_slug}.parquet"
    vehicles_parquet_path = output_dir / f"vehicles_{version_slug}.parquet"
    manifest_path = output_dir / f"snapshot_manifest_{version_slug}.json"
    readme_path = output_dir / f"README_SNAPSHOT_{version_slug.upper()}.md"

    artifacts: dict[str, Path] = {}

    if not entity_filter or "persons" in entity_filter:
        if "csv" in output_formats:
            _write_csv(persons_path, bundle.persons, PERSON_COLUMNS)
            artifacts["persons_csv"] = persons_path
        if "ndjson" in output_formats:
            _write_ndjson(persons_ndjson_path, bundle.persons)
            artifacts["persons_ndjson"] = persons_ndjson_path
        if "parquet" in output_formats:
            _write_parquet(persons_parquet_path, bundle.persons)
            artifacts["persons_parquet"] = persons_parquet_path

    if not entity_filter or "vehicles" in entity_filter:
        if "csv" in output_formats:
            _write_csv(vehicles_path, bundle.vehicles, VEHICLE_COLUMNS)
            artifacts["vehicles_csv"] = vehicles_path
        if "ndjson" in output_formats:
            _write_ndjson(vehicles_ndjson_path, bundle.vehicles)
            artifacts["vehicles_ndjson"] = vehicles_ndjson_path
        if "parquet" in output_formats:
            _write_parquet(vehicles_parquet_path, bundle.vehicles)
            artifacts["vehicles_parquet"] = vehicles_parquet_path

    dataset_path = write_snapshot_bundle(bundle, output_dir)
    metadata_path = dataset_path.with_name(dataset_path.name.replace("dataset_", "metadata_"))
    artifacts["dataset_json"] = dataset_path
    artifacts["metadata_json"] = metadata_path

    manifest = {
        "dataset_version": bundle.metadata.dataset_version,
        "generated_at": bundle.metadata.generated_at.isoformat(),
        "record_counts": {
            "persons": len(bundle.persons),
            "vehicles": len(bundle.vehicles),
            "profiles": len(bundle.profiles),
        },
        "files": {label: path.name for label, path in artifacts.items()},
        "checksums": {label: _sha256(path) for label, path in artifacts.items()},
        "stats": {
            "persons": _age_stats(bundle.persons),
            "vehicles": _vehicle_stats(bundle.vehicles),
        },
        "notes": bundle.metadata.notes,
        "synthetic_marker": settings.synthetic_marker,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    artifacts["manifest_json"] = manifest_path

    readme_lines = [
        f"# Snapshot {bundle.metadata.dataset_version}",
        "",  # blank line
        "Files exported by the CLI:",
    ]
    for label, path in artifacts.items():
        suffix = ""
        if label.endswith("ndjson"):
            suffix = " (NDJSON export)"
        elif label.endswith("parquet"):
            suffix = " (Parquet export)"
        elif label.endswith("csv"):
            suffix = " (CSV export)"
        elif label.startswith("dataset_json"):
            suffix = " (combined JSON bundle)"
        elif label.startswith("metadata_json"):
            suffix = " (metadata JSON)"
        elif label.startswith("manifest_json"):
            suffix = " (manifest with stats + checksums)"
        readme_lines.append(f"- {path.name}{suffix}")
    readme_lines.extend(
        [
            "",
            "Re-generate via:",
            "```bash",
            "python -m enterprise_synthetic_data_hub.cli.main generate-snapshot",
            "```",
        ]
    )
    readme_path.write_text("\n".join(readme_lines), encoding="utf-8")

    artifacts["readme"] = readme_path

    logger.info(
        "Snapshot exported",
        extra={
            "output_dir": str(output_dir),
            "files": list(artifacts.keys()),
            "record_counts": manifest["record_counts"],
        },
    )

    return artifacts


def export_snapshot_stub(output_dir: Path, persons: Iterable[Person], vehicles: Iterable[Vehicle]) -> None:
    """Compatibility shim for legacy callers.

    The CLI and validators now route through :func:`export_snapshot_bundle`, but the
    stub is retained so older instructions do not break during the transition.
    """

    raise RuntimeError(
        "export_snapshot_stub is deprecated. Use export_snapshot_bundle with a full SnapshotBundle."
    )


__all__ = ["export_snapshot_bundle"]
