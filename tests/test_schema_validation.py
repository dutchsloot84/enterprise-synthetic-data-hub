from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agentic.validators import schema_validator


SCHEMA_DIR = ROOT / "schemas" / "v0.1"


def _load_schema(name: str) -> dict:
    return yaml.safe_load((SCHEMA_DIR / name).read_text())


def test_schema_files_have_matching_field_counts():
    for filename in ("person_schema.yaml", "vehicle_schema.yaml"):
        data = _load_schema(filename)
        assert data["field_count"] == len(data["fields"])


def test_schema_validator_finds_no_errors():
    errors = []
    for filename in ("person_schema.yaml", "vehicle_schema.yaml"):
        path = SCHEMA_DIR / filename
        errors.extend(schema_validator.validate_schema(path))
    assert not errors
