from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def normalize_json(value: Any, *, sort_lists: bool = False, strip_keys: set[str] | None = None) -> Any:
    """Recursively normalize JSON-like structures for deterministic comparisons."""

    strip_keys = strip_keys or set()

    if isinstance(value, dict):
        normalized = {}
        for key in sorted(value.keys()):
            if key in strip_keys:
                continue
            normalized[key] = normalize_json(value[key], sort_lists=sort_lists, strip_keys=strip_keys)
        return normalized

    if isinstance(value, list):
        normalized_list = [normalize_json(item, sort_lists=sort_lists, strip_keys=strip_keys) for item in value]
        if sort_lists:
            return sorted(normalized_list, key=lambda item: json.dumps(item, sort_keys=True))
        return normalized_list

    return value


def load_json(path: str | Path) -> Any:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)
