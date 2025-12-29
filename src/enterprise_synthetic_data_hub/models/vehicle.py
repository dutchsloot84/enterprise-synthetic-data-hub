from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from enterprise_synthetic_data_hub.config.settings import settings


class Vehicle(BaseModel):
    """Vehicle representation linked to a Person."""

    vehicle_id: str = Field(..., description="Global unique identifier (UUID) for the vehicle")
    person_id: str = Field(..., description="Foreign key linking to Person.person_id")
    vin: str = Field(..., min_length=17, max_length=17)
    make: str
    model: str
    model_year: int = Field(..., ge=1980, le=2100)
    body_style: str
    risk_rating: str
    lob_type: str = Field(..., description="Line of business classification (Personal, Commercial, Other)")
    garaging_state: str = Field(..., min_length=2, max_length=2)
    garaging_postal_code: str = Field(..., min_length=5, max_length=10)
    synthetic_source: str = Field(
        ...,
        description="Indicates the governed synthetic origin for demo storytelling.",
    )

    model_config = ConfigDict(
        frozen=True,
        json_schema_extra={
            "examples": [
                {
                    "vehicle_id": "d4d43008-76d3-4a44-9972-5e6a9b2fd3a8",
                    "person_id": "c0f7be59-0eb5-4c6f-9f24-ffe236c05c77",
                    "vin": "1HGBH41JXMN109186",
                    "make": "Toyota",
                    "model": "Camry",
                    "model_year": 2021,
                    "body_style": "SUV",
                    "risk_rating": "Low",
                    "garaging_state": "CA",
                    "garaging_postal_code": "95814",
                    "lob_type": "Personal",
                    "synthetic_source": settings.synthetic_marker,
                }
            ]
        },
    )


__all__ = ["Vehicle"]
