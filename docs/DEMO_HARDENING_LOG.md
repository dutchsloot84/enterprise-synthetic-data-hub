# Demo Hardening Log (append-only)
- Purpose: each demo-hardening PR appends an entry so sequential changes stay aligned; do not rewrite history.

## Entries
- **2024-** Added `make demo-gate` to enforce a fail-fast sequence (validate → smoke → demo flow with `--skip-smoke`). Commands: `make demo-validate`, `make demo-smoke`, `python scripts/run_demo_flow.py --skip-smoke`. Impact: improves demo reliability by gating on validation and smoke tests before orchestration. Not changed: generator logic, schemas, auth, or distribution mechanisms.
- **2025-12-30** Documented the canned demo refresh path and quick checks. Commands: `PYTHONPATH=src python - <<'PY' ...` (Flask test client to regenerate `data/demo_samples/phase1/*.json` with seed `20240601`), `make demo-validate`, and `rg "enterprise-synthetic-data-hub v0.1" data/demo_samples/phase1/*.json` for a fast synthetic-marker spot check. Not changed: generator logic, schemas, filenames, or tests; no new helper targets added.
