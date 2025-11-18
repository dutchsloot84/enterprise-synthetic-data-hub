# Demo Runbook – Live Walkthrough
Version: 0.1.0
Last Updated: 2024-06-09

## Prerequisites
- Python 3.10+
- `pip install -e .[dev]`
- Terminal that supports ANSI colors (for the demo CLI)

## Step 1 – Generate the governed snapshot
```bash
python -m enterprise_synthetic_data_hub.cli.main generate-snapshot \
    --output-dir data/snapshots/v0.1 \
    --records 50 --randomize
```
_What to narrate_: call out deterministic defaults (`settings.random_seed`) and the new `--randomize` flag for ad-hoc previews. Mention that profiles are included automatically and manifest counts now list `record_count_profiles`.

## Step 2 – Preview data locally
```bash
python scripts/demo_data.py --records 5 --preview 2
```
_What to narrate_: highlight the Rich separators, metadata block, and how Profiles summarize Person + Vehicle context. Point to `data/demo_samples/v0.1/*.json` as a reusable asset for slide decks.

## Step 3 – Start the Flask API
```bash
export FLASK_APP=enterprise_synthetic_data_hub.api.app:app
flask run
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
python scripts/demo_data.py --use-api --api-url http://127.0.0.1:5000 --records 3 --preview 1
```
_What to narrate_: the CLI now shows which endpoint it called, the effective seed, and quick JSON snippets for persons/vehicles/profiles.

## Step 5 – Automate with `make demo`
```bash
make demo
```
This target wraps Steps 1–4: generates a snapshot, runs the generator preview, then launches `scripts/demo_start_api.sh` which starts Flask, performs health + sample requests, and finally executes the demo CLI in API mode. Use this when time-boxed or when handing off the repo to reviewers.

## Step 6 – Smoke tests
```bash
pytest -m smoke
```
_What to narrate_: smoke tests prove `/generate/profile` responds and the CLI preview works in headless mode. Point stakeholders to `tests/smoke/test_demo_flow.py` if they want to extend coverage.

## Quick Reference
- API reference: `docs/api.md`
- Demo CLI module: `src/enterprise_synthetic_data_hub/cli/demo.py`
- Automation script: `scripts/demo_start_api.sh`
- Prompt changelog: `docs/demo/changelog_v2.md`
