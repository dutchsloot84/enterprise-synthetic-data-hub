"""Vehicle schema definition for the synthetic dataset POC."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class Vehicle(BaseModel):
    """Vehicle representation linked to a Person."""

    vehicle_id: str = Field(..., description="Global unique identifier (UUID) for the vehicle")
    person_id: str = Field(..., description="Foreign key linking to Person.person_id")
    vin: str = Field(..., min_length=17, max_length=17)
    make: str
    model: str
    model_year: int = Field(..., ge=1980, le=2100)
    garaging_postal_code: str = Field(..., min_length=5, max_length=10)
    lob_type: str = Field(..., description="Line of business classification (Personal, Commercial, Other)")

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
                    "garaging_postal_code": "95814",
                    "lob_type": "Personal",
                }
            ]
        },
    )


__all__ = ["Vehicle"]
