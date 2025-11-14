from __future__ import annotations

import re
from datetime import date

from enterprise_synthetic_data_hub.models.person import Person

UUID_PATTERN = re.compile(r"^[0-9a-fA-F-]{36}$")


def test_person_schema_fields():
    person = Person(
        person_id="123e4567-e89b-12d3-a456-426614174000",
        first_name="Test",
        last_name="User",
        date_of_birth=date(1990, 1, 1),
        driver_license_number="T123-4567-8901",
        driver_license_state="CA",
        address_line_1="1 Test Way",
        city="San Jose",
        state="CA",
        postal_code="95112",
        country="US",
        lob_type="Personal",
    )

    assert UUID_PATTERN.match(person.person_id)
    assert person.country == "US"
    assert person.driver_license_state == "CA"
