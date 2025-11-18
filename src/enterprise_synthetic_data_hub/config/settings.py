"""Project-wide configuration defaults.

These settings provide a single place to tune dataset-level parameters.
Future generator logic should import from here rather than re-defining
constants inline.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class DatasetSettings:
    """Basic configuration for dataset generation."""

    dataset_version: str = "v0.1"
    target_person_records: int = 200
    random_seed: int = 20240601
    generation_timestamp: datetime = datetime(2024, 6, 1, 0, 0, 0)
    synthetic_marker: str = "enterprise-synthetic-data-hub v0.1"


settings = DatasetSettings()
