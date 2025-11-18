from __future__ import annotations

import re

from enterprise_synthetic_data_hub.models.vehicle import Vehicle

UUID_PATTERN = re.compile(r"^[0-9a-fA-F-]{36}$")
VIN_PATTERN = re.compile(r"^[A-HJ-NPR-Z0-9]{17}$")


def test_vehicle_schema_fields():
    vehicle = Vehicle(
        vehicle_id="223e4567-e89b-12d3-a456-426614174001",
        person_id="123e4567-e89b-12d3-a456-426614174000",
        vin="1HGCM82633A004352",
        make="Honda",
        model="Accord",
        model_year=2022,
        body_style="SUV",
        risk_rating="Low",
        garaging_postal_code="95112",
        garaging_state="CA",
        lob_type="Personal",
        synthetic_source="enterprise-synthetic-data-hub v0.1",
    )

    assert UUID_PATTERN.match(vehicle.vehicle_id)
    assert VIN_PATTERN.match(vehicle.vin)
    assert 1980 <= vehicle.model_year <= 2100
