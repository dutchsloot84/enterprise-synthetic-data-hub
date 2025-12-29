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
        ...,
        description="Indicates the governed synthetic origin for demo storytelling.",
    )

    model_config = ConfigDict(
        frozen=True,
        json_schema_extra={
            "examples": [
                {
                    "profile_id": "8dc78f6a-b2d9-5ad4-845d-e2166d4ad8ea",
                    "person_id": "c0f7be59-0eb5-4c6f-9f24-ffe236c05c77",
                    "vehicle_id": "d4d43008-76d3-4a44-9972-5e6a9b2fd3a8",
                    "full_name": "Ava Rivera",
                    "lob_type": "Personal",
                    "residence_state": "CA",
                    "city": "Sacramento",
                    "postal_code": "95814",
                    "garaging_state": "CA",
                    "primary_vehicle_vin": "1HGBH41JXMN109186",
                    "vehicle_summary": "2021 Toyota Camry",
                    "risk_rating": "Low",
                    "synthetic_source": settings.synthetic_marker,
                }
            ]
        },
    )


__all__ = ["Profile"]
