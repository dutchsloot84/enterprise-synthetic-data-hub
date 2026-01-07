# Demo Runbook – Live Walkthrough
Version: 0.1.1
Last Updated: 2026-01-06

## Prerequisites
- Python 3.10+
- `pip install -e .[dev]`
- Terminal that supports ANSI colors (for the demo CLI)

## Demo Guardrails
- The Flask API is intentionally unauthenticated and unthrottled—keep it scoped to local/demo networks only.
- The flow is not production hardened; deterministic seeds and governed schemas are prioritized over scalability or resilience.
- If live generation fails, fall back to the canned payloads in `data/demo_samples/phase1/` for slides or quick API stand-ins.

## Step 0 – Inspect the demo profile
```bash
make demo-profile-info
```
_What to narrate_: demo profiles (from `config/demo.yaml`) control record counts, seeds, and API defaults. Use `DEMO_PROFILE=heavy` to stress the flow.

## Step 1 – Generate the governed snapshot
```bash
python -m enterprise_synthetic_data_hub.cli.main generate-snapshot \
    --output-dir data/snapshots/v0.1 \
    --records 50 --randomize
```
_What to narrate_: call out deterministic defaults (`settings.random_seed`) and the `--randomize` flag for ad-hoc previews. Mention that profiles are included automatically and manifest counts list `record_count_profiles`.

## Step 2 – Preview data locally
```bash
python scripts/demo_data.py --records 5 --preview 2
```
_What to narrate_: highlight the Rich separators, metadata block, and how Profiles summarize Person + Vehicle context. Point to `data/demo_samples/v0.1/*.json` as a reusable asset for slide decks.

## Step 3 – Start the Flask API
```bash
export PYTHONPATH=src
flask --app enterprise_synthetic_data_hub.api.app run
```
_What to narrate_: `GET /healthz` surfaces dataset version + generation plan. Every `/generate/*` endpoint accepts `{records, seed, randomize}` so the CLI and API stay in sync.

Example curl (in a second terminal):
```bash
curl -s -X POST http://127.0.0.1:5000/generate/profile \
  -H 'Content-Type: application/json' \
  -d '{"records": 2, "seed": 123}' | jq '.profiles'
```

## Step 4 – Hit the API via the demo CLI
```bash
python scripts/demo_data.py --use-api --api-url http://127.0.0.1:5000 --records 3 --preview 1 --endpoint bundle
```
_What to narrate_: the CLI shows which endpoint it called, the effective seed, and quick JSON snippets for persons/vehicles/profiles.

## Step 5 – Automate with `make demo`
```bash
make demo
```
This target wraps Steps 1–4: generates a snapshot, runs the generator preview, then launches `scripts/demo_start_api.sh` which starts Flask, performs health + sample requests, and finally executes the demo CLI in API mode. Use this when time-boxed or when handing off the repo to reviewers.

## Step 6 – Demo tests
```bash
pytest -m demo
```
_What to narrate_: demo tests prove `/generate/profile` responds and the CLI preview works in headless mode. Point stakeholders to `tests/smoke/test_demo_flow.py` if they want the stricter smoke variant.

## Quick Reference
- API reference: `docs/api.md`
- Demo CLI module: `src/enterprise_synthetic_data_hub/cli/demo.py`
- Automation script: `scripts/demo_start_api.sh`
- Prompt changelog: `docs/demo/changelog_v2.md`
