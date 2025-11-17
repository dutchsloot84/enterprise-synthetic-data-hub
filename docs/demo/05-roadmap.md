# Roadmap – Phase 2 and Beyond
Version: 0.1.0
Last Updated: 2024-06-03

## Guiding Principles
1. Preserve deterministic, governed snapshots while expanding coverage.
2. Reuse the existing prompts, validators, and critics to keep contributions consistent.
3. Deliver value incrementally (API, analytics, automation) without breaking v0.1 contracts.

## Near-Term (Phase 2)
| Workstream | Description | Dependencies |
| --- | --- | --- |
| API Hardening | Finish Flask endpoints in `src/enterprise_synthetic_data_hub/api/`, align payloads with governed CSV layout, and add auth stubs. | Slice 06 scaffolding, schema stability. |
| Distribution Strategy | Automate publishing snapshots to S3/Snowflake and add checksum validation in manifests. | Generator v0.1 outputs, IO/exporter enhancements. |
| Expanded Validators | Add CLI regression tests, data drift detection, and CI hooks invoking `agentic/validators/*.py`. | Existing validator scripts, GitHub Actions wiring. |
| Power BI & Analytics | Build dashboards using governed CSVs (see `future/powerbi_dashboards/`). | Stable exports, metadata enrichment. |

## Mid-Term (Phase 3)
- Add Policy/Claim schemas once Person/Vehicle usage patterns solidify.
- Introduce multiple snapshot versions (v0.2+) with backward-compatible manifest schemas.
- Layer in scenario templates for QA automation harnesses.

## Long-Term Vision
- Deliver Synthetic Data as a Service: authenticated API, event-driven refreshes, and integration with Mobilitas/CSAA toolchains.
- Embed agentic co-pilots that can reason over prompts, run validators, and propose changes autonomously using the same A-E-V
  workflow.

## Call to Action
To unlock Phase 2 we need:
1. Approval to continue prompt-driven development with shared validators.
2. Sponsorship for cloud distribution (S3 or Snowflake) and dashboard hosting.
3. Dedicated QA + data engineering support to extend schemas and test harnesses.
