# Architecture
Text-based overview of the Enterprise Synthetic Data Hub POC.

## Components
- **Generator** (`generation/generator.py`): rule-based builder for Persons, Vehicles, Profiles with deterministic seed (20240601) and synthetic markers.
- **Config** (`config/settings.py`): dataset version, seed, synthetic marker, API key environment variable.
- **Exports** (`io/exporters.py`): writers for CSV/JSON/NDJSON/Parquet plus manifest checksums and stats.
- **CLI** (`cli/main.py`): `generate-snapshot` command wiring generator to exporters.
- **API** (`api/app.py`): Flask endpoints `/healthz`, `/generate/*`, optional API-key middleware, and `/demo` UI.
- **Demo orchestration** (`scripts/run_demo_flow.py`): stepwise flow with structured JSONL logging and profile-driven settings.
- **Tests** (`tests/`): smoke/performance, CLI/API contracts, and manifest assertions.

## Data Flow (text diagram)
```
config/settings.py -- seed/version --> generation/generator.py --> SnapshotBundle
SnapshotBundle --> io/exporters.py --> CSV/JSON/NDJSON/Parquet + manifest (checksums, stats)
SnapshotBundle --> api/app.py (/generate/*) and cli/main.py (generate-snapshot)
cli/main.py + exporters --> data/snapshots/<version>/
api/app.py (/demo UI) --> users --> manifests + synthetic markers for QA
scripts/run_demo_flow.py --> orchestrates CLI/API + logs to data/demo_runs/
```

## Determinism + Governance Hooks
- Seed defaults to 20240601; API/CLI report effective seed in responses/stdout.
- `synthetic_source` propagated across entities; validators enforce presence.
- Manifests capture SHA-256 checksums, record counts, and stats for integrity checks.

## Success Metrics
- Reproducible outputs across CLI/API with the same seed and profile.
- Golden tests and manifest checks reduce flaky regressions by ≥50%.
- Onboarding via `make demo-gate` completes in under 30 minutes with deterministic artifacts.
