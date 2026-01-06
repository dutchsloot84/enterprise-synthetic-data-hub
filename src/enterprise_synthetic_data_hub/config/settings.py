"""Project-wide configuration defaults.

These settings provide a single place to tune dataset-level parameters.
Future generator logic should import from here rather than re-defining
constants inline.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import os


@dataclass(frozen=True)
class DatasetSettings:
    """Basic configuration for dataset generation."""

    dataset_version: str = "v0.1"
    target_person_records: int = 200
    random_seed: int = 20240601
    generation_timestamp: datetime = datetime(2024, 6, 1, 0, 0, 0)
    synthetic_marker: str = "enterprise-synthetic-data-hub v0.1"
    demo_api_key_env: str = "ESDH_API_KEY"

    @property
    def demo_api_key(self) -> str | None:
        """Optional API key guard for demo deployments."""

        return os.getenv(self.demo_api_key_env)


settings = DatasetSettings()
