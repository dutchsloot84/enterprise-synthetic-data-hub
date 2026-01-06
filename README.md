# Enterprise Synthetic Data Hub (POC)

## Overview
Enterprise Synthetic Data Hub (ESDH) is a January 2026 proof of concept focused on governed, deterministic synthetic data for Persons, Vehicles, and derived Profiles. The project emphasizes:
- **Determinism and reproducibility** via the default seed **20240601**, manifests with SHA-256 checksums, and golden tests.
- **Synthetic governance** with `synthetic_source` markers on every entity and no reliance on production PII.
- **Automation-first workflows** across CLI, API, exporters, and demo orchestration to reduce flakes and accelerate QA onboarding.

## Core Invariants
- Default seed: **20240601** (override via CLI/API while preserving the reported seed).
- Manifest-driven exports with file-level checksums and entity stats for drift detection.
- Synthetic-only generation (rules-based, deterministic lookups) with explicit provenance markers.
- Golden tests and demo smoke flows ensure **100% issue reproducibility** and target **≥50% flaky test reduction**.
- Onboarding goal: **<30 minutes** to run `make demo-gate` successfully on a fresh machine.

## Components
- **Generator** (`enterprise_synthetic_data_hub.generation.generator`): deterministic bundle builder for Persons, Vehicles, Profiles; exposes generation plan for docs/tests.
- **CLI** (`enterprise_synthetic_data_hub.cli.main`): `generate-snapshot` command with `--entity-filter`, `--output-format` (csv, json, ndjson, parquet), `--seed`, and `--randomize`.
- **API** (`enterprise_synthetic_data_hub.api.app`): Flask app with `/healthz`, `/generate/*`, optional `ESDH_API_KEY` middleware, and `/demo` HTML UI.
- **Exports** (`enterprise_synthetic_data_hub.io.exporters`): CSV/JSON/NDJSON/Parquet writers plus manifest + snapshot README and stats.
- **Demo flow** (`scripts/run_demo_flow.py`): orchestrated run with structured JSONL logging to `data/demo_runs/demo_flow_log.jsonl`.
- **Tests** (pytest): smoke and performance coverage under `tests/smoke/`, CLI/API contracts, and golden snapshot assertions.

## Quick Start
1. **Set up environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .[dev]
   ```
2. **Generate a deterministic snapshot**
   ```bash
   python -m enterprise_synthetic_data_hub.cli.main generate-snapshot \
     --output-dir data/snapshots/v0.1 \
     --records 200 \
     --seed 20240601 \
     --output-format csv json ndjson parquet
   ```
   The command prints exported paths and creates `snapshot_manifest_v0_1.json` with checksums and stats.
3. **Preview via API**
   ```bash
   export FLASK_APP=enterprise_synthetic_data_hub.api.app:app
   flask run --host 127.0.0.1 --port 5000
   curl -fsSL http://127.0.0.1:5000/healthz
   curl -fsSL -X POST http://127.0.0.1:5000/generate/bundle -H 'Content-Type: application/json' -d '{"records": 3}'
   ```
   Set `ESDH_API_KEY` to enforce the `X-API-Key` header when needed.
4. **Demo gate (recommended onboarding path)**
   ```bash
   make demo-gate  # validation -> smoke -> flow using config/demo.yaml and seed 20240601
   ```
   Expected outputs include `data/demo_runs/<timestamp>_<profile>/` artifacts, structured demo flow logs, and synthetic markers on all entities.

## Governance & Safety
- No production data or uploads; all outputs are fabricated from deterministic rules.
- Every entity includes `synthetic_source="enterprise-synthetic-data-hub v0.1"`.
- Manifests expose checksums and stats to verify integrity before sharing artifacts.
- See [docs/PII_POLICY.md](docs/PII_POLICY.md) for handling rules, retention, and demo API guidance.

## Contribution Guidelines
- Follow reproducibility guardrails: prefer the default seed 20240601 for tests and docs.
- Run `pytest` (or `make demo-gate` for demo scenarios) before submitting changes.
- Keep documentation aligned with manifests, CLI/API flags, and the generator’s reported plan.

## Additional References
- [CLI usage](docs/CLI_USAGE.md)
- [API reference](docs/API_REFERENCE.md)
- [Testing guide](docs/TESTING_GUIDE.md)
- [CI/CD overview](docs/CI_CD_OVERVIEW.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Demo readiness](docs/DEMO_READINESS.md)
- [PII policy](docs/PII_POLICY.md)
- [Changelog](CHANGELOG.md)
