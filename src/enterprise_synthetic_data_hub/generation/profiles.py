"""Helpers for deriving profile records from persons and vehicles."""
from __future__ import annotations

import uuid
from typing import Sequence

from enterprise_synthetic_data_hub.config.settings import settings
from enterprise_synthetic_data_hub.models.profile import Profile

_PROFILE_NAMESPACE = uuid.UUID("ca92fd9b-5368-4924-8db6-bb1f56766c2b")


def _build_profile_id(person_id: str, vehicle_id: str) -> str:
    seed = f"{person_id}:{vehicle_id}"
    return str(uuid.uuid5(_PROFILE_NAMESPACE, seed))


def build_profiles(
    persons: Sequence[dict],
    vehicles: Sequence[dict],
    *,
    synthetic_source: str | None = None,
) -> list[dict]:
    """Return deterministic profiles derived from governed entities."""

    vehicle_lookup = {vehicle["person_id"]: vehicle for vehicle in vehicles}
    profiles: list[dict] = []
    for person in persons:
        vehicle = vehicle_lookup.get(person["person_id"])
        if vehicle is None:
            continue
        profile = Profile(
            profile_id=_build_profile_id(person["person_id"], vehicle["vehicle_id"]),
            person_id=person["person_id"],
            vehicle_id=vehicle["vehicle_id"],
            full_name=f"{person['first_name']} {person['last_name']}",
            lob_type=person["lob_type"],
            residence_state=person["state"],
            city=person["city"],
            postal_code=person["postal_code"],
            garaging_state=vehicle["garaging_state"],
            primary_vehicle_vin=vehicle["vin"],
            vehicle_summary=f"{vehicle['model_year']} {vehicle['make']} {vehicle['model']}",
            risk_rating=vehicle["risk_rating"],
            synthetic_source=synthetic_source or settings.synthetic_marker,
        )
        profiles.append(profile.model_dump(mode="json"))
    return profiles


__all__ = ["build_profiles"]
