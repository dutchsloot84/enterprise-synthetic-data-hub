from __future__ import annotations

from enterprise_synthetic_data_hub.cli.main import build_parser, main


def test_cli_parser_supports_generate_snapshot():
    parser = build_parser()
    args = parser.parse_args(["generate-snapshot"])
    assert args.command == "generate-snapshot"


def test_cli_main_writes_placeholder(tmp_path):
    exit_code = main(["generate-snapshot", "--output-dir", str(tmp_path)])
    assert exit_code == 0
    readme = tmp_path / "README_EXPORT_PENDING.md"
    assert readme.exists()
    assert "Snapshot export not implemented yet" in readme.read_text(encoding="utf-8")
