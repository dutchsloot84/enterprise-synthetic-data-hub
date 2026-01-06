# Changelog

## v0.1.0 – Enterprise Synthetic Data Hub POC (January 2026)
- Deterministic generator for Persons, Vehicles, Profiles with default seed **20240601** and `synthetic_source` markers.
- CLI `generate-snapshot` with entity filters, multiple output formats (CSV/JSON/NDJSON/Parquet), and manifest emission (SHA-256 checksums, stats, snapshot README).
- Flask API exposing `/healthz`, `/generate/*`, optional API key guard, and lightweight `/demo` UI.
- Demo orchestration via `scripts/run_demo_flow.py` with structured JSONL logs and profile-driven settings.
- Smoke/performance tests (`tests/smoke/*`), CLI/API contract tests, and golden expectations to ensure reproducibility.
- GitHub Actions workflow (`publish-snapshot.yml`) to publish governed artifacts from `develop` branch pushes.
