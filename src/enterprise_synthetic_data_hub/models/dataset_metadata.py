"""Dataset-level metadata schema."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DatasetMetadata(BaseModel):
    """Captures information about a generated snapshot."""

    dataset_version: str = Field(..., description="Semantic version of the dataset snapshot")
    generated_at: datetime
    record_count_persons: int = Field(..., ge=0)
    record_count_vehicles: int = Field(..., ge=0)
    record_count_profiles: int = Field(..., ge=0)
    notes: Optional[str] = None

    model_config = ConfigDict(frozen=True)


__all__ = ["DatasetMetadata"]
