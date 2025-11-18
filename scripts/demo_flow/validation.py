"""Validation helpers for the guided demo flow."""
from __future__ import annotations

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def run_smoke_tests() -> None:
    subprocess.run(["pytest", "-m", "demo"], check=True, cwd=REPO_ROOT)


__all__ = ["run_smoke_tests"]
