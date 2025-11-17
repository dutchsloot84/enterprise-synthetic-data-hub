from __future__ import annotations

import json
from pathlib import Path

from enterprise_synthetic_data_hub.cli.main import build_parser, main
from enterprise_synthetic_data_hub.config.settings import settings


def test_cli_parser_supports_generate_snapshot():
    parser = build_parser()
    args = parser.parse_args([
        "generate-snapshot",
        "--output-dir",
        "data/snapshots/v0.1",
        "--records",
        "10",
        "--seed",
        "123",
    ])
    assert args.command == "generate-snapshot"
    assert args.records == 10
    assert args.seed == 123


def test_cli_main_writes_snapshot(tmp_path):
    exit_code = main(
        [
            "generate-snapshot",
            "--output-dir",
            str(tmp_path),
            "--records",
            "5",
            "--seed",
            "456",
        ]
    )
    assert exit_code == 0
    version_slug = settings.dataset_version.replace(".", "_")
    manifest_path = tmp_path / f"snapshot_manifest_{version_slug}.json"
    assert manifest_path.exists()
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert payload["record_counts"]["persons"] == 5
    assert payload["record_counts"]["vehicles"] == 5
    persons_csv = tmp_path / f"persons_{version_slug}.csv"
    vehicles_csv = tmp_path / f"vehicles_{version_slug}.csv"
    assert persons_csv.exists()
    assert vehicles_csv.exists()
    assert Path(payload["files"]["persons_csv"]).name == persons_csv.name
