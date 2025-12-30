# Demo Readiness – Operator Contract
_Mode B hybrid with Mode C fallback; concise checklist for release/demo operators._

## Demo Gate
- **Command:** `make demo-gate`
- **Sequence:** validation → smoke → flow (skips smoke inside the flow)
  - `make demo-validate`
  - `make demo-smoke`
  - `python scripts/run_demo_flow.py --skip-smoke`
- **PASS means:** schemas + synthetic markers are intact, demo smoke tests pass, and the orchestrated flow completes with smoke skipped internally.

## Minimum Pass Criteria (Demo Red Lines)
- `make demo-gate` succeeds end-to-end.
- Synthetic marker (`settings.synthetic_marker`) present on all persons, vehicles, and profiles (checked by `make demo-validate`).
- Can pivot to canned artifacts within **60 seconds**.
- Negative-path validation exists: `tests/smoke/test_api_contract.py::test_generate_rejects_invalid_records`.

## Demo Modes
- **Mode B (Hybrid):** Live `/healthz` + show canned artifacts; optionally trigger a small live generate for freshness.
- **Mode C (Fallback):** Canned artifacts only; use screenshots if needed.
- **Switching:** If API health, smoke, or live generation stalls, drop to Mode B; if the API cannot start or time is <60s, switch to Mode C and narrate from the canned set.

## Rehearsal Matrix
- **Native Python**
  - Setup: `python -m venv .venv && source .venv/bin/activate && pip install -e .[dev]`
  - Run: `make demo-gate`
  - Expect: validation + smoke + flow summary; `.demo_api_pid/.demo_api_port` cleared on stop.
- **Docker**
  - Setup: `docker build -t esdh-demo .`
  - Run: `docker run --rm -p 5000:5000 esdh-demo make demo-gate`
  - Expect: same gate sequence; host port 5000 must be free. This is the recommended “it works anywhere” path when Windows Git Bash or local shells are temperamental.
- **Bootstrap (Unix / Windows)**
  - Setup: `bash scripts/bootstrap.sh` (Unix) or `scripts\\bootstrap.bat` (Windows)
  - Run: `make demo-gate`
  - Expect: env + deps installed, then gate run; ensure `PYTHONPATH=src` when invoking scripts directly.
- **Windows fallback**
  - If Bash-based orchestration is blocked, start the API via Python directly: `python -m flask run --host 127.0.0.1 --port 5000 --no-debugger --no-reload`
  - Verify `http://127.0.0.1:5000/healthz` via `curl` before running CLI previews or `python scripts/run_demo_flow.py --skip-smoke`.

## Canned Artifacts (Demo Fallbacks)
- **Canonical Mode C set:** `data/demo_samples/phase1/` (`persons_seed_20240601.json`, `vehicles_seed_20240601.json`, `profiles_seed_20240601.json`, `bundle_seed_20240601.json`).
- **Curated reference set:** `data/demo_samples/v0.1/` (use for visuals; not the primary fallback).
- **Regenerate:** follow `data/demo_samples/README.md` (Flask test client script seeded to `20240601`).

## Failure Recovery (aim for 60s)
- **Port 5000 conflict:** free the port (e.g., `lsof -i :5000` to find blocker) then rerun `make demo-gate`.
- **Stale `.demo_api_pid` / `.demo_api_port`:** `make demo-stop` or `make demo-clean`.
- **Missing deps/venv:** `python -m venv .venv && source .venv/bin/activate && pip install -e .[dev]`.
- **Corrupted demo artifacts:** restore from git or regenerate via `data/demo_samples/README.md`.
- **Outdated Docker image:** `docker build -t esdh-demo .` then rerun container with `make demo-gate`.

## Runbook Link
- Narrated walkthrough: `docs/demo/06-runbook.md`.
