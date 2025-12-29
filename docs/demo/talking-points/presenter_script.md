# Presenter Script – Synthetic Data POC Demo
Version: 0.1.0
Last Updated: 2024-06-03

## Opening (Slide 1)
- **Timebox: 1 minute.**
- "Hi everyone, I’m walking you through the Enterprise Synthetic Data Hub, a two-week sprint that now gives Mobilitas and CSAA a governed way to share synthetic Persons and Vehicles."
- Reinforce that the generator, prompts, and validators are production-grade even though this is a POC.

## Slide 2 – Why Synthetic Data Now
- Highlight current pain: disparate spreadsheets, inconsistent fixtures, privacy concerns.
- Explain that the governed snapshot under `data/snapshots/v0.1` replaces ad-hoc files with a single manifest-driven dataset.

## Slide 3 – Architecture Overview
- Point to prompts/governance first: "Every change starts with the Master Operating Prompt and slice sub-prompts."
- Walk left-to-right: prompts → agentic tasks → core package → outputs.
- Mention validators (`agentic/validators/*.py`) and critics that keep the repo aligned.

## Slide 4 – Slice Journey
- Spend ~30 seconds per slice theme.
- Emphasize determinism thread: scaffolding → schemas → generator → validation → CLI → API → demo.
- Call out that Slice 07 (this work) packages the story for leadership without touching code.

## Slide 5 – Generator Spotlight
- Describe CLI command and deterministic seed flag.
- Mention `snapshot_manifest_v0_1.json` as the artifact auditors love.
- Offer optional live demo: run the CLI to show file outputs if time permits.

## Slide 6 – A-E-V & Governance
- Explain how Analyze → Execute → Validate works in practice using prompts and validators.
- Remind audience of pause-for-approval checkpoints (schemas, generator logic, version bumps).
- Tie the new demo critic into this story as proof of self-policing documentation.

## Slide 7 – Roadmap & CTA
- Outline Phase 2 priorities: API hardening, automated distribution, expanded validators, Power BI dashboards.
- Phase 3 glimpse: Policy/Claim schemas and multi-version snapshots.
- Close with ask: sponsorship + dedicated QA/data engineering support to operationalize the hub.

## Anticipated Q&A
1. **How hard is it to add a new entity (e.g., Policy)?** – Update schemas in `schemas/v0.1`, extend Pydantic models, add generator rules, update validators/tests; prompts guide each step.
2. **Can we trust the data for audits?** – Yes; manifest + metadata JSON capture generation parameters, and validators are part of the PR checklist.
3. **What about real-time APIs?** – Slice 06 set up the Flask scaffold; Phase 2 funding lets us align responses with governed CSV outputs and add auth/logging.

## Closing
- Reiterate that the hardest part—governed scaffolding and deterministic generator—is done.
- Thank stakeholders and invite them to stay for a CLI walkthrough or review the docs under `docs/demo/`.
