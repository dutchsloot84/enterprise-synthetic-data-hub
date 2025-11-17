"""Flask API server aligned with the agentic workflow."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
from flask import Flask, jsonify, request

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

API_VERSION = "v0.1"
DATA_PATH = REPO_ROOT / "data" / "snapshots" / API_VERSION / "persons_v0_1.csv"
REQUIRED_COLUMNS = {
    "Global_ID",
    "First_Name",
    "Last_Name",
    "Age",
    "Risk_Rating",
    "LOB_Type",
}

try:  # pragma: no cover - fallback when running validators only
    from generator.synthetic_generator_v01 import generate_person_vehicle_dataset
except Exception:  # pragma: no cover
    generate_person_vehicle_dataset = None

app = Flask(__name__)


def _validate_snapshot_frame(frame: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(frame.columns)
    if missing:
        raise ValueError(f"Snapshot is missing required columns: {sorted(missing)}")
    frame["Age"] = pd.to_numeric(frame["Age"], errors="coerce")
    if frame["Age"].isna().any():
        raise ValueError("Age column must contain only numeric values")


def _fallback_dataframe() -> pd.DataFrame:
    if generate_person_vehicle_dataset is None:
        raise FileNotFoundError(str(DATA_PATH))
    persons, _ = generate_person_vehicle_dataset(num_records=50, seed=99)
    rows = []
    for record in persons:
        dob = record["date_of_birth"]
        age = 2024 - int(dob.split("-")[0])
        rows.append(
            {
                "Global_ID": record["person_id"],
                "First_Name": record["first_name"],
                "Last_Name": record["last_name"],
                "Age": age,
                "Risk_Rating": "Medium",
                "LOB_Type": record["lob_type"],
            }
        )
    frame = pd.DataFrame(rows)
    frame.set_index("Global_ID", inplace=True)
    return frame


def _load_person_snapshot() -> tuple[Optional[pd.DataFrame], List[Dict[str, Any]], Optional[str]]:
    try:
        dataframe = pd.read_csv(DATA_PATH)
        _validate_snapshot_frame(dataframe)
        dataframe = dataframe.set_index("Global_ID")
        records = dataframe.reset_index().to_dict("records")
        return dataframe, records, None
    except FileNotFoundError:
        try:
            dataframe = _fallback_dataframe()
            records = dataframe.reset_index().to_dict("records")
            return dataframe, records, "Loaded fallback dataset"
        except Exception as exc:
            return None, [], str(exc)
    except ValueError as exc:
        return None, [], str(exc)


PERSON_DATA, PERSON_RECORDS, SNAPSHOT_ERROR = _load_person_snapshot()


@app.get(f"/{API_VERSION}/person/<string:global_id>")
def get_person(global_id: str):
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
    validation = validate_snapshot_loaded()
    status_code = 200 if validation["data_available"] else 503
    return jsonify(validation), status_code


def validate_snapshot_loaded() -> Dict[str, Any]:
    return {
        "data_available": PERSON_DATA is not None,
        "record_count": 0 if PERSON_DATA is None else int(PERSON_DATA.shape[0]),
        "data_path": str(DATA_PATH),
        "error": SNAPSHOT_ERROR,
        "version": API_VERSION,
        "sample_record": PERSON_RECORDS[0] if PERSON_RECORDS else None,
    }


def main() -> None:  # pragma: no cover
    validation_report = json.dumps(validate_snapshot_loaded(), indent=2)
    app.logger.info("Snapshot validation: %s", validation_report)
    app.run(debug=True)


if __name__ == "__main__":  # pragma: no cover
    main()
