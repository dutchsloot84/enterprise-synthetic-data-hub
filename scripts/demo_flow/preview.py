"""API + CLI preview helpers used by the demo flow."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import List

import requests

from enterprise_synthetic_data_hub.config import demo_profiles

REPO_ROOT = Path(__file__).resolve().parents[2]


def call_health(base_url: str, endpoint: str) -> dict:
    response = requests.get(f"{base_url.rstrip('/')}{endpoint}", timeout=10)
    response.raise_for_status()
    return response.json()


def preview_profiles_via_api(base_url: str, profile: demo_profiles.DemoProfile) -> List[dict]:
    payload = {
        "records": profile.records_profile,
        "seed": profile.seed,
        "randomize": profile.randomize,
    }
    response = requests.post(f"{base_url.rstrip('/')}/generate/profile", json=payload, timeout=10)
    response.raise_for_status()
    return response.json().get("profiles", [])


def cli_preview(base_url: str, profile: demo_profiles.DemoProfile) -> None:
    cmd = [
        sys.executable,
        str(REPO_ROOT / "scripts" / "demo_data.py"),
        "--profile",
        profile.name,
        "--use-api",
        "--api-url",
        base_url,
        "--records",
        str(profile.records_profile),
        "--preview",
        "1",
    ]
    subprocess.run(cmd, check=True, cwd=REPO_ROOT)


__all__ = ["call_health", "preview_profiles_via_api", "cli_preview"]
