"""Demo-focused CLI that previews generator output and API responses."""
from __future__ import annotations

import argparse
import json
import secrets
from typing import Any

import requests
from rich.console import Console
from rich.panel import Panel

from enterprise_synthetic_data_hub.config.settings import settings
from enterprise_synthetic_data_hub.generation.generator import generate_snapshot_bundle

DEFAULT_API_URL = "http://127.0.0.1:5000"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Demo data preview CLI")
    parser.add_argument("--records", type=int, default=5, help="Number of records to generate")
    parser.add_argument("--seed", type=int, default=None, help="Seed override for deterministic runs")
    parser.add_argument(
        "--randomize",
        action="store_true",
        help="Use a random seed instead of the governed default",
    )
    parser.add_argument(
        "--preview",
        type=int,
        default=2,
        help="Number of rows to display per entity",
    )
    parser.add_argument(
        "--use-api",
        action="store_true",
        help="Hit the local Flask API instead of running the generator in-process",
    )
    parser.add_argument(
        "--api-url",
        default=DEFAULT_API_URL,
        help="Base URL for the local Flask API (used when --use-api is set)",
    )
    parser.add_argument(
        "--endpoint",
        choices=["bundle", "person", "vehicle", "profile"],
        default="bundle",
        help="API endpoint to hit when --use-api is set",
    )
    return parser


def _resolve_seed(seed: int | None, randomize: bool) -> int | None:
    if randomize:
        return secrets.randbelow(1_000_000_000)
    return seed


def _render_json(console: Console, title: str, payload: Any) -> None:
    console.rule(title)
    serializable = {} if payload is None else payload
    console.print_json(data=json.loads(json.dumps(serializable)))


def _preview_bundle(console: Console, args: argparse.Namespace) -> None:
    seed = _resolve_seed(args.seed, args.randomize)
    bundle = generate_snapshot_bundle(num_records=args.records, seed=seed)
    console.print(
        Panel.fit(
            f"Generator preview — records={args.records} seed={seed or settings.random_seed}",
            title="Generator",
        )
    )
    metadata = bundle.metadata.model_dump(mode="json")
    _render_json(console, "Metadata", metadata)
    _render_json(console, "Persons", bundle.persons[: args.preview])
    _render_json(console, "Vehicles", bundle.vehicles[: args.preview])
    _render_json(console, "Profiles", bundle.profiles[: args.preview])


def _call_api(api_url: str, endpoint: str, args: argparse.Namespace) -> dict[str, Any]:
    url = f"{api_url.rstrip('/')}/generate/{'bundle' if endpoint == 'bundle' else endpoint}"
    payload = {
        "records": args.records,
        "seed": args.seed,
        "randomize": args.randomize,
    }
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def _preview_api(console: Console, args: argparse.Namespace) -> None:
    try:
        payload = _call_api(args.api_url, args.endpoint, args)
    except requests.RequestException as exc:  # pragma: no cover - network failure
        console.print(f"[red]API request failed:[/red] {exc}")
        raise SystemExit(2) from exc
    console.print(
        Panel.fit(
            f"API preview — endpoint={args.endpoint} records={args.records}",
            title="Flask API",
        )
    )
    _render_json(console, "Metadata", payload.get("metadata"))
    key = {
        "person": "persons",
        "vehicle": "vehicles",
        "profile": "profiles",
        "bundle": "profiles",
    }.get(args.endpoint, "persons")
    if args.endpoint == "bundle":
        _render_json(console, "Persons", payload.get("persons", [])[: args.preview])
        _render_json(console, "Vehicles", payload.get("vehicles", [])[: args.preview])
        _render_json(console, "Profiles", payload.get("profiles", [])[: args.preview])
    else:
        _render_json(console, key.title(), payload.get(key, [])[: args.preview])


def run_demo(argv: list[str] | None = None, console: Console | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.records <= 0:
        parser.error("--records must be positive")
    console = console or Console()
    if args.use_api:
        _preview_api(console, args)
    else:
        _preview_bundle(console, args)
    return 0


def main(argv: list[str] | None = None) -> int:
    return run_demo(argv)


__all__ = ["build_parser", "main", "run_demo"]
