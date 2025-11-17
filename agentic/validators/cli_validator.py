"""CLI validator ensuring snapshot command writes the expected stub artifact."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from enterprise_synthetic_data_hub.cli.main import main as cli_main  # noqa: E402


def main() -> int:
    errors: list[str] = []
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_dir = Path(tmp_dir)
        exit_code = cli_main(["generate-snapshot", "--output-dir", str(output_dir)])
        if exit_code != 0:
            errors.append("CLI returned non-zero exit status")
        note_path = output_dir / "README_EXPORT_PENDING.md"
        if not note_path.exists():
            errors.append("Exporter placeholder README missing after CLI run")
        else:
            content = note_path.read_text(encoding="utf-8")
            if "Snapshot export not implemented" not in content:
                errors.append("Exporter placeholder README content unexpected")

    summary = {
        "status": "error" if errors else "ok",
        "errors": errors,
    }
    print(json.dumps(summary, indent=2))
    return 1 if errors else 0


# Usage:
#   python agentic/validators/cli_validator.py
if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
