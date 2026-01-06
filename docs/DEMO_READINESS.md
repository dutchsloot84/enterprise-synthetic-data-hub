# Demo Readiness – Operator Contract
_Concise checklist for running governed demos with deterministic outputs._

## Pass Criteria
- `make demo-gate` succeeds end-to-end (validation → smoke → flow) using seed **20240601**.
- Synthetic markers present on all Persons/Vehicles/Profiles; manifest includes SHA-256 checksums and entity stats.
- Operator can pivot to canned artifacts within **60 seconds** if live generation fails.

## Primary Path (Mode B hybrid)
1. **Prep**: `python -m venv .venv && source .venv/bin/activate && pip install -e .[dev]`.
2. **Run gate**: `make demo-gate` (uses `config/demo.yaml` for profiles/ports; skips smoke inside flow).
3. **Validate outputs**:
   - Artifacts under `data/demo_runs/<timestamp>_<profile>/` with `latest_demo` symlink.
   - `snapshot_manifest_*` shows counts, stats, and checksums.
   - `data/demo_runs/demo_flow_log.jsonl` contains structured step timing.
4. **Narrate**: show `/healthz`, `/demo` UI, and a small `/generate/bundle` call (records=3) to surface the `synthetic_source` marker.

## Fallbacks (Mode C)
- Use canned artifacts in `data/demo_samples/phase1/` (seeded to 20240601) for screenshots and walkthroughs.
- If API port 5000 is busy: set `DEMO_API_PORT=5051 make demo` or run `python -m flask run --host 127.0.0.1 --port 5051 --no-debugger --no-reload` then rerun CLI preview.
- Clear stale state with `make demo-stop` or `make demo-clean` when `.demo_api_pid`/`.demo_api_port` linger.

## Troubleshooting (target <60s)
- **Health check**: `curl -fsSL http://127.0.0.1:5000/healthz` (expect default seed and plan).
- **Seed drift**: confirm CLI/API output reports the effective seed; rerun with `--seed 20240601` if needed.
- **Dependencies**: rebuild Docker image (`docker build -t esdh-demo .`) or reinstall (`pip install -e .[dev]`).
- **Artifacts missing**: rerun `make demo-validate` to regenerate governed bundles.

## References
- Runbook: `docs/demo/06-runbook.md`
- PII guardrails: `docs/PII_POLICY.md`
- CLI/API details: `docs/CLI_USAGE.md`, `docs/API_REFERENCE.md`
