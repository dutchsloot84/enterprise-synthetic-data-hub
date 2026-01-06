# API Reference
Flask demo API exposing the governed generator at `src/enterprise_synthetic_data_hub/api/app.py`. All endpoints preserve determinism (default seed **20240601**) and return `synthetic_source` markers.

## Authentication
- Optional API key: set `ESDH_API_KEY` in the environment; clients must send `X-API-Key: <value>` (or `?api_key=` query).
- Without the variable set, endpoints are open for demo/QA.

## Base URL
`http://127.0.0.1:5000`

## Endpoints
### `GET /healthz`
Returns generator status and plan.

Example:
```bash
curl -fsSL http://127.0.0.1:5000/healthz | jq
```
Response excerpt:
```json
{
  "status": "ok",
  "dataset_version": "v0.1",
  "default_seed": 20240601,
  "target_records": 200,
  "plan": {"steps": ["Dataset version: v0.1", "Use deterministic seed for reproducibility.", "Generate Persons first, then attach Vehicles per rules (one-to-one)." ...]}
}
```

### `POST /generate/person`
### `POST /generate/vehicle`
### `POST /generate/profile`
### `POST /generate/bundle`
Request body (all fields optional):
```json
{
  "records": 5,
  "seed": 20240601,
  "randomize": false
}
```
- `records`: positive integer; defaults to 5.
- `seed`: integer; when omitted, defaults to 20240601. Set to `"random"` or `randomize=true` to generate a random seed (returned in payload).
- `randomize`: boolean flag to request a random seed.

Example deterministic bundle:
```bash
curl -fsSL -X POST http://127.0.0.1:5000/generate/bundle \
  -H 'Content-Type: application/json' \
  -d '{"records": 3, "seed": 20240601}' | jq '.seed, .metadata.record_count_profiles'
```
Example randomized Persons subset:
```bash
curl -fsSL -X POST http://127.0.0.1:5000/generate/person \
  -H 'Content-Type: application/json' \
  -d '{"records": 2, "randomize": true}' | jq '{seed: .seed, count: .record_count}'
```

Response shape (bundle):
```json
{
  "metadata": {"dataset_version": "v0.1", "record_count_persons": 3, ...},
  "persons": [...],
  "vehicles": [...],
  "profiles": [...],
  "records_requested": 3,
  "seed": 20240601
}
```

## Errors
- `400 invalid_request`: malformed `records` or `seed` (non-integer, <=0).
- `401 unauthorized`: missing/invalid API key when `ESDH_API_KEY` is set.

## Demo UI
- `GET /demo` serves a lightweight HTML page for manual calls to `/healthz` and `/generate/*` without external tooling.

## Validation Checklist
- `/healthz` reports `default_seed=20240601` and the generation plan.
- `/generate/bundle` returns matching record counts for persons/vehicles/profiles and includes `synthetic_source` on each entity.
- Effective seed in responses should match request or reported random seed; record this when using randomized runs.
