# Pilot Charter — Enterprise Synthetic Data Hub (POC)

## Purpose
The Pilot validates that the Enterprise Synthetic Data Hub delivers deterministic, audit-ready synthetic data bundles while staying aligned with the January 2026 baseline and current repo behavior.

## January 2026 baseline (reference)
- **Generator**: Rules-based, deterministic generation that bundles Persons/Vehicles/Profiles with `synthetic_source` markers.
- **CLI**: `generate-snapshot` with entity scoping (`--entity-filter`) and output selection (`--output-format` for csv/json/ndjson/parquet).
- **API**: `/healthz` and `/generate/*` endpoints with optional `ESDH_API_KEY` middleware (env-var only; no hard-coded secrets).
- **Exports**: CSV/JSON/NDJSON/Parquet artifacts plus manifests with SHA-256 checksums and entity stats.
- **Demo**: `scripts/run_demo_flow.py` writes `demo_flow_log.jsonl`; `make demo-gate` orchestrates validation/smoke runs.
- **Testing & CI**: pytest smoke/perf/golden snapshots; `publish-snapshot.yml` auto-publishes artifacts.
- **Governance**: PII policy, demo readiness modes, and chartered Pilot scope.

## Current repo reality (Pilot POC)
- Deterministic, rules-based generator produces Persons/Vehicles/Profiles with `synthetic_source` markers for reproducibility and auditability.
- CLI `generate-snapshot` supports deterministic seeds and outputs CSV + JSON bundle/metadata with a manifest; additional entity filters and output formats remain Pilot backlog.
- API exposes `/healthz` and `/generate/*` endpoints; auth is intentionally optional for demo environments.
- Demo orchestration relies on `scripts/run_demo_flow.py` and `make demo-gate` to validate demo readiness.
- Testing coverage includes smoke/performance and golden snapshot validation.
- Governance references include demo readiness guidance and governance logs; the standalone PII policy remains a baseline requirement to codify before production.

## Pilot objectives and metrics
- **Auditability**: 100% reproducibility via fixed seeds + manifests; document checksum validation requirements.
- **Reliability**: ≥50% reduction in flaky demo runs versus pre-Pilot baseline.
- **Determinism**: All Pilot flows remain seed-reproducible (no nondeterministic data paths).

## Security best practices (append)
- Use environment variables for secrets only; no hard-coded keys in code or docs (e.g., `ESDH_API_KEY`).
- Keep API authentication optional for demo/POC usage but ensure all production notes point to env-var middleware.
- Validate snapshot manifests with SHA-256 checksums before downstream use.
- Log minimal operational metadata; avoid capturing real or sensitive data in demo logs.

## Post-Pilot expansions (append)
- **DB extracts**: Add `io/importers.py` for Guidewire or similar data dumps, preserving deterministic seeding and audit traces.
- **Scenario prompts**: Introduce scenario templates (e.g., “Fleet Policy with 100 vehicles”) that map to deterministic rules and fixed seeds; host in `agentic/tasks/`.
- **Output formats**: Expand CLI/exporters for `--entity-filter` and `--output-format` (csv/json/ndjson/parquet) once Pilot gating metrics are met.
- **Integrity**: Add SHA-256 checksum validation in manifests for all artifact types.
