from __future__ import annotations

from io import StringIO

from rich.console import Console

from enterprise_synthetic_data_hub.cli import demo as demo_cli


def test_demo_cli_parser_defaults():
    parser = demo_cli.build_parser()
    args = parser.parse_args([])
    assert args.records is None
    assert args.preview == 2
    assert args.use_api is False


def test_demo_cli_generator_preview_runs():
    console = Console(file=StringIO(), force_terminal=False, color_system=None)
    exit_code = demo_cli.run_demo(["--records", "2", "--preview", "1"], console=console)
    assert exit_code == 0
    output = console.file.getvalue()
    assert "Generator preview" in output
