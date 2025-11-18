"""Helpers shared across the scripted demo flow."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from enterprise_synthetic_data_hub.config import demo_profiles


@dataclass
class DemoRunState:
    """Track demo execution context for diagnostics + summary output."""

    profile: demo_profiles.DemoProfile
    snapshot_dir: Path | None = None
    manifest: dict[str, Any] | None = None
    base_url: str | None = None
    api_port: str | None = None
    timings: dict[str, float] = field(default_factory=dict)

    def record_timing(self, key: str, value: float) -> None:
        self.timings[key] = value


__all__ = ["DemoRunState"]
