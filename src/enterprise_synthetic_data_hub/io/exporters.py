"""Export helpers (stubs)."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from enterprise_synthetic_data_hub.models.person import Person
from enterprise_synthetic_data_hub.models.vehicle import Vehicle


def export_snapshot_stub(output_dir: Path, persons: Iterable[Person], vehicles: Iterable[Vehicle]) -> None:
    """Placeholder exporter that documents future expectations."""

    # TODO: Implement CSV/JSON export logic aligned with governance rules.
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "README_EXPORT_PENDING.md").write_text(
        "Snapshot export not implemented yet. Use generation prompt 03 before exporting.",
        encoding="utf-8",
    )
