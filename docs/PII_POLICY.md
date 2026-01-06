# Synthetic Data PII + Compliance Guardrails

This proof-of-concept intentionally avoids real PII and includes lightweight governance hooks for demos and QA. Key points:

- **Synthetic-only inputs**: All entities (Persons, Vehicles, Profiles) are created from deterministic rules and curated lookup tables. No production data, user uploads, or external feeds are referenced.
- **Governance marker**: Every record carries `synthetic_source` (see `config/settings.py`). Validators and smoke tests assert its presence across entities to make provenance explicit.
- **Anonymization stance**: Although data are fabricated, fields mirror real-world schemas (e.g., names, addresses, VINs). Treat outputs as test fixtures. Do not mingle with production PII or customer data lakes.
- **Determinism + auditability**: Seeds default to `20240601`; optional `--randomize` is logged. Manifests now include checksums and entity-level statistics (age + VIN distributions) to spot drift or tampering.
- **API access control**: Demo API supports an optional API key via `ESDH_API_KEY` (header `X-API-Key`). This is not production security, but discourages accidental exposure.
- **Export hygiene**: CSV/JSON/NDJSON/Parquet outputs stay in repo-relative `data/` paths. Use GitHub Actions release artifacts for controlled sharing rather than emailing files.

If you need tighter controls (data retention, DSR handling, or access logs), front the API with standard authentication and rotate seeds/keys per environment.
