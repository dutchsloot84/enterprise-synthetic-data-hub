# API Layer – v0.1

The v0.1 Synthetic Data POC exposes a lightweight Flask server defined in
`src/api/api_server.py`. The server reads the static snapshot stored under
`data/snapshots/v0.1/` when available and falls back to the deterministic
generator to guarantee local usability. The API provides read-only access to the
person dataset and is intended for local use only.

## Prerequisites

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the server

```bash
python src/api/api_server.py
# or use the legacy shim
python api_server.py
```

The app starts in debug mode and logs whether the CSV snapshot was validated.
If the snapshot is missing, it automatically populates an in-memory dataset via
`enterprise_synthetic_data_hub.generation.generator.generate_snapshot_bundle` (or the shim in `src/generator/`).

## Endpoints

### `GET /v0.1/person/<global_id>`
- Looks up a single person record by `Global_ID`.
- Returns HTTP 404 if the ID is not present.

### `GET /v0.1/person/search`
- Optional query parameters:
  - `age_min` (integer)
  - `age_max` (integer)
  - `risk_rating` (Low, Medium, High)
- Applies filters and returns up to the first 10 matches.
- Returns HTTP 503 if the snapshot fallback failed to load.

### `GET /v0.1/validator`
- Returns the validation result for the currently loaded CSV snapshot or fallback
  dataset, including file path and record counts.

## Data Contract

- Primary CSV path: `data/snapshots/v0.1/persons_v0_1.csv`
- Fallback source: `enterprise_synthetic_data_hub.generation.generator`
- Required columns: `Global_ID`, `First_Name`, `Last_Name`, `Age`,
  `Risk_Rating`, `LOB_Type`

Refer to `prompts/sub-prompts/06_api_layer.md` for the agentic instructions that
must be followed when editing the API layer.
