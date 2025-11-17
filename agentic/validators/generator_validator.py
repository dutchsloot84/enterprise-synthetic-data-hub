"""Generator validator ensuring deterministic outputs."""
from __future__ import annotations

import json
import sys
from importlib import import_module
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

SCHEMA_DIR = REPO_ROOT / "schemas" / "v0.1"
PERSON_FIELDS = {
    field["name"]
    for field in yaml.safe_load((SCHEMA_DIR / "person_schema.yaml").read_text())[
        "fields"
    ]
}
VEHICLE_FIELDS = {
    field["name"]
    for field in yaml.safe_load((SCHEMA_DIR / "vehicle_schema.yaml").read_text())[
        "fields"
    ]
}


def _load_generator() -> Any:
    return import_module("generator.synthetic_generator_v01")


def main() -> int:
    module = _load_generator()
    persons_a, vehicles_a = module.generate_person_vehicle_dataset(num_records=5, seed=123)
    persons_b, vehicles_b = module.generate_person_vehicle_dataset(num_records=5, seed=123)

    errors: list[str] = []
    if persons_a != persons_b or vehicles_a != vehicles_b:
        errors.append("Generator output is not deterministic for the same seed")

    if len(persons_a) != 5 or len(vehicles_a) != 5:
        errors.append("Generator did not return the expected record counts")

    for person in persons_a:
        missing = PERSON_FIELDS - person.keys()
        if missing:
            errors.append(f"Person record missing fields: {sorted(missing)}")
            break
    for vehicle in vehicles_a:
        missing = VEHICLE_FIELDS - vehicle.keys()
        if missing:
            errors.append(f"Vehicle record missing fields: {sorted(missing)}")
            break

    summary = {
        "status": "error" if errors else "ok",
        "person_count": len(persons_a),
        "vehicle_count": len(vehicles_a),
        "errors": errors,
    }
    print(json.dumps(summary, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
