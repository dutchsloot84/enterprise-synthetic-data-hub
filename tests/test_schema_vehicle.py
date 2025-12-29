from __future__ import annotations

from enterprise_synthetic_data_hub.config.settings import settings
from enterprise_synthetic_data_hub.models.vehicle import Vehicle


def test_vehicle_schema_fields():
    vehicle = Vehicle(
        vehicle_id="123e4567-e89b-12d3-a456-426614174000",
        person_id="123e4567-e89b-12d3-a456-426614174001",
        vin="1HGBH41JXMN109186",
        make="Test",
        model="Car",
        model_year=2020,
        body_style="SUV",
        risk_rating="Low",
        garaging_state="CA",
        garaging_postal_code="94105",
        lob_type="Personal",
        synthetic_source=settings.synthetic_marker,
    )

    assert vehicle.vehicle_id
    assert vehicle.vin.startswith("1HGBH")
