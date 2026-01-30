# Phase 1 Demo Samples & Golden Snapshots

- **Seed**: `20251101` (matches `DatasetSettings.random_seed`)
- **Note**: The seed is a deterministic anchor, not the project start date. Changing it requires regenerating golden snapshots.
- **Goal**: keep demo payloads deterministic so slide decks and golden tests stay stable.

## Regenerate demo backup payloads

```bash
PYTHONPATH=src python - <<'PY'
import json
from pathlib import Path
from enterprise_synthetic_data_hub.api.app import create_app
from enterprise_synthetic_data_hub.config.settings import settings

seed = settings.random_seed
records = 3
output_dir = Path("data/demo_samples/phase1")
output_dir.mkdir(parents=True, exist_ok=True)

app = create_app()
app.testing = True
with app.test_client() as client:
    endpoints = {
        "persons_seed_20251101.json": ("/generate/person", {"records": records, "seed": seed}),
        "vehicles_seed_20251101.json": ("/generate/vehicle", {"records": records, "seed": seed}),
        "profiles_seed_20251101.json": ("/generate/profile", {"records": records, "seed": seed}),
        "bundle_seed_20251101.json": ("/generate/bundle", {"records": records, "seed": seed}),
    }
    for filename, (endpoint, body) in endpoints.items():
        resp = client.post(endpoint, json=body)
        assert resp.status_code == 200, resp.data
        payload = resp.get_json()
        (output_dir / filename).write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
PY
```

## Regenerate golden snapshots (used by smoke tests)

```bash
PYTHONPATH=src python - <<'PY'
import json
from pathlib import Path
from enterprise_synthetic_data_hub.api.app import create_app
from enterprise_synthetic_data_hub.config.settings import settings

seed = settings.random_seed
records = 3
output_dir = Path("tests/golden")
output_dir.mkdir(parents=True, exist_ok=True)

app = create_app()
app.testing = True
with app.test_client() as client:
    payloads = {
        "healthz_seed20251101.json": client.get("/healthz").get_json(),
        "person_seed20251101_count3.json": client.post("/generate/person", json={"records": records, "seed": seed}).get_json(),
        "vehicle_seed20251101_count3.json": client.post("/generate/vehicle", json={"records": records, "seed": seed}).get_json(),
        "profile_seed20251101_count3.json": client.post("/generate/profile", json={"records": records, "seed": seed}).get_json(),
        "bundle_seed20251101_count3.json": client.post("/generate/bundle", json={"records": records, "seed": seed}).get_json(),
    }

for name, payload in payloads.items():
    Path(output_dir / name).write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
PY
```

**If tests/golden snapshots fail after a schema change, regenerate artifacts using the commands below.**

## Determinism tripwires

- Keep `DatasetSettings.generation_timestamp` and `DatasetSettings.random_seed` unchanged when regenerating.
- Endpoints should be called with the explicit `seed` and `records` shown above to avoid any randomness.
- Timestamps and UUIDs are already seeded/fixed; if an unexpected timestamp appears, regenerate after verifying the seed is set to `20251101`.

## When to regenerate (demo backups + golden snapshots)

- Any schema/contract update (fields added/removed/renamed, required keys/type changes)
- Relationship logic changes that affect profile/person/vehicle linkages
- API envelope changes (e.g., `/healthz` metadata shape or error envelope updates)
- Generator rule tweaks that alter outputs even with the same seed

Regenerating both `data/demo_samples/phase1/*.json` and `tests/golden/*.json` prevents demo drift and keeps golden tests aligned with the governed contract.
