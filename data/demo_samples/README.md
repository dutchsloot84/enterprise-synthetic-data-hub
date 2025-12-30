# Demo Sample Refresh Guide

## Canonical fallback set
- **Folder:** `data/demo_samples/phase1/`
- **Purpose:** Small, deterministic JSON payloads used when the live demo path is unavailable.
- **Shape:** 3 records per entity, seeded with `20240601` (matches `DatasetSettings.random_seed`).

## Deterministic regeneration (existing script)
Run the existing API-backed helper to rewrite the fallback artifacts in place:

```bash
PYTHONPATH=src python - <<'PY'
import json
from pathlib import Path
from enterprise_synthetic_data_hub.api.app import create_app
from enterprise_synthetic_data_hub.config.settings import settings

seed = settings.random_seed  # 20240601
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

This uses the existing Flask test client and seeded settings to ensure deterministic output and stable filenames.

## Expected artifacts
- `data/demo_samples/phase1/persons_seed_20240601.json` – 3 persons
- `data/demo_samples/phase1/vehicles_seed_20240601.json` – 3 vehicles
- `data/demo_samples/phase1/profiles_seed_20240601.json` – 3 profiles
- `data/demo_samples/phase1/bundle_seed_20240601.json` – 3 persons, 3 vehicles, 3 profiles
- Reference-only curated set for slides: `data/demo_samples/v0.1/` (`persons_sample.json`, `vehicles_sample.json`, `profiles_sample.json`, `bundle_sample.json`; 5 records each, seeded as recorded in `bundle_sample.json` metadata).

## Quick verification
- `make demo-validate` – runs schema + synthetic marker checks against generator output.
- `rg "enterprise-synthetic-data-hub v0.1" data/demo_samples/phase1/*.json` – spot-check the synthetic marker on the canned payloads.

## Reminder
These canned artifacts are **demo fallbacks**, not production distributions. Prefer live generation when available; keep filenames and seeds stable to avoid demo drift.
