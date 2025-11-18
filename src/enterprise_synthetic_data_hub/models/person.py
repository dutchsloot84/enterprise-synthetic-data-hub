"""Person schema definition for the synthetic dataset POC."""
from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from enterprise_synthetic_data_hub.config.settings import settings


class Person(BaseModel):
    """Minimal representation of a person for Mobilitas / CSAA QA needs."""

    person_id: str = Field(..., description="Global unique identifier (UUID) for the person")
    first_name: str
    last_name: str
    date_of_birth: date
    driver_license_number: str
    driver_license_state: str = Field(..., min_length=2, max_length=2)
    address_line_1: str
    address_line_2: Optional[str] = None
    city: str
    state: str = Field(..., min_length=2, max_length=2)
    postal_code: str = Field(..., min_length=5, max_length=10)
    country: str = "US"
    lob_type: str = Field(..., description="Line of business classification (Personal, Commercial, Other)")
    synthetic_source: str = Field(
        default=settings.synthetic_marker,
        description="Indicates the governed synthetic origin for demo storytelling.",
    )

    model_config = ConfigDict(
        frozen=True,
        json_schema_extra={
            "examples": [
                {
                    "person_id": "c0f7be59-0eb5-4c6f-9f24-ffe236c05c77",
                    "first_name": "Ava",
                    "last_name": "Rivera",
                    "date_of_birth": "1988-05-21",
                    "driver_license_number": "D123-4567-8901",
                    "driver_license_state": "CA",
                    "address_line_1": "123 Main St",
                    "city": "Sacramento",
                    "state": "CA",
                    "postal_code": "95814",
                    "country": "US",
                    "lob_type": "Personal",
                }
            ]
        },
    )


__all__ = ["Person"]
