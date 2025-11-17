from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from generator.synthetic_generator_v01 import (
    SCHEMA_VERSION,
    generate_person_vehicle_dataset,
    write_dataset_snapshot,
)


def test_generator_returns_matching_counts():
    persons, vehicles = generate_person_vehicle_dataset(num_records=3, seed=7)
    assert len(persons) == 3
    assert len(vehicles) == 3
    assert persons[0]["person_id"]
    assert vehicles[0]["person_id"] == persons[0]["person_id"]


def test_snapshot_writer_persists_json(tmp_path):
    persons, vehicles = generate_person_vehicle_dataset(num_records=2, seed=9)
    path = write_dataset_snapshot(persons, vehicles, tmp_path)
    payload = json.loads(path.read_text())
    assert payload["version"] == SCHEMA_VERSION
    assert payload["person_count"] == 2
    assert payload["vehicle_count"] == 2
