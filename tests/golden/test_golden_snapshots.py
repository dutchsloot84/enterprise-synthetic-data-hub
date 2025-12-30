from __future__ import annotations

from pathlib import Path

import pytest

from enterprise_synthetic_data_hub.api.app import create_app
from enterprise_synthetic_data_hub.config.settings import settings
from tests.utils import load_json, normalize_json

GOLDEN_DIR = Path(__file__).resolve().parent
SEED = settings.random_seed
RECORDS = 3


@pytest.fixture()
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


def _compare(endpoint: str, *, request_payload: dict | None, golden_name: str, client) -> None:
    if request_payload is None:
        response = client.get(endpoint)
    else:
        response = client.post(endpoint, json=request_payload)
    assert response.status_code == 200, response.data
    assert response.content_type.startswith("application/json")
    actual = response.get_json()
    expected = load_json(GOLDEN_DIR / golden_name)

    assert normalize_json(actual) == normalize_json(expected)


@pytest.mark.smoke
@pytest.mark.demo
def test_healthz_matches_golden(client):
    _compare("/healthz", request_payload=None, golden_name="healthz_seed20240601.json", client=client)


@pytest.mark.smoke
@pytest.mark.demo
@pytest.mark.parametrize(
    ("endpoint", "golden_file"),
    [
        ("/generate/person", "person_seed20240601_count3.json"),
        ("/generate/vehicle", "vehicle_seed20240601_count3.json"),
        ("/generate/profile", "profile_seed20240601_count3.json"),
        ("/generate/bundle", "bundle_seed20240601_count3.json"),
    ],
)
def test_generate_matches_golden(client, endpoint: str, golden_file: str):
    payload = {"records": RECORDS, "seed": SEED}
    _compare(endpoint, request_payload=payload, golden_name=golden_file, client=client)
