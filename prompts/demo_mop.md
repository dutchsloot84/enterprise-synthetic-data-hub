# Demo Master Orchestrator Prompt (MOP) – Synthetic Data POC
Version: 0.1.0
Last Updated: 2024-06-03

## Objective
Coordinate the deterministic generation of all demo-ready artifacts for the Enterprise Synthetic Data Hub. The demo MOP ensures
that every narrative, slide, and explainer aligns with the completed Slices 01–07, the governed generator v0.1, and the
agentic A-E-V workflow that already powers the repository.

## Responsibilities
1. **Repo Context Refresh** – Scan `README.md`, `/docs`, `/schemas`, `/src`, `/prompts`, and `/governance` before drafting any
demo materials. Capture notable updates (e.g., generator rules, validator coverage, CLI behavior).
2. **Sub-Prompt Invocation** – Sequentially call:
   1. `/prompts/sub-prompts/demo_generate_artifacts.md`
   2. `/prompts/sub-prompts/demo_generate_slides.md`
   3. `/prompts/sub-prompts/demo_generate_talking_points.md`
   4. `/prompts/sub-prompts/demo_generate_narrative.md`
3. **A-E-V Loop** – For each sub-prompt run:
   - **Analyze** the repository facts tied to that artifact.
   - **Execute** the writing task and save deterministic markdown output under `/docs/demo/**`.
   - **Validate** by re-reading the new artifact for alignment with schemas, generator behavior, and slice objectives.
4. **Critic Enforcement** – After all artifacts exist, run `/prompts/sub-prompts/demo_critic_check.md`. Apply any fixes it
requires before finalizing the demo bundle.
5. **Commit-Ready Output** – Ensure files land exactly in:
   - `/docs/demo/00-overview.md`
   - `/docs/demo/01-architecture.md`
   - `/docs/demo/02-slice-summary.md`
   - `/docs/demo/03-generator-v0.1.md`
   - `/docs/demo/04-aev-explainer.md`
   - `/docs/demo/05-roadmap.md`
   - `/docs/demo/slides/deck.md`
   - `/docs/demo/talking-points/presenter_script.md`

## Deterministic Narrative Rules
- Reuse canonical terminology from README, schemas, and prompts (Persons, Vehicles, governed snapshots, v0.1 generator).
- Describe Slices 01–07 factually: scaffold, pipeline, schemas, generator, validation, CLI/export, API alignment, and demo prep.
- Do not invent new capabilities (e.g., no cloud deployment, no ML-based generation yet).
- Each artifact must read as a finished deliverable with headings, tables/bullets where appropriate, and no TODOs.

## Validation Checklist
- [ ] All demo docs exist with non-empty content.
- [ ] Slide deck covers overview, architecture, workflow, generator showcase, roadmap, and CTA.
- [ ] Presenter script mirrors slide ordering and embeds speaker cues.
- [ ] Executive narrative summarizes purpose, impact, and next steps.
- [ ] Critic findings resolved.
- [ ] Files contain only repository-accurate statements.
