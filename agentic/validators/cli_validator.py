"""CLI validator ensuring snapshot command writes governed snapshot artifacts."""
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
from enterprise_synthetic_data_hub.config.settings import settings  # noqa: E402


def main() -> int:
    errors: list[str] = []
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_dir = Path(tmp_dir)
        exit_code = cli_main(["generate-snapshot", "--output-dir", str(output_dir), "--records", "5", "--seed", "777"])
        if exit_code != 0:
            errors.append("CLI returned non-zero exit status")
        version_slug = settings.dataset_version.replace(".", "_")
        expected_files = {
            "persons_csv": output_dir / f"persons_{version_slug}.csv",
            "vehicles_csv": output_dir / f"vehicles_{version_slug}.csv",
            "dataset_json": output_dir / f"dataset_{version_slug}.json",
            "metadata_json": output_dir / f"metadata_{version_slug}.json",
            "manifest_json": output_dir / f"snapshot_manifest_{version_slug}.json",
            "readme": output_dir / f"README_SNAPSHOT_{version_slug.upper()}.md",
        }
        for label, path in expected_files.items():
            if not path.exists():
                errors.append(f"Missing {label} after CLI execution")

        manifest_path = expected_files["manifest_json"]
        if manifest_path.exists():
            payload = json.loads(manifest_path.read_text(encoding="utf-8"))
            persons = payload.get("record_counts", {}).get("persons")
            vehicles = payload.get("record_counts", {}).get("vehicles")
            if persons != vehicles:
                errors.append("Manifest person/vehicle counts should match")
            if persons != 5:
                errors.append("CLI --records flag did not propagate to exporter")

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
