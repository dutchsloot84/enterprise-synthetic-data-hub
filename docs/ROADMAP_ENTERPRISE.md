# Enterprise Readiness Roadmap

## Current state (POC)
- Demo flows are validated via `make demo-gate` / `python -m pytest -m demo -q` and the scripted runner `scripts/run_demo_flow.py --skip-smoke`.
- Demo profiles live in `config/demo.yaml` and can be selected with `DEMO_PROFILE=baseline|heavy` (or `--profile` on the demo CLI).
- Docker builds succeed on open networks using `docker build -t esdh-demo .` followed by containerized demo/test runs.
- Bootstrap scripts (`scripts/bootstrap_and_demo.sh` / `scripts/bootstrap_and_demo.ps1`) remain the primary “happy path” for new users on Unix/macOS and Windows PowerShell.
- `make doctor` provides quick diagnostics for demo-day readiness.

## Pilot Phase (January 2026 baseline alignment)
- Rules-based, deterministic generator continues to bundle Persons/Vehicles/Profiles with `synthetic_source` markers.
- CLI `generate-snapshot` remains the entrypoint; Pilot scope covers deterministic seeds and export manifests while tracking gaps for `--entity-filter` and `--output-format` (csv/json/ndjson/parquet).
- API delivers `/healthz` and `/generate/*` endpoints with optional, env-var-based auth middleware planned for Pilot hardening.
- Exports remain platform-agnostic (CSV + JSON bundle/metadata); Pilot adds checksum validation in manifests without breaking existing consumers.
- Demo validation stays anchored on `scripts/run_demo_flow.py` plus `make demo-gate` for smoke/validation orchestration.
- CI continues to auto-publish snapshot artifacts via `.github/workflows/publish-snapshot.yml`.

## Known gaps
- Docker builds on CSAA networks cannot reach public PyPI due to TLS inspection; an Internal PyPI mirror is required.
- Windows portability is constrained when `make` is unavailable and when shells block bash-based orchestration.
- CI container builds have not been validated against enterprise network constraints.
- Dependency pinning/lockfiles and image signing are not yet enforced.

## Next steps to Pilot
- Stand up and document an Internal PyPI mirror/proxy; wire builds/tests to it via `PIP_INDEX_URL`, `PIP_EXTRA_INDEX_URL`, and `PIP_TRUSTED_HOST`.
- Enable CI to build and smoke-test the Docker image using the mirror and publish to an internal registry.
- Provide a fully scripted demo flow that avoids bash dependencies on Windows (python-native entrypoints).
- Capture platform portability guidance (Docker Desktop vs. Linux daemon vs. Windows hosts) in operator docs.

## Post-Pilot (gated expansions)
- Add `--scenario` flag to the CLI for prompt-based generation that preserves deterministic seeds.
- Introduce `io/importers.py` for DB extract ingestion (Guidewire dumps), preserving seed/manifest audit trails.
- Expand export surfaces to include NDJSON/Parquet and entity filters once checksum validation is in place.
- Publish versioned, signed images with SBOMs and vulnerability scanning in the pipeline.
- Introduce dependency lockfiles and reproducible builds to reduce supply-chain drift.
- Add artifact caching for snapshot generation and internal mirrors for other ecosystems as needed.
- Automate reproducible demo snapshots and make them available as tested artifacts.

## Issues to track
- Add Internal PyPI mirror support in CI (mirror configuration, secrets management, and validation jobs).
- Document approved internal index URL and onboarding steps once the mirror exists.
- Make the demo flow Windows-safe without bash (python-native API start and orchestration).
