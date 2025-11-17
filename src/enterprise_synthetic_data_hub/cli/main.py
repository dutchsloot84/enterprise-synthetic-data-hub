"""Command-line entrypoint stub for snapshot workflows."""
from __future__ import annotations

import argparse
import secrets
from pathlib import Path

from enterprise_synthetic_data_hub.generation.generator import generate_snapshot_bundle
from enterprise_synthetic_data_hub.io.exporters import export_snapshot_bundle


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Enterprise Synthetic Data Hub CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    snapshot_parser = subparsers.add_parser(
        "generate-snapshot", help="Generate the deterministic POC snapshot artifacts."
    )
    snapshot_parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/snapshots/v0.1"),
        help="Directory where the snapshot should be written.",
    )
    snapshot_parser.add_argument(
        "--records",
        type=int,
        default=None,
        help="Override default person/vehicle record count.",
    )
    snapshot_parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Override the default deterministic seed.",
    )
    snapshot_parser.add_argument(
        "--randomize",
        action="store_true",
        help="Use a random seed for exploratory sample generation.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "generate-snapshot":
        seed = args.seed
        if args.randomize:
            seed = secrets.randbelow(1_000_000_000)
        bundle = generate_snapshot_bundle(num_records=args.records, seed=seed)
        artifacts = export_snapshot_bundle(bundle, args.output_dir)
        print("Snapshot generation completed. Files written:")
        for label, path in artifacts.items():
            print(f"- {label}: {path}")
        print(
            "Record counts — persons: {persons} vehicles: {vehicles} profiles: {profiles}".format(
                persons=bundle.metadata.record_count_persons,
                vehicles=bundle.metadata.record_count_vehicles,
                profiles=bundle.metadata.record_count_profiles,
            )
        )
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
