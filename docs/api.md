# Demo API – Generator-backed Flask App
Version: 0.1.1
Last Updated: 2024-06-09

The demo API now lives in `src/enterprise_synthetic_data_hub/api/app.py` and exposes
the governed generator directly. It no longer depends on CSV fallbacks and instead
produces JSON payloads aligned with the Person, Vehicle, Profile, and metadata
schemas.

## Run the server
```bash
export FLASK_APP=enterprise_synthetic_data_hub.api.app:app
flask run  # defaults to http://127.0.0.1:5000
```

Set `PYTHONPATH=src` if you are running outside of `make demo`. The factory
function `create_app()` is used by the CLI tests, `scripts/demo_start_api.sh`, and
`make demo` so the API stays lightweight.

## Endpoints
- `GET /healthz`
  - Returns dataset version, default seed, target record count, and the current generation plan.
- `POST /generate/person`
- `POST /generate/vehicle`
- `POST /generate/profile`
  - Body (optional): `{"records": <int>, "seed": <int>, "randomize": <bool>}`
  - Defaults: 5 records, deterministic seed from settings.
  - Returns metadata + the requested entity array and reports the effective seed.
- `POST /generate/bundle`
  - Returns metadata plus persons, vehicles, and profiles in one payload.

All endpoints share the same validation rules: `records` must be positive and
`seed` must be an integer or the string `"random"`. When `randomize` (or
`seed="random"`) is provided, the server generates a random seed but still
reports it in the response for reproducibility.

## Demo Automation
Running `make demo` automatically launches the Flask API via
`scripts/demo_start_api.sh`, performs a `/healthz` check, hits
`/generate/person`, and then triggers the colorful CLI preview that calls
`/generate/bundle`. Review that script if you need to adapt the workflow for CI.

## Testing
`tests/api/test_demo_api.py` exercises `/healthz`, `/generate/person`, and
`/generate/bundle` using Flask’s test client. Additional smoke coverage lives in
`tests/smoke/test_demo_flow.py`.
