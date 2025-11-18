"""Compatibility shim that now exposes the governed generator API."""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from enterprise_synthetic_data_hub.api.app import app, create_app

__all__ = ["app", "create_app"]


def main() -> None:  # pragma: no cover - delegated entry point
    app.run(debug=True)


if __name__ == "__main__":  # pragma: no cover
    main()
