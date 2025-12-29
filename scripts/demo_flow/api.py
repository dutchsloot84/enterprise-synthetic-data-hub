"""Shell helpers that start/stop the Flask demo API."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Tuple

from enterprise_synthetic_data_hub.config import demo_profiles

REPO_ROOT = Path(__file__).resolve().parents[1]
PORT_FILE = REPO_ROOT / ".demo_api_port"


def start_api(profile: demo_profiles.DemoProfile) -> Tuple[str, str]:
    """Start the Flask API via the shell helper and return its base URL + port."""

    env = os.environ.copy()
    env.setdefault("DEMO_PROFILE", profile.name)
    subprocess.run(
        ["bash", str(REPO_ROOT / "scripts" / "demo_start_api.sh")],
        check=True,
        cwd=REPO_ROOT,
        env=env,
    )
    if not PORT_FILE.exists():
        raise RuntimeError("demo_start_api.sh did not record the port")
    port = PORT_FILE.read_text(encoding="utf-8").strip()
    api_settings = demo_profiles.get_api_settings()
    base_url = f"http://{api_settings.host}:{port}"
    return base_url, port


def stop_api() -> None:
    """Stop the Flask API if it is running."""

    subprocess.run(["bash", str(REPO_ROOT / "scripts" / "demo_stop_api.sh")], cwd=REPO_ROOT)


__all__ = ["start_api", "stop_api", "PORT_FILE"]
