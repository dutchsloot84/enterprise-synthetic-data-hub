"""API validator ensuring routes and metadata remain healthy."""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from flask.testing import FlaskClient  # type: ignore

try:
    from api.api_server import API_VERSION, app
except Exception as exc:  # pragma: no cover - import guard
    print(json.dumps({"status": "error", "error": str(exc)}))
    raise SystemExit(1)


def main() -> int:
    client: FlaskClient = app.test_client()
    response = client.get(f"/{API_VERSION}/validator")
    status = 0 if response.status_code in (200, 503) else 1
    payload = response.get_json(silent=True) or {}

    search_response = client.get(f"/{API_VERSION}/person/search?age_min=abc")
    if search_response.status_code not in (400, 503):
        status = 1
    search_payload = search_response.get_json(silent=True) or {}

    result = {
        "status": "ok" if status == 0 else "error",
        "validator_status": response.status_code,
        "validator_version": payload.get("version"),
        "record_count": payload.get("record_count"),
        "search_status": search_response.status_code,
        "search_error": search_payload.get("error"),
    }
    print(json.dumps(result, indent=2))
    return status


# Usage:
#   python agentic/validators/api_validator.py
if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
