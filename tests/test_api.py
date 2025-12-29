from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import pytest
from enterprise_synthetic_data_hub.api.app import create_app


@pytest.fixture()
def client():
    application = create_app()
    application.testing = True
    with application.test_client() as client:
        yield client


def test_healthz_exposes_version(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ok"
    assert payload["dataset_version"]


def test_generate_person_endpoint(client):
    response = client.post("/generate/person", json={"records": 2, "randomize": True})
    assert response.status_code == 200
    payload = response.get_json()
    assert len(payload["persons"]) == 2
    assert payload["metadata"]["record_count_persons"] == 2
