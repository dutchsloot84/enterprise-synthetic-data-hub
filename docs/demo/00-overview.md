# Demo Overview – Enterprise Synthetic Data Hub
Version: 0.1.1
Last Updated: 2026-01-06

## Executive Narrative
CSAA / Mobilitas QA teams asked for a privacy-safe way to exercise insurance workflows without juggling brittle spreadsheets.
Over two focused weeks we stood up the Enterprise Synthetic Data Hub: a governed, deterministic generator that produces a
snapshot of Persons, Vehicles, and derived Profiles stored under `data/snapshots/v0.1`. The POC codifies schemas, prompts, and
validator hooks so future engineers—or LLM copilots—can extend it without relearning the domain.

The demo showcases how the repository’s scaffolding, prompts, and tests work together. The generator in
`src/enterprise_synthetic_data_hub/generation/` uses rule-based logic plus deterministic seeds so QA can reproduce every record.
CLI exports and manifest writers produce governed CSV + JSON bundles that mirror the schemas defined in
`schemas/v0.1`. Validators under `agentic/validators/` keep the data trustworthy, while the Master Operating Prompt
orchestrates Analyze → Execute → Validate loops for human + agent contributors.

With the foundations in place, the repo now ships a runnable demo: a local Flask API (`/healthz`, `/generate/*`), a colorful
CLI (`scripts/demo_data.py`), curated JSON samples under `data/demo_samples/v0.1/`, and automation (`make demo`) plus a runbook
and demo profile configuration (`config/demo.yaml`) to narrate the flow. The orchestration script (`scripts/run_demo_flow.py`)
collects snapshots into `data/demo_runs/` for easy handoff and audit trails.

## Audience & Use Cases
- QA and UAT engineers who need consistent, governed Person + Vehicle records.
- Data platform stakeholders evaluating Synthetic Data as a Service.
- Engineering leadership reviewing A-E-V agentic workflows for future slices.

## Success Indicators (Slices 01–14)
- ✅ Stable repo scaffolding with prompts, governance, schemas, and validators.
- ✅ Generator v0.1 producing linked Person/Vehicle/Profile bundles + sample JSON exports.
- ✅ CLI exports, demo CLI previews, and manifest writers aligned with schema definitions.
- ✅ Local Flask API + smoke tests verifying `/generate/*` endpoints.
- ✅ Agentic prompts + critics (v2) ready for human/LLM collaboration.

## Demo Assets
| Artifact | Path |
| --- | --- |
| Architecture explainer | `docs/demo/01-architecture.md` |
| Slice-by-slice summary | `docs/demo/02-slice-summary.md` |
| Generator deep dive | `docs/demo/03-generator-v0.1.md` |
| A-E-V workflow explainer | `docs/demo/04-aev-explainer.md` |
| Roadmap | `docs/demo/05-roadmap.md` |
| Demo runbook | `docs/demo/06-runbook.md` |
| API reference | `docs/api.md` |
| Slide deck | `docs/demo/slides/deck.md` |
| Presenter script | `docs/demo/talking-points/presenter_script.md` |
