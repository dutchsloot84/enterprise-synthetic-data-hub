# Demo Readiness – Operator Contract

## Demo Gate
- **Name:** `make demo-gate`
- **Sequence:** `make demo-validate` → `make demo-smoke` → `python scripts/run_demo_flow.py --skip-smoke`
- **Fail-fast:** inherits `SHELLFLAGS := -eu -o pipefail`; the first non-zero command aborts the target and returns non-zero.
- **PASS means:** validation shows schemas + synthetic markers are intact, demo smoke tests pass, and the orchestrated flow completes (with smoke skipped inside the flow).

## Minimum Pass Criteria (Demo Red Lines)
- `make demo-gate` succeeds end-to-end.
- Synthetic marker (`settings.synthetic_marker`) present on all persons, vehicles, and profiles.
- Able to pivot to canned demo artifacts within **60 seconds** if live generation or API is unhealthy.

## Demo Modes
- **Mode B (Hybrid):** Live `/healthz` + canned artifacts + optional small live generate for freshness.
- **Mode C (Offline fallback):** Canned artifacts only.
- **When to switch:** If API health, smoke tests, or live generation stall, drop to Mode B; if API cannot start or time is under 60s, switch to Mode C and narrate from canned assets.

## Rehearsal Matrix
- **Native Python**
  - Setup: `python -m venv .venv && source .venv/bin/activate && pip install -e .[dev]`
  - Demo: `make demo-gate`
  - Friction: missing deps; stale `.demo_api_pid`; port 5000 in use.
- **Docker**
  - Setup: `docker build -t esdh-demo .`
  - Demo: `docker run --rm -p 5000:5000 esdh-demo make demo-gate`
  - Friction: image drift; host port 5000 conflicts.
- **Bootstrap (Unix / Windows)**
  - Setup: `bash scripts/bootstrap.sh` (Unix) or `scripts\\bootstrap.bat` (Windows)
  - Demo: `make demo-gate`
  - Friction: shell path quoting on Windows; ensure `PYTHONPATH=src` is set if running scripts directly.

## Canned Demo Artifacts
- **Canonical locations:** `data/demo_samples/v0.1/` (official demo set) and legacy backups in `data/demo_samples/phase1/`.
- **Regeneration pointer:** see `data/demo_samples/phase1/README.md` for scripted regeneration of canned payloads and golden snapshots.

## Runbook Reference
- Authoritative step-by-step: `docs/demo/06-runbook.md`.

## Failure Recovery (aim for 60-second fixes)
- **Port conflict (5000):** `lsof -i :5000` then stop the blocker; re-run `make demo-gate`.
- **Stale Flask PID:** `make demo-stop` or `make demo-clean` to clear `.demo_api_pid`/`.demo_api_port`.
- **Missing venv/deps:** `python -m venv .venv && source .venv/bin/activate && pip install -e .[dev]`.
- **Corrupted demo artifacts:** restore from git or regenerate via `data/demo_samples/phase1/README.md`.
- **Outdated Docker image:** `docker build -t esdh-demo .` then rerun the container.
