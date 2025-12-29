"""Inspect demo profile metadata and payload structure."""
from __future__ import annotations

import argparse
import json
from typing import Any, Dict

from enterprise_synthetic_data_hub.config import demo_profiles
from enterprise_synthetic_data_hub.config.settings import settings
from enterprise_synthetic_data_hub.models.person import Person
from enterprise_synthetic_data_hub.models.profile import Profile
from enterprise_synthetic_data_hub.models.vehicle import Vehicle


def _payload_shape() -> Dict[str, list[str]]:
    return {
        "persons_fields": list(Person.model_fields),
        "vehicles_fields": list(Vehicle.model_fields),
        "profiles_fields": list(Profile.model_fields),
    }


def gather_profile_info(profile_name: str | None = None) -> dict[str, Any]:
    profile = demo_profiles.get_demo_profile(profile_name)
    api_defaults = demo_profiles.get_api_settings()
    return {
        "profile": profile.name,
        "records": {
            "persons": profile.records_person,
            "vehicles": profile.records_vehicle,
            "profiles": profile.records_profile,
        },
        "seed": profile.seed,
        "randomize": profile.randomize,
        "api_defaults": {
            "host": api_defaults.host,
            "port": api_defaults.port,
            "health_endpoint": api_defaults.health_endpoint,
        },
        "dataset_version": settings.dataset_version,
        "synthetic_marker": settings.synthetic_marker,
        "payload_shape": _payload_shape(),
    }


def _print_readable(info: dict[str, Any]) -> None:
    print(f"Profile: {info['profile']}")
    print(f"  Persons: {info['records']['persons']}")
    print(f"  Vehicles: {info['records']['vehicles']}")
    print(f"  Profiles: {info['records']['profiles']}")
    print(f"Seed: {info['seed']}")
    print(f"Randomize: {info['randomize']}")
    print("API Defaults:")
    print(f"  Host: {info['api_defaults']['host']}")
    print(f"  Port: {info['api_defaults']['port']}")
    print(f"  Health endpoint: {info['api_defaults']['health_endpoint']}")
    print("Payload shape keys:")
    for key, fields in info["payload_shape"].items():
        print(f"  {key}: {', '.join(fields)}")
    print(f"Synthetic marker: {info['synthetic_marker']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inspect demo profile configuration")
    parser.add_argument("--profile", default=None, help="Demo profile name (default: baseline)")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args(argv)
    info = gather_profile_info(args.profile)
    if args.json:
        print(json.dumps(info, indent=2))
    else:
        _print_readable(info)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
