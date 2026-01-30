# Security Best Practices

## Principles
- **No hard-coded secrets**: store API keys or tokens only in environment variables (e.g., `ESDH_API_KEY`).
- **Optional authentication**: keep auth middleware optional for POC/demo workflows; ensure production guidance uses env-var configuration only.
- **Artifact integrity**: publish and validate SHA-256 checksums for manifests and exported artifacts before downstream use.
- **Deterministic generation**: preserve seed-based reproducibility to support audit trails and verification.
- **Least privilege by default**: avoid exposing write-enabled endpoints beyond local demo scope.
- **Log hygiene**: log metadata, not payloads; never include real or sensitive information in demo logs.

## Recommended validations
- Verify checksum manifests during `make demo-gate` or CI smoke runs.
- Confirm API authentication behavior via `ESDH_API_KEY` in non-demo environments.
- Track reproducibility metrics (seed + manifest) alongside Pilot KPIs.
