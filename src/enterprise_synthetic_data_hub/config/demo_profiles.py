"""Helpers for loading demo profile configuration."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import os
from typing import Any

import yaml

CONFIG_PATH = Path(__file__).resolve().parents[3] / "config" / "demo.yaml"


class DemoConfigError(RuntimeError):
    """Raised when the demo configuration file is missing or invalid."""


@dataclass(frozen=True)
class DemoProfile:
    name: str
    records_person: int
    records_vehicle: int
    records_profile: int
    seed: int | None
    randomize: bool
    description: str | None = None


@dataclass(frozen=True)
class DemoAPISettings:
    host: str
    port: int
    health_endpoint: str


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise DemoConfigError(f"Demo config missing: {path}")
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:  # pragma: no cover - invalid YAML is rare
        raise DemoConfigError(f"Failed to parse demo config: {exc}") from exc


def load_demo_config(path: Path | None = None) -> dict[str, Any]:
    """Return the parsed demo config as a dictionary."""

    return _load_yaml(path or CONFIG_PATH)


def _coerce_bool(value: Any) -> bool:
    return bool(value) if value is not None else False


def _coerce_int(value: Any) -> int | None:
    if value is None:
        return None
    return int(value)


def _select_profile(config: dict[str, Any], profile_name: str) -> DemoProfile:
    profiles = config.get("profiles") or {}
    if profile_name not in profiles:
        available = ", ".join(sorted(profiles)) or "<none>"
        raise DemoConfigError(
            f"Profile '{profile_name}' not found in config/demo.yaml (available: {available})"
        )
    data = profiles[profile_name] or {}
    return DemoProfile(
        name=profile_name,
        records_person=int(data.get("records_person", 10)),
        records_vehicle=int(data.get("records_vehicle", data.get("records_person", 10))),
        records_profile=int(data.get("records_profile", data.get("records_person", 10))),
        seed=_coerce_int(data.get("seed")),
        randomize=_coerce_bool(data.get("randomize")),
        description=data.get("description"),
    )


def get_profile_name(explicit: str | None = None) -> str:
    return explicit or os.environ.get("DEMO_PROFILE") or "baseline"


def get_demo_profile(profile_name: str | None = None, *, path: Path | None = None) -> DemoProfile:
    config = load_demo_config(path)
    return _select_profile(config, get_profile_name(profile_name))


def get_api_settings(path: Path | None = None) -> DemoAPISettings:
    config = load_demo_config(path)
    api = config.get("api") or {}
    return DemoAPISettings(
        host=str(api.get("default_host", "127.0.0.1")),
        port=int(api.get("default_port", 5000)),
        health_endpoint=str(api.get("health_endpoint", "/healthz")),
    )


def _main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Inspect demo configuration")
    subparsers = parser.add_subparsers(dest="command", required=True)

    profile_parser = subparsers.add_parser("profile", help="Print a demo profile as JSON")
    profile_parser.add_argument("name", nargs="?", default=None)

    subparsers.add_parser("api", help="Print API defaults as JSON")

    args = parser.parse_args(argv)

    if args.command == "profile":
        profile = get_demo_profile(args.name)
        print(json.dumps(profile.__dict__, indent=2))
        return 0
    if args.command == "api":
        api = get_api_settings()
        print(json.dumps(api.__dict__, indent=2))
        return 0
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(_main())


__all__ = ["DemoConfigError", "DemoProfile", "DemoAPISettings", "get_demo_profile", "get_api_settings", "get_profile_name"]
