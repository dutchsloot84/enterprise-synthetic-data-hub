from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.validators import schema_validator


SCHEMA_DIR = ROOT / "schemas" / "v0.1"
SCHEMA_FILES = (
    "person_schema.yaml",
    "vehicle_schema.yaml",
    "dataset_metadata_schema.yaml",
)


def _load_schema(name: str) -> dict:
    return yaml.safe_load((SCHEMA_DIR / name).read_text())


def test_schema_files_have_matching_field_counts():
    for filename in SCHEMA_FILES:
        data = _load_schema(filename)
        assert data["field_count"] == len(data["fields"])


def test_schema_validator_finds_no_errors():
    errors = []
    for filename in SCHEMA_FILES:
        path = SCHEMA_DIR / filename
        errors.extend(schema_validator.validate_schema(path))
    assert not errors


def test_person_schema_includes_optional_address_line_2():
    data = _load_schema("person_schema.yaml")
    optional_fields = [field for field in data["fields"] if field["name"] == "address_line_2"]
    assert optional_fields, "address_line_2 field missing"
    assert optional_fields[0]["required"] is False


def test_dataset_metadata_schema_tracks_record_counts():
    data = _load_schema("dataset_metadata_schema.yaml")
    field_names = {field["name"] for field in data["fields"]}
    assert {"record_count_persons", "record_count_vehicles"}.issubset(field_names)
