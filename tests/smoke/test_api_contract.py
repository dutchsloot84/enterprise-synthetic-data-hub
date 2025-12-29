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


@pytest.mark.smoke
@pytest.mark.demo
def test_healthz_contract(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ok"
    assert payload["dataset_version"] == settings.dataset_version
    assert payload["default_seed"] == settings.random_seed
    assert payload["target_records"] == settings.target_person_records
    assert isinstance(payload.get("plan"), list)
    assert payload["plan"]


@pytest.mark.smoke
@pytest.mark.demo
@pytest.mark.parametrize(
    ("endpoint", "entity_key"),
    [
        ("/generate/person", "persons"),
        ("/generate/vehicle", "vehicles"),
        ("/generate/profile", "profiles"),
        ("/generate/bundle", None),
    ],
)
def test_generate_contracts_deterministic(client, endpoint, entity_key):
    response = client.post(endpoint, json={"records": 2, "seed": 1234})
    assert response.status_code == 200
    payload = response.get_json()

    if entity_key:
        records = payload[entity_key]
        assert len(records) == 2
        assert records[0]["synthetic_source"] == settings.synthetic_marker
    else:
        assert len(payload["persons"]) == 2
        assert len(payload["vehicles"]) == 2
        assert len(payload["profiles"]) == 2
        assert payload["persons"][0]["synthetic_source"] == settings.synthetic_marker

    assert payload["seed"] == 1234
    assert payload["records_requested"] == 2
    assert payload["metadata"]["record_count_persons"] == 2
    assert payload["metadata"]["record_count_vehicles"] == 2
    assert payload["metadata"]["record_count_profiles"] == 2


@pytest.mark.smoke
@pytest.mark.demo
def test_generate_rejects_invalid_records(client):
    response = client.post("/generate/person", json={"records": 0, "seed": "abc"})
    assert response.status_code == 400
    payload = response.get_json()
    assert "records" in payload["error"]
