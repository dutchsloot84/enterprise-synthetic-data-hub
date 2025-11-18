"""Snapshot orchestration helpers for the guided demo."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Tuple

from enterprise_synthetic_data_hub.config import demo_profiles
from enterprise_synthetic_data_hub.config.settings import settings

REPO_ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_ROOT = REPO_ROOT / "data" / "demo_runs"
LATEST_DEMO_LINK = SNAPSHOT_ROOT / "latest_demo"
MANIFEST_TEMPLATE = "snapshot_manifest_{slug}.json"
MAX_SAVED_RUNS = 5


def _ensure_snapshot_root() -> None:
    SNAPSHOT_ROOT.mkdir(parents=True, exist_ok=True)


def _timestamped_directory(profile: demo_profiles.DemoProfile) -> Path:
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    return SNAPSHOT_ROOT / f"{timestamp}_{profile.name}"


def _promote_latest_symlink(target: Path) -> None:
    try:
        if LATEST_DEMO_LINK.exists() or LATEST_DEMO_LINK.is_symlink():
            if LATEST_DEMO_LINK.is_dir() and not LATEST_DEMO_LINK.is_symlink():
                shutil.rmtree(LATEST_DEMO_LINK)
            else:
                LATEST_DEMO_LINK.unlink()
        LATEST_DEMO_LINK.symlink_to(target, target_is_directory=True)
    except OSError:
        # Windows users without Developer Mode cannot create symlinks.
        fallback = SNAPSHOT_ROOT / "latest_demo.path"
        fallback.write_text(str(target), encoding="utf-8")


def _cleanup_old_runs(limit: int = MAX_SAVED_RUNS) -> None:
    runs = [
        path
        for path in SNAPSHOT_ROOT.iterdir()
        if path.is_dir() and path.name != LATEST_DEMO_LINK.name
    ]
    runs.sort(reverse=True)
    for stale in runs[limit:]:
        shutil.rmtree(stale, ignore_errors=True)


def generate_snapshot(profile: demo_profiles.DemoProfile) -> Tuple[Path, dict]:
    """Generate a governed snapshot via the CLI and manage retention."""

    _ensure_snapshot_root()
    output_dir = _timestamped_directory(profile)
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
    subprocess.run(cmd, check=True, cwd=REPO_ROOT)
    version_slug = settings.dataset_version.replace(".", "_")
    manifest_path = output_dir / MANIFEST_TEMPLATE.format(slug=version_slug)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    _promote_latest_symlink(output_dir)
    _cleanup_old_runs()
    return output_dir, manifest


__all__ = [
    "generate_snapshot",
    "LATEST_DEMO_LINK",
    "SNAPSHOT_ROOT",
]
