# Testing Guide
Deterministic tests ensure reproducibility and reduce flakes. Pytest is the primary runner.

## Quick Start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
pytest
```

## Test Suites
- **Smoke/demo tests**: `tests/smoke/` (e.g., `tests/smoke/test_generation_performance.py`) validate performance and input guardrails. Tagged with `@pytest.mark.demo` for demo flows.
- **CLI contracts**: `tests/test_cli.py` covers parser flags, manifest emission, and NDJSON support.
- **API contracts**: `tests/api/test_demo_api.py` verifies `/healthz`, `/generate/*`, and synthetic markers.
- **Golden expectations**: Manifests include SHA-256 checksums and stats; tests assert counts and marker presence to detect drift.

## Running Targeted Suites
- Demo smoke only: `pytest -m demo`
- API only: `pytest tests/api/test_demo_api.py`
- Performance smoke: `pytest tests/smoke/test_generation_performance.py -k performance`

## Adding Tests
1. Prefer deterministic seed **20240601** unless explicitly testing randomization.
2. Use helpers from `enterprise_synthetic_data_hub.generation.generator` and CLI entrypoints to mirror user flows.
3. Assert synthetic markers and manifest integrity (counts, checksums, stats) to maintain governance guarantees.
4. Keep runtime short; smoke/perf tests target <5s for 1000-record generation.

## CI Expectations
- Local runs of `pytest` should mirror GitHub Actions results.
- Demo operators can rely on `make demo-gate` (validation → smoke → flow) to exercise tagged demo tests.
