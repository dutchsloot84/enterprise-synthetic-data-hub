from __future__ import annotations

from types import SimpleNamespace

from scripts.demo_flow import preview
from src.enterprise_synthetic_data_hub.config.demo_profiles import DemoProfile


def test_cli_preview_uses_repo_root(monkeypatch):
    calls: list[tuple[list[str], str]] = []

    def fake_run(cmd, check, cwd):
        calls.append((cmd, cwd))
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(preview.subprocess, "run", fake_run)

    profile = DemoProfile(
        name="baseline",
        records_person=1,
        records_vehicle=1,
        records_profile=2,
        seed=None,
        randomize=False,
    )

    preview.cli_preview("http://example.com", profile)

    assert len(calls) == 1
    cmd, cwd = calls[0]
    expected_path = preview.REPO_ROOT / "scripts" / "demo_data.py"
    assert cmd[1] == str(expected_path)
    assert "scripts/scripts" not in cmd[1]
    assert cwd == preview.REPO_ROOT
    assert expected_path.exists()
