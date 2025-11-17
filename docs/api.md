# Local API Layer (v0.1)

The v0.1 Synthetic Data POC now exposes a lightweight Flask server that reads the
static snapshot stored under `data/snapshots/v0.1/`. The API provides read-only
access to the person dataset and is intended for local use only.

## Prerequisites

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
# or install only the API deps
pip install -r requirements.txt
```

## Run the server

```bash
python api_server.py
```

The app starts in debug mode and logs whether the CSV snapshot was validated
successfully. Hot reload is provided by Flask's debug server.

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
- Returns an empty list when no records match.

### `GET /v0.1/validator`
- Returns the validation result for the currently loaded CSV snapshot,
  including file path and record counts. Useful for local smoke tests and to
  confirm the dataset was located properly.

## Data contract

The API reads from `data/snapshots/v0.1/persons_v0_1.csv`.
Required columns: `Global_ID`, `First_Name`, `Last_Name`, `Age`, `Risk_Rating`,
`LOB_Type`, `City`, `State`, `Postal_Code`.
