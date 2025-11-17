from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import pytest
from api.api_server import API_VERSION, app


def test_validator_endpoint_returns_status():
    client = app.test_client()
    response = client.get(f"/{API_VERSION}/validator")
    assert response.status_code in (200, 503)
    payload = response.get_json()
    assert payload["version"] == API_VERSION


def test_search_endpoint_handles_params():
    client = app.test_client()
    response = client.get(f"/{API_VERSION}/person/search?age_min=10&age_max=90")
    assert response.status_code in (200, 503)


def test_search_endpoint_rejects_invalid_age():
    client = app.test_client()
    response = client.get(f"/{API_VERSION}/person/search?age_min=invalid")
    if response.status_code == 503:
        pytest.skip("Snapshot unavailable; invalid query branch not executed")
    assert response.status_code == 400
    payload = response.get_json()
    assert "age_min" in payload["error"]
