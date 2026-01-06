"""Command-line entrypoint stub for snapshot workflows."""
from __future__ import annotations

import argparse
import logging
import secrets
from pathlib import Path
from typing import Iterable

from enterprise_synthetic_data_hub.generation.generator import generate_snapshot_bundle
from enterprise_synthetic_data_hub.io.exporters import export_snapshot_bundle
from enterprise_synthetic_data_hub.config.settings import settings


logger = logging.getLogger(__name__)


def _parse_entity_filter(values: Iterable[str] | None) -> set[str]:
    return set(values or [])


def _should_include_profiles(entity_filter: set[str]) -> bool:
    if not entity_filter:
        return True
    return "profiles" in entity_filter


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
    snapshot_parser.add_argument(
        "--entity-filter",
        nargs="+",
        choices=["persons", "vehicles", "profiles"],
        help="Limit export to specific entities (defaults to all).",
    )
    snapshot_parser.add_argument(
        "--output-format",
        nargs="+",
        choices=["csv", "json", "ndjson", "parquet"],
        help="Additional output formats to persist alongside CSV/JSON.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "generate-snapshot":
        seed = args.seed
        if args.randomize:
            seed = secrets.randbelow(1_000_000_000)
            logger.warning("Randomized seed used for snapshot generation", extra={"seed": seed})
        if seed is None and settings.random_seed:
            logger.info("Using deterministic seed from settings", extra={"seed": settings.random_seed})
        entity_filter = _parse_entity_filter(args.entity_filter)
        output_formats = args.output_format or ["csv", "json"]
        bundle = generate_snapshot_bundle(
            num_records=args.records,
            seed=seed,
            include_profiles=_should_include_profiles(entity_filter),
        )
        artifacts = export_snapshot_bundle(
            bundle,
            args.output_dir,
            entity_filter=entity_filter,
            output_formats=output_formats,
        )
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
