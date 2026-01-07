# Demo API – Generator-backed Flask App
Version: 0.1.2
Last Updated: 2026-01-06

The demo API lives in `src/enterprise_synthetic_data_hub/api/app.py` and exposes
the governed generator directly. A compatibility shim remains at
`src/api/api_server.py` for legacy entrypoints. The API returns JSON payloads
aligned with the Person, Vehicle, Profile, and metadata schemas.

## Run the server
```bash
export PYTHONPATH=src
flask --app enterprise_synthetic_data_hub.api.app run --host 127.0.0.1 --port 5000
```

If you are using `make demo` or `scripts/demo_start_api.sh`, the API is started
for you and defaults to the host/port in `config/demo.yaml` (override the port
with `DEMO_API_PORT`).

## Endpoints
- `GET /healthz`
  - Returns dataset version, default seed, target record count, and the current generation plan.
- `POST /generate/person`
- `POST /generate/vehicle`
- `POST /generate/profile`
- `POST /generate/bundle`

### Request body (optional)
```json
{"records": 10, "seed": 123, "randomize": false}
```
- `records` must be a positive integer.
- `seed` must be an integer, a numeric string, or the string "random".
- `randomize` forces a random seed regardless of `seed`.

### Response notes
- All `/generate/*` responses include `metadata`, `records_requested`, and the
  effective `seed` value used to generate the data.
- `/generate/person|vehicle|profile` responses include a single entity list plus
  `record_count`.
- `/generate/bundle` responses include `persons`, `vehicles`, and `profiles` in
  one payload.

## Demo Automation
Running `make demo` launches the Flask API via `scripts/demo_start_api.sh`,
performs a `/healthz` check, hits `/generate/person`, and then triggers the
colorful CLI preview that calls `/generate/bundle`. The end-to-end
test orchestration is implemented in `scripts/run_demo_flow.py`.

## Testing
`tests/api/test_demo_api.py` exercises `/healthz`, `/generate/person`, and
`/generate/bundle` using Flask’s test client. Additional smoke coverage lives in
`tests/smoke/test_demo_flow.py`.
