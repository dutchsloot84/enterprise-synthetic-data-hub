# Demo Overview – Enterprise Synthetic Data Hub
Version: 0.1.0
Last Updated: 2024-06-03

## Executive Narrative
CSAA / Mobilitas QA teams asked for a privacy-safe way to exercise insurance workflows without juggling brittle spreadsheets.
Over two focused weeks we stood up the Enterprise Synthetic Data Hub: a governed, deterministic generator that produces a single
snapshot of Persons and Vehicles stored under `data/snapshots/v0.1`. The POC codifies schemas, prompts, and validator hooks so
future engineers—or LLM copilots—can extend it without relearning the domain.

The demo showcases how the repository’s scaffolding, prompts, and tests work together. The generator in
`src/enterprise_synthetic_data_hub/generation/` uses rule-based logic plus deterministic seeds so QA can reproduce every
record. CLI exports and manifest writers produce governed CSV + JSON bundles that mirror the schemas defined in
`schemas/v0.1`. Validators under `agentic/validators/` keep the data trustworthy, while the Master Operating Prompt
orchestrates Analyze → Execute → Validate loops for human + agent contributors.

With the foundations in place, we are ready to expose the dataset through the Flask API stubs, harden validators, and deliver
Power BI insights without re-architecting. Funding Phase 2 unlocks multi-snapshot support, automated distribution, and agentic
extensions that reuse today’s governance guardrails.

## Audience & Use Cases
- QA and UAT engineers who need consistent, governed Person + Vehicle records.
- Data platform stakeholders evaluating Synthetic Data as a Service.
- Engineering leadership reviewing A-E-V agentic workflows for future slices.

## Success Indicators (Slice 01–07)
- ✅ Stable repo scaffolding with prompts, governance, schemas, and validators.
- ✅ Deterministic generator v0.1 producing ~200 linked Person/Vehicle pairs.
- ✅ CLI exports and manifest writers aligned with schema definitions.
- ✅ Agentic prompts + critics ready for human/LLM collaboration.

## Demo Assets
| Artifact | Path |
| --- | --- |
| Architecture explainer | `docs/demo/01-architecture.md` |
| Slice-by-slice summary | `docs/demo/02-slice-summary.md` |
| Generator deep dive | `docs/demo/03-generator-v0.1.md` |
| A-E-V workflow explainer | `docs/demo/04-aev-explainer.md` |
| Roadmap | `docs/demo/05-roadmap.md` |
| Slide deck | `docs/demo/slides/deck.md` |
| Presenter script | `docs/demo/talking-points/presenter_script.md` |
