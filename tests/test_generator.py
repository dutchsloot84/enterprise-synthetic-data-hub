from __future__ import annotations

import json

from enterprise_synthetic_data_hub.config.settings import settings
from enterprise_synthetic_data_hub.generation.generator import (
    SnapshotBundle,
    generate_snapshot_bundle,
    write_snapshot_bundle,
)


def test_generate_snapshot_bundle_deterministic():
    bundle_a = generate_snapshot_bundle(num_records=3, seed=7)
    bundle_b = generate_snapshot_bundle(num_records=3, seed=7)

    assert bundle_a.persons == bundle_b.persons
    assert bundle_a.vehicles == bundle_b.vehicles
    assert bundle_a.metadata.record_count_persons == 3
    assert bundle_a.metadata.record_count_vehicles == 3


def test_generate_snapshot_bundle_rejects_invalid_count():
    try:
        generate_snapshot_bundle(num_records=0)
    except ValueError as exc:
        assert "positive" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("generate_snapshot_bundle should reject non-positive counts")


def test_write_snapshot_bundle_persists_json(tmp_path):
    bundle = generate_snapshot_bundle(num_records=2, seed=9)
    path = write_snapshot_bundle(bundle, tmp_path)

    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["metadata"]["dataset_version"] == settings.dataset_version
    assert payload["metadata"]["record_count_persons"] == 2
    assert payload["metadata"]["record_count_vehicles"] == 2
    assert len(payload["persons"]) == 2
    assert len(payload["vehicles"]) == 2


def test_snapshot_bundle_type_annotations():
    bundle = generate_snapshot_bundle(num_records=1, seed=1)
    assert isinstance(bundle, SnapshotBundle)
    assert bundle.metadata.dataset_version == settings.dataset_version
