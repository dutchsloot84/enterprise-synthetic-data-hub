from __future__ import annotations

import json
from pathlib import Path

from enterprise_synthetic_data_hub.cli.main import build_parser, main
from enterprise_synthetic_data_hub.config.settings import settings


def test_cli_parser_supports_generate_snapshot():
    parser = build_parser()
    args = parser.parse_args(
        [
            "generate-snapshot",
            "--output-dir",
            "data/snapshots/v0.1",
            "--records",
            "10",
            "--seed",
            "123",
            "--randomize",
            "--entity-filter",
            "persons",
            "vehicles",
            "--output-format",
            "ndjson",
            "csv",
        ]
    )
    assert args.command == "generate-snapshot"
    assert args.records == 10
    assert args.seed == 123
    assert args.randomize is True
    assert args.entity_filter == ["persons", "vehicles"]
    assert "ndjson" in args.output_format


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
    assert payload["record_counts"]["profiles"] == 5
    persons_csv = tmp_path / f"persons_{version_slug}.csv"
    vehicles_csv = tmp_path / f"vehicles_{version_slug}.csv"
    assert persons_csv.exists()
    assert vehicles_csv.exists()
    assert Path(payload["files"]["persons_csv"]).name == persons_csv.name
    assert "checksums" in payload
    assert "stats" in payload
    assert payload["stats"]["persons"]
    assert payload["checksums"]["persons_csv"]


def test_cli_supports_ndjson(tmp_path):
    exit_code = main(
        [
            "generate-snapshot",
            "--output-dir",
            str(tmp_path),
            "--records",
            "3",
            "--output-format",
            "ndjson",
            "csv",
        ]
    )
    assert exit_code == 0
    version_slug = settings.dataset_version.replace(".", "_")
    ndjson_path = tmp_path / f"persons_{version_slug}.ndjson"
    assert ndjson_path.exists()
    lines = ndjson_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 3
