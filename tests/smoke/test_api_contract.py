from __future__ import annotations

import pytest

from enterprise_synthetic_data_hub.api.app import create_app
from enterprise_synthetic_data_hub.config.settings import settings
from tests.utils import normalize_json


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
    assert response.status_code == 200, response.data
    assert response.content_type.startswith("application/json")
    payload = response.get_json()
    required_keys = {"status", "dataset_version", "default_seed", "target_records", "version", "seed", "plan"}
    assert required_keys.issubset(payload.keys())
    assert payload["status"] == "ok"
    assert isinstance(payload["version"], str)
    assert isinstance(payload["seed"], (int, str))
    assert payload["version"] == settings.dataset_version
    assert payload["dataset_version"] == settings.dataset_version
    assert payload["default_seed"] == settings.random_seed
    assert payload["target_records"] == settings.target_person_records

    plan = payload["plan"]
    assert isinstance(plan, (dict, str))
    if isinstance(plan, dict):
        assert "steps" in plan
        assert isinstance(plan["steps"], list)
        assert all(isinstance(step, str) for step in plan["steps"])


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
    requested = 2
    response = client.post(endpoint, json={"records": requested, "seed": settings.random_seed})
    assert response.status_code == 200, response.data
    assert response.content_type.startswith("application/json")
    payload = response.get_json()

    if entity_key:
        records = payload[entity_key]
        assert len(records) == requested
        assert all(record.get("synthetic_source") == settings.synthetic_marker for record in records)
        id_keys = [key for key in records[0].keys() if key.endswith("_id")]
        assert id_keys
        for record in records:
            for key in id_keys:
                assert record.get(key)
    else:
        assert len(payload["persons"]) == requested
        assert len(payload["vehicles"]) == requested
        assert len(payload["profiles"]) == requested
        assert payload["persons"][0]["synthetic_source"] == settings.synthetic_marker

        person_ids = {person["person_id"] for person in payload["persons"]}
        vehicle_person_ids = {vehicle["person_id"] for vehicle in payload["vehicles"]}
        assert vehicle_person_ids == person_ids

        profile_person_ids = {profile["person_id"] for profile in payload["profiles"]}
        profile_vehicle_ids = {profile["vehicle_id"] for profile in payload["profiles"]}
        vehicle_ids = {vehicle["vehicle_id"] for vehicle in payload["vehicles"]}
        assert profile_person_ids == person_ids
        assert profile_vehicle_ids == vehicle_ids

    assert payload["seed"] == settings.random_seed
    assert payload["records_requested"] == requested
    assert payload["metadata"]["record_count_persons"] == requested
    assert payload["metadata"]["record_count_vehicles"] == requested
    assert payload["metadata"]["record_count_profiles"] == requested

    if entity_key:
        assert payload["record_count"] == requested


@pytest.mark.smoke
@pytest.mark.demo
def test_generate_rejects_invalid_records(client):
    response = client.post("/generate/person", json={"records": 0, "seed": "abc"})
    assert response.status_code == 400
    assert response.content_type.startswith("application/json")
    payload = response.get_json()
    normalized = normalize_json(payload)
    assert normalized == {
        "error": {
            "code": "invalid_request",
            "message": "'records' must be a positive integer",
        }
    }
