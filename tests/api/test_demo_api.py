from __future__ import annotations

import pytest

from enterprise_synthetic_data_hub.api.app import create_app
from enterprise_synthetic_data_hub.config.settings import settings


@pytest.fixture()
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


def test_healthz_returns_plan(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ok"
    assert payload["plan"]


def test_generate_person_payload(client):
    response = client.post("/generate/person", json={"records": 3, "seed": 123})
    assert response.status_code == 200
    payload = response.get_json()
    assert len(payload["persons"]) == 3
    assert payload["records_requested"] == 3
    assert payload["persons"][0]["synthetic_source"] == settings.synthetic_marker


def test_generate_bundle_includes_profiles(client):
    response = client.post("/generate/bundle", json={"records": 2})
    assert response.status_code == 200
    payload = response.get_json()
    assert len(payload["profiles"]) == 2
    assert payload["metadata"]["record_count_profiles"] == 2
    assert payload["profiles"][0]["synthetic_source"] == settings.synthetic_marker
