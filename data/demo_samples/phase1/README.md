# Phase 1 Demo Samples & Golden Snapshots

- **Seed**: `20240601` (matches `DatasetSettings.random_seed`)
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
        "persons_seed_20240601.json": ("/generate/person", {"records": records, "seed": seed}),
        "vehicles_seed_20240601.json": ("/generate/vehicle", {"records": records, "seed": seed}),
        "profiles_seed_20240601.json": ("/generate/profile", {"records": records, "seed": seed}),
        "bundle_seed_20240601.json": ("/generate/bundle", {"records": records, "seed": seed}),
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
        "healthz_seed20240601.json": client.get("/healthz").get_json(),
        "person_seed20240601_count3.json": client.post("/generate/person", json={"records": records, "seed": seed}).get_json(),
        "vehicle_seed20240601_count3.json": client.post("/generate/vehicle", json={"records": records, "seed": seed}).get_json(),
        "profile_seed20240601_count3.json": client.post("/generate/profile", json={"records": records, "seed": seed}).get_json(),
        "bundle_seed20240601_count3.json": client.post("/generate/bundle", json={"records": records, "seed": seed}).get_json(),
    }

for name, payload in payloads.items():
    Path(output_dir / name).write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
PY
```

## Determinism tripwires

- Keep `DatasetSettings.generation_timestamp` and `DatasetSettings.random_seed` unchanged when regenerating.
- Endpoints should be called with the explicit `seed` and `records` shown above to avoid any randomness.
- Timestamps and UUIDs are already seeded/fixed; if an unexpected timestamp appears, regenerate after verifying the seed is set to `20240601`.
