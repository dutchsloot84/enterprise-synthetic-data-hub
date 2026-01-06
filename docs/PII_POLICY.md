# Synthetic Data PII + Compliance Guardrails

## Principles
- **Synthetic-only generation**: Persons, Vehicles, and Profiles are produced from deterministic rules and curated lookups—no production inputs or user uploads.
- **Provenance marker**: Every entity carries `synthetic_source="enterprise-synthetic-data-hub v0.1"`; validators assert its presence.
- **Determinism**: Default seed **20240601** plus manifests with SHA-256 checksums and stats enable tamper detection and reproducibility.
- **Scoped access**: Demo API supports optional API key protection via the `ESDH_API_KEY` environment variable (header `X-API-Key`). Intended for controlled QA/demo use only.

## Handling Rules
- Treat outputs as governed test fixtures; never merge with production PII or customer data lakes.
- Keep artifacts under repo-relative `data/` paths or the published GitHub releases to maintain checksum visibility.
- When using randomized seeds, record the effective seed surfaced in CLI/API output to preserve reproducibility.
- Do not email raw artifacts; share via release downloads or signed channels that preserve manifests.
- Retain synthetic markers when downstream systems transform or subset the data.

## Verification
- Run `make demo-validate` (or `python scripts/demo_validate.py`) to confirm schema alignment and synthetic markers.
- Inspect `snapshot_manifest_*.json` for checksums, record counts, and stats before distributing artifacts.
- For API scenarios, hit `/healthz` to verify default seed and generation plan, then call `/generate/bundle` to confirm markers and counts.

## Escalation & Hardening
- If tighter controls are required, front the API with standard authentication, rotate seeds per environment, and log access.
- Apply enterprise container guidance in `docs/DOCKER_ENTERPRISE.md` when TLS inspection or private mirrors are mandated.
- Avoid long-term retention beyond demo scope; regenerate deterministically as needed.
