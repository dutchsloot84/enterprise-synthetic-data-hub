"""Utilities for printing labeled steps + supporting interactive pauses."""
from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from typing import Callable, Generic, Iterable, List, Optional, Tuple, TypeVar

T = TypeVar("T")


@dataclass
class StepRecord:
    """Lightweight timing information for the demo summary."""

    label: str
    duration_seconds: float


class StepManager(Generic[T]):
    """Prints bracketed step banners and records timing info."""

    def __init__(self, *, interactive: bool = False) -> None:
        self._interactive = interactive and sys.stdin.isatty()
        self._records: List[StepRecord] = []

    def run(self, label: str, func: Callable[[], T]) -> T:
        print(f"[ {label} ]")
        start = time.perf_counter()
        result = func()
        duration = time.perf_counter() - start
        self._records.append(StepRecord(label=label, duration_seconds=duration))
        if self._interactive:
            input("Press ENTER to continue...")
        return result

    def last_successful_step(self) -> Optional[str]:
        if not self._records:
            return None
        return self._records[-1].label

    def durations(self) -> Iterable[Tuple[str, float]]:
        for record in self._records:
            yield record.label, record.duration_seconds


__all__ = ["StepManager", "StepRecord"]
