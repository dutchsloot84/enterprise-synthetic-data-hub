#!/usr/bin/env python
"""Story-driven orchestration for the make demo target."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import requests

from enterprise_synthetic_data_hub.config import demo_profiles
from enterprise_synthetic_data_hub.config.settings import settings

REPO_ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_ROOT = REPO_ROOT / "data" / "demo_runs"
MANIFEST_TEMPLATE = "snapshot_manifest_{slug}.json"


def _step(label: str) -> None:
    print(f"[ {label} ]")


def _run(cmd: list[str], **kwargs) -> None:
    print(f"$ {' '.join(cmd)}")
    subprocess.run(cmd, check=True, **kwargs)


def _generate_snapshot(profile: demo_profiles.DemoProfile) -> tuple[Path, dict]:
    SNAPSHOT_ROOT.mkdir(parents=True, exist_ok=True)
    output_dir = SNAPSHOT_ROOT / profile.name
    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        "-m",
        "enterprise_synthetic_data_hub.cli.main",
        "generate-snapshot",
        "--output-dir",
        str(output_dir),
        "--records",
        str(profile.records_person),
    ]
    if profile.randomize:
        cmd.append("--randomize")
    elif profile.seed is not None:
        cmd.extend(["--seed", str(profile.seed)])
    _run(cmd, cwd=REPO_ROOT)
    version_slug = settings.dataset_version.replace(".", "_")
    manifest_path = output_dir / MANIFEST_TEMPLATE.format(slug=version_slug)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    return output_dir, manifest


def _start_api(profile: demo_profiles.DemoProfile) -> tuple[str, Path]:
    env = os.environ.copy()
    env.setdefault("DEMO_PROFILE", profile.name)
    _run(["bash", str(REPO_ROOT / "scripts" / "demo_start_api.sh")], env=env)
    port_file = REPO_ROOT / ".demo_api_port"
    if not port_file.exists():
        raise RuntimeError("demo_start_api.sh did not record the port")
    port = port_file.read_text(encoding="utf-8").strip()
    api_settings = demo_profiles.get_api_settings()
    host = api_settings.host
    base_url = f"http://{host}:{port}"
    return base_url, port_file


def _call_health(base_url: str, endpoint: str) -> dict:
    response = requests.get(f"{base_url.rstrip('/')}{endpoint}", timeout=10)
    response.raise_for_status()
    return response.json()


def _preview_profiles_via_api(base_url: str, profile: demo_profiles.DemoProfile) -> list[dict]:
    payload = {
        "records": profile.records_profile,
        "seed": profile.seed,
        "randomize": profile.randomize,
    }
    response = requests.post(f"{base_url.rstrip('/')}/generate/profile", json=payload, timeout=10)
    response.raise_for_status()
    return response.json().get("profiles", [])


def _cli_preview(base_url: str, profile: demo_profiles.DemoProfile) -> None:
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
    _run(cmd, cwd=REPO_ROOT)


def _run_smoke_tests() -> None:
    _run(["pytest", "-m", "demo"], cwd=REPO_ROOT)


def orchestrate(profile_name: str, skip_smoke: bool) -> None:
    profile = demo_profiles.get_demo_profile(profile_name)
    api_settings = demo_profiles.get_api_settings()
    try:
        _step("STEP 1/5 Generate governed snapshot")
        snapshot_dir, manifest = _generate_snapshot(profile)
        _step("STEP 2/5 Start Flask API")
        base_url, port_file = _start_api(profile)
        _step("STEP 3/5 Health check")
        health = _call_health(base_url, api_settings.health_endpoint)
        print(json.dumps(health, indent=2))
        _step("STEP 4/5 Preview data via API + CLI")
        profiles = _preview_profiles_via_api(base_url, profile)
        print(json.dumps(profiles[:1], indent=2))
        _cli_preview(base_url, profile)
        if not skip_smoke:
            _step("STEP 5/5 Demo smoke tests")
            _run_smoke_tests()
        else:
            _step("STEP 5/5 Demo smoke tests (skipped)")
        print("\n===== Demo Summary =====")
        print(f"Profile: {profile.name}")
        print(f"Snapshot location: {snapshot_dir}")
        print(f"API URL: {base_url}")
        counts = manifest.get("record_counts", {})
        print(
            "Counts — persons: {p} vehicles: {v} profiles: {r}".format(
                p=counts.get("persons"),
                v=counts.get("vehicles"),
                r=counts.get("profiles"),
            )
        )
        print("Curated demo bundles: data/demo_samples/v0.1/")
        print(f"Synthetic marker: {settings.synthetic_marker}")
    finally:
        _run(["bash", str(REPO_ROOT / "scripts" / "demo_stop_api.sh")], cwd=REPO_ROOT)


def main() -> int:
    parser = argparse.ArgumentParser(description="End-to-end demo orchestrator")
    parser.add_argument("--profile", default=None, help="Demo profile name (default: baseline)")
    parser.add_argument("--skip-smoke", action="store_true", help="Skip pytest -m demo")
    args = parser.parse_args()
    orchestrate(demo_profiles.get_profile_name(args.profile), args.skip_smoke)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
