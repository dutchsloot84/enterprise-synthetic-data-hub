from __future__ import annotations

import pytest

from enterprise_synthetic_data_hub.api.app import create_app
from enterprise_synthetic_data_hub.cli import demo as demo_cli
from rich.console import Console
from io import StringIO


@pytest.mark.smoke
@pytest.mark.demo
def test_api_profile_endpoint_smoke():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        response = client.post("/generate/profile", json={"records": 2, "seed": 5})
        assert response.status_code == 200
        payload = response.get_json()
        assert len(payload["profiles"]) == 2


@pytest.mark.smoke
@pytest.mark.demo
def test_demo_cli_bundle_preview_smoke():
    console = Console(file=StringIO(), force_terminal=False, color_system=None)
    exit_code = demo_cli.run_demo(["--profile", "baseline", "--records", "2", "--preview", "1"], console=console)
    assert exit_code == 0
