"""Demo-focused CLI that previews generator output and API responses."""
from __future__ import annotations

import argparse
import json
import os
import secrets
from dataclasses import dataclass
from typing import Any

import requests
from rich.console import Console
from rich.panel import Panel

from enterprise_synthetic_data_hub.config.demo_profiles import (
    DemoAPISettings,
    DemoConfigError,
    DemoProfile,
    get_api_settings,
    get_demo_profile,
)
from enterprise_synthetic_data_hub.config.settings import settings
from enterprise_synthetic_data_hub.generation.generator import generate_snapshot_bundle


@dataclass(frozen=True)
class ResolvedDemoArgs:
    """Container for CLI arguments after applying profile defaults."""

    profile: DemoProfile
    api: DemoAPISettings
    records: int
    seed: int | None
    randomize: bool
    preview: int
    use_api: bool
    api_url: str
    endpoint: str


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Demo data preview CLI")
    parser.add_argument(
        "--profile",
        default=None,
        help="Demo profile name from config/demo.yaml (default: $DEMO_PROFILE or baseline)",
    )
    parser.add_argument(
        "--records",
        type=int,
        default=None,
        help="Number of records to generate (defaults to the profile's person count)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Seed override for deterministic runs (falls back to the profile seed)",
    )
    parser.add_argument(
        "--randomize",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Toggle random seed behavior (defaults to the profile setting)",
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
        default=None,
        help="Base URL for the local Flask API (defaults to config/demo.yaml)",
    )
    parser.add_argument(
        "--endpoint",
        choices=["bundle", "person", "vehicle", "profile"],
        default="bundle",
        help="API endpoint to hit when --use-api is set",
    )
    return parser


def _resolve_seed(seed: int | None, randomize: bool, profile_seed: int | None) -> int | None:
    if randomize:
        return secrets.randbelow(1_000_000_000)
    if seed is not None:
        return seed
    if profile_seed is not None:
        return profile_seed
    return settings.random_seed


def _resolve_runtime_args(parser: argparse.ArgumentParser, args: argparse.Namespace) -> ResolvedDemoArgs:
    try:
        profile = get_demo_profile(args.profile)
        api_settings = get_api_settings()
    except DemoConfigError as exc:  # pragma: no cover - exercised via CLI parsing
        parser.error(str(exc))
    randomize = profile.randomize if args.randomize is None else args.randomize
    records = args.records if args.records is not None else profile.records_person
    if records <= 0:
        parser.error("--records must be positive")
    preview = args.preview
    if preview <= 0:
        parser.error("--preview must be positive")
    seed = args.seed if args.seed is not None else profile.seed
    api_port_override = os.environ.get("DEMO_API_PORT")
    api_url = args.api_url or f"http://{api_settings.host}:{api_port_override or api_settings.port}"
    return ResolvedDemoArgs(
        profile=profile,
        api=api_settings,
        records=records,
        seed=seed,
        randomize=randomize,
        preview=preview,
        use_api=bool(args.use_api),
        api_url=api_url,
        endpoint=args.endpoint,
    )


def _render_json(console: Console, title: str, payload: Any) -> None:
    console.rule(title)
    serializable = {} if payload is None else payload
    console.print_json(data=json.loads(json.dumps(serializable)))


def _preview_bundle(console: Console, resolved: ResolvedDemoArgs) -> None:
    seed = _resolve_seed(resolved.seed, resolved.randomize, resolved.profile.seed)
    bundle = generate_snapshot_bundle(num_records=resolved.records, seed=seed)
    console.print(
        Panel.fit(
            f"Generator preview — profile={resolved.profile.name} records={resolved.records} seed={seed}",
            title="Generator",
        )
    )
    metadata = bundle.metadata.model_dump(mode="json")
    _render_json(console, "Metadata", metadata)
    _render_json(console, "Persons", bundle.persons[: resolved.preview])
    _render_json(console, "Vehicles", bundle.vehicles[: resolved.preview])
    _render_json(console, "Profiles", bundle.profiles[: resolved.preview])


def _call_api(api_url: str, endpoint: str, resolved: ResolvedDemoArgs) -> dict[str, Any]:
    seed = _resolve_seed(resolved.seed, resolved.randomize, resolved.profile.seed)
    url = f"{api_url.rstrip('/')}/generate/{'bundle' if endpoint == 'bundle' else endpoint}"
    payload = {
        "records": resolved.records,
        "seed": seed,
        "randomize": resolved.randomize,
    }
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    payload = response.json()
    payload.setdefault("metadata", {}).setdefault("synthetic_source", settings.synthetic_marker)
    return payload


def _preview_api(console: Console, resolved: ResolvedDemoArgs) -> None:
    try:
        payload = _call_api(resolved.api_url, resolved.endpoint, resolved)
    except requests.RequestException as exc:  # pragma: no cover - network failure
        console.print(f"[red]API request failed:[/red] {exc}")
        raise SystemExit(2) from exc
    console.print(
        Panel.fit(
            f"API preview — endpoint={resolved.endpoint} profile={resolved.profile.name} records={resolved.records}",
            title="Flask API",
        )
    )
    _render_json(console, "Metadata", payload.get("metadata"))
    key = {
        "person": "persons",
        "vehicle": "vehicles",
        "profile": "profiles",
        "bundle": "profiles",
    }.get(resolved.endpoint, "persons")
    if resolved.endpoint == "bundle":
        _render_json(console, "Persons", payload.get("persons", [])[: resolved.preview])
        _render_json(console, "Vehicles", payload.get("vehicles", [])[: resolved.preview])
        _render_json(console, "Profiles", payload.get("profiles", [])[: resolved.preview])
    else:
        _render_json(console, key.title(), payload.get(key, [])[: resolved.preview])


def run_demo(argv: list[str] | None = None, console: Console | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    resolved = _resolve_runtime_args(parser, args)
    console = console or Console()
    if resolved.use_api:
        _preview_api(console, resolved)
    else:
        _preview_bundle(console, resolved)
    return 0


def main(argv: list[str] | None = None) -> int:
    return run_demo(argv)


__all__ = ["build_parser", "main", "run_demo"]
