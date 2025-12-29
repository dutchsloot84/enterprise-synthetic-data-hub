"""Lightweight schema validator for the agentic workflow."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = "v0.1"
SCHEMA_DIR = REPO_ROOT / "schemas" / SCHEMA_VERSION
REQUIRED_FILES = [
    "person_schema.yaml",
    "vehicle_schema.yaml",
    "dataset_metadata_schema.yaml",
]


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def validate_schema(path: Path) -> list[str]:
    data = _load_yaml(path)
    errors: list[str] = []
    for key in ("version", "last_updated", "field_count", "fields"):
        if key not in data:
            errors.append(f"{path.name} missing required key '{key}'")
    if data.get("version") != SCHEMA_VERSION:
        errors.append(
            f"{path.name} declares version {data.get('version')} but expected {SCHEMA_VERSION}"
        )
    fields = data.get("fields", [])
    if not isinstance(fields, list):
        errors.append(f"{path.name} fields must be a list")
    else:
        declared_count = data.get("field_count")
        if declared_count != len(fields):
            errors.append(
                f"{path.name} field_count={declared_count} but contains {len(fields)} entries"
            )
        for field in fields:
            for required_key in ("name", "type", "required"):
                if required_key not in field:
                    errors.append(
                        f"{path.name} field '{field}' missing key '{required_key}'"
                    )
    return errors


def main() -> int:
    missing = [name for name in REQUIRED_FILES if not (SCHEMA_DIR / name).exists()]
    if missing:
        print(json.dumps({"status": "error", "missing_files": missing}, indent=2))
        return 1

    results: dict[str, Any] = {"status": "ok", "schemas": []}
    overall_errors: list[str] = []

    for filename in REQUIRED_FILES:
        path = SCHEMA_DIR / filename
        errors = validate_schema(path)
        results["schemas"].append({"file": filename, "errors": errors})
        overall_errors.extend(errors)

    if overall_errors:
        results["status"] = "error"
    print(json.dumps(results, indent=2))
    return 0 if not overall_errors else 1


# Usage:
#   python agentic/validators/schema_validator.py
if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
