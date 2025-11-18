"""Profile schema derived from governed Person and Vehicle entities."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from enterprise_synthetic_data_hub.config.settings import settings


class Profile(BaseModel):
    """Join-friendly view that powers demo previews and the API."""

    profile_id: str = Field(..., description="Deterministic identifier for the profile row")
    person_id: str = Field(..., description="Foreign key to the Person record")
    vehicle_id: str = Field(..., description="Foreign key to the Vehicle record")
    full_name: str
    lob_type: str
    residence_state: str = Field(..., min_length=2, max_length=2)
    city: str
    postal_code: str
    garaging_state: str = Field(..., min_length=2, max_length=2)
    primary_vehicle_vin: str
    vehicle_summary: str
    risk_rating: str
    synthetic_source: str = Field(
        default=settings.synthetic_marker,
        description="Indicates the governed synthetic origin for demo storytelling.",
    )

    model_config = ConfigDict(frozen=True)


__all__ = ["Profile"]
