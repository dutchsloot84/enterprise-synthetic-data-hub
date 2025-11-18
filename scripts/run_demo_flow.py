#!/usr/bin/env python
"""Story-driven orchestration for the make demo target."""
from __future__ import annotations

import argparse
import json
import platform
import time

from enterprise_synthetic_data_hub.config import demo_profiles
from enterprise_synthetic_data_hub.config.settings import settings

from demo_flow import DemoRunState
from demo_flow import api as api_flow
from demo_flow import preview, snapshot, steps, validation


def _measure(state: DemoRunState, metric_name: str, func):
    start = time.perf_counter()
    result = func()
    state.record_timing(metric_name, time.perf_counter() - start)
    return result


def orchestrate(state: DemoRunState, stepper: steps.StepManager, skip_smoke: bool) -> None:
    api_settings = demo_profiles.get_api_settings()
    try:
        state.snapshot_dir, state.manifest = stepper.run(
            "STEP 1/5 Generate governed snapshot",
            lambda: _measure(state, "snapshot_seconds", lambda: snapshot.generate_snapshot(state.profile)),
        )
        state.base_url, state.api_port = stepper.run(
            "STEP 2/5 Start Flask API",
            lambda: _measure(state, "api_start_seconds", lambda: api_flow.start_api(state.profile)),
        )
        health = stepper.run(
            "STEP 3/5 Health check",
            lambda: preview.call_health(state.base_url or "", api_settings.health_endpoint),
        )
        print(json.dumps(health, indent=2))

        def preview_block() -> list[dict]:
            profiles_payload = preview.preview_profiles_via_api(state.base_url or "", state.profile)
            print(json.dumps(profiles_payload[:1], indent=2))
            _measure(state, "cli_preview_seconds", lambda: preview.cli_preview(state.base_url or "", state.profile))
            return profiles_payload

        stepper.run("STEP 4/5 Preview data via API + CLI", preview_block)
        if not skip_smoke:
            stepper.run("STEP 5/5 Demo smoke tests", validation.run_smoke_tests)
        else:
            stepper.run(
                "STEP 5/5 Demo smoke tests (skipped)",
                lambda: print("Smoke tests skipped via --skip-smoke flag."),
            )
        _print_summary(state)
    finally:
        api_flow.stop_api()


def _print_summary(state: DemoRunState) -> None:
    print("\n===== Demo Summary =====")
    print(f"Profile: {state.profile.name}")
    if state.snapshot_dir:
        print(f"Snapshot location: {state.snapshot_dir}")
    print(f"Latest demo symlink: {snapshot.LATEST_DEMO_LINK}")
    if state.base_url:
        print(f"API URL: {state.base_url}")
    counts = (state.manifest or {}).get("record_counts", {})
    print(
        "Counts — persons: {p} vehicles: {v} profiles: {r}".format(
            p=counts.get("persons"),
            v=counts.get("vehicles"),
            r=counts.get("profiles"),
        )
    )
    print("Curated demo bundles: data/demo_samples/v0.1/")
    print(f"Synthetic marker: {settings.synthetic_marker}")
    if state.timings:
        print("Timing metrics (seconds):")
        for key in sorted(state.timings):
            print(f"  {key}: {state.timings[key]:.2f}")


def _print_failure_diagnostics(exc: Exception, state: DemoRunState, stepper: steps.StepManager, args: argparse.Namespace) -> None:
    port = state.api_port
    if port is None and api_flow.PORT_FILE.exists():
        port = api_flow.PORT_FILE.read_text(encoding="utf-8").strip()
    diagnostics = {
        "error": str(exc),
        "python_version": platform.python_version(),
        "profile": state.profile.name,
        "interactive": args.interactive,
        "skip_smoke": args.skip_smoke,
        "api_port": port,
        "last_successful_step": stepper.last_successful_step(),
    }
    print("\nDemo flow encountered an error. Diagnostics:")
    print(json.dumps(diagnostics, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="End-to-end demo orchestrator")
    parser.add_argument("--profile", default=None, help="Demo profile name (default: baseline)")
    parser.add_argument("--skip-smoke", action="store_true", help="Skip pytest -m demo")
    parser.add_argument("--interactive", action="store_true", help="Pause for input after each step")
    args = parser.parse_args()
    profile = demo_profiles.get_demo_profile(demo_profiles.get_profile_name(args.profile))
    state = DemoRunState(profile=profile)
    stepper = steps.StepManager(interactive=args.interactive)
    try:
        orchestrate(state, stepper, args.skip_smoke)
    except Exception as exc:  # pragma: no cover - orchestration guardrail
        _print_failure_diagnostics(exc, state, stepper, args)
        raise
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
