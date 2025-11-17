"""Local Flask API server for the Synthetic Data POC (v0.1)."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
from flask import Flask, jsonify, request

# Ensure the internal package is importable when running `python api_server.py`
ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
if SRC_DIR.exists() and str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

try:
    from enterprise_synthetic_data_hub.config.settings import settings as project_settings
except Exception:  # pragma: no cover - fallback when package isn't installed
    project_settings = None

API_VERSION = getattr(project_settings, "dataset_version", "v0.1")
DATA_PATH = ROOT_DIR / "data" / "snapshots" / API_VERSION / "persons_v0_1.csv"
REQUIRED_COLUMNS = {
    "Global_ID",
    "First_Name",
    "Last_Name",
    "Age",
    "Risk_Rating",
    "LOB_Type",
}

app = Flask(__name__)


def _validate_snapshot_frame(frame: pd.DataFrame) -> None:
    """Validate minimum columns and datatypes for the loaded snapshot."""
    missing = REQUIRED_COLUMNS - set(frame.columns)
    if missing:
        raise ValueError(f"Snapshot is missing required columns: {sorted(missing)}")

    frame["Age"] = pd.to_numeric(frame["Age"], errors="coerce")
    if frame["Age"].isna().any():
        raise ValueError("Age column must contain only numeric values")


def _load_person_snapshot() -> tuple[Optional[pd.DataFrame], List[Dict[str, Any]], Optional[str]]:
    try:
        dataframe = pd.read_csv(DATA_PATH)
        _validate_snapshot_frame(dataframe)
        dataframe = dataframe.set_index("Global_ID")
        records = dataframe.reset_index().to_dict("records")
        return dataframe, records, None
    except FileNotFoundError:
        return None, [], f"Snapshot file not found at {DATA_PATH}"
    except ValueError as exc:
        return None, [], str(exc)


PERSON_DATA, PERSON_RECORDS, SNAPSHOT_ERROR = _load_person_snapshot()


@app.get(f"/{API_VERSION}/person/<string:global_id>")
def get_person(global_id: str):
    """Return a single person record if present."""
    if PERSON_DATA is None:
        return jsonify({"error": SNAPSHOT_ERROR or "Person snapshot unavailable"}), 503

    try:
        record = PERSON_DATA.loc[global_id]
    except KeyError:
        return jsonify({"error": f"Person with Global_ID '{global_id}' not found"}), 404

    data = record.to_dict()
    data["Global_ID"] = global_id
    return jsonify(data)


def _parse_int(value: Optional[str], field_name: str) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError(f"Query parameter '{field_name}' must be an integer") from None


@app.get(f"/{API_VERSION}/person/search")
def search_person():
    """Filter person records based on query parameters."""
    if PERSON_DATA is None:
        return jsonify({"error": SNAPSHOT_ERROR or "Person snapshot unavailable"}), 503

    try:
        age_min = _parse_int(request.args.get("age_min"), "age_min")
        age_max = _parse_int(request.args.get("age_max"), "age_max")
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    risk_rating = request.args.get("risk_rating")

    df = PERSON_DATA.copy()
    if age_min is not None:
        df = df[df["Age"] >= age_min]
    if age_max is not None:
        df = df[df["Age"] <= age_max]
    if risk_rating:
        df = df[df["Risk_Rating"].str.lower() == risk_rating.lower()]

    results = df.reset_index().head(10).to_dict("records")
    return jsonify(results)


@app.get(f"/{API_VERSION}/validator")
def validator():
    """Expose snapshot validation results for local smoke checks."""
    validation = validate_snapshot_loaded()
    status_code = 200 if validation["data_available"] else 503
    return jsonify(validation), status_code


def validate_snapshot_loaded() -> Dict[str, Any]:
    """Return validation metadata for the currently loaded snapshot."""
    return {
        "data_available": PERSON_DATA is not None,
        "record_count": 0 if PERSON_DATA is None else int(PERSON_DATA.shape[0]),
        "data_path": str(DATA_PATH),
        "error": SNAPSHOT_ERROR,
        "version": API_VERSION,
        "sample_record": PERSON_RECORDS[0] if PERSON_RECORDS else None,
    }


if __name__ == "__main__":
    validation_report = json.dumps(validate_snapshot_loaded(), indent=2)
    app.logger.info("Snapshot validation: %s", validation_report)
    app.run(debug=True)
