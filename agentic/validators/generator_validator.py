"""Generator validator ensuring deterministic outputs."""
from __future__ import annotations

import json
import sys
from pathlib import Path

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


def main() -> int:
    from enterprise_synthetic_data_hub.generation.generator import generate_snapshot_bundle

    bundle_a = generate_snapshot_bundle(num_records=5, seed=123)
    bundle_b = generate_snapshot_bundle(num_records=5, seed=123)
    persons_a, vehicles_a = bundle_a.persons, bundle_a.vehicles
    persons_b, vehicles_b = bundle_b.persons, bundle_b.vehicles

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
