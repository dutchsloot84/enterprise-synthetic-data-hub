from __future__ import annotations

from enterprise_synthetic_data_hub.generation.generator import generate_snapshot_bundle
from enterprise_synthetic_data_hub.generation.profiles import build_profiles


def test_build_profiles_matches_generator_counts():
    bundle = generate_snapshot_bundle(num_records=4, seed=77)
    derived = build_profiles(bundle.persons, bundle.vehicles)
    assert len(derived) == len(bundle.persons) == len(bundle.vehicles)
    assert derived[0]["person_id"] == bundle.persons[0]["person_id"]
    assert derived[0]["synthetic_source"] == bundle.persons[0]["synthetic_source"]


def test_profile_fields_are_deterministic():
    bundle_a = generate_snapshot_bundle(num_records=2, seed=5)
    bundle_b = generate_snapshot_bundle(num_records=2, seed=5)
    assert bundle_a.profiles == bundle_b.profiles
