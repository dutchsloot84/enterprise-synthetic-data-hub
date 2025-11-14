"""Command-line entrypoint stub for snapshot workflows."""
from __future__ import annotations

import argparse
from pathlib import Path

from enterprise_synthetic_data_hub.generation.generator import generate_snapshot_stub
from enterprise_synthetic_data_hub.io.exporters import export_snapshot_stub


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Enterprise Synthetic Data Hub CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    snapshot_parser = subparsers.add_parser(
        "generate-snapshot", help="Generate the deterministic POC snapshot (stub)."
    )
    snapshot_parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/snapshots/v0.1"),
        help="Directory where the snapshot should be written.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "generate-snapshot":
        bundle = generate_snapshot_stub()
        export_snapshot_stub(args.output_dir, bundle.persons, bundle.vehicles)
        print("Snapshot generation stub executed. Check output directory for notes.")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
