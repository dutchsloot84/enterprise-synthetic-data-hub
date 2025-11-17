from __future__ import annotations

from io import StringIO

import pytest
from rich.console import Console

from enterprise_synthetic_data_hub.cli import demo as demo_cli


@pytest.mark.smoke
def test_demo_cli_smoke_preview():
    console = Console(file=StringIO(), force_terminal=False, color_system=None)
    exit_code = demo_cli.run_demo(["--records", "1", "--preview", "1"], console=console)
    assert exit_code == 0
    assert "Persons" in console.file.getvalue()
