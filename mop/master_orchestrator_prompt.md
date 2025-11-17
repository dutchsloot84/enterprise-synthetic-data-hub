# Master Orchestrator Prompt – v2.0

## Purpose
Deliver a runnable live demo for the Enterprise Synthetic Data Hub by completing Slices 08–14:
1. Generator v0.1 upgrades (Persons + Vehicles + derived Profiles + sample bundles)
2. Local Flask API with `/healthz` and `/generate/*` endpoints
3. Demo CLI with colorful previews + API integration (`scripts/demo_data.py`)
4. `make demo` automation + helper scripts
5. Demo runbook + documentation updates
6. Smoke tests spanning generator, API, and CLI
7. Prompt archival for v1 + regeneration of v2 task prompts

## Workflow Expectations
- **Analyze** the scope for each slice using the matching sub-prompt under `prompts/sub-prompts/`.
- **Execute** code/docs/tests inside the governed package (`src/enterprise_synthetic_data_hub`), `docs/demo`, `scripts/`, and automation layers.
- **Validate** via targeted pytest suites (`pytest`, `pytest -m smoke`), linting, and critic checklists embedded in each sub-prompt.
- Provide ready-to-commit file trees in slice notes so reviewers know what to expect.

## Governance & Pauses
- Do **not** change schema contracts without updating the YAML definitions, Pydantic models, and validators.
- Pause and request approval before altering API route signatures, CLI UX commitments, or dataset versions.
- Archive all prior prompts under `archive/demo_v1/` and keep v2 prompts synchronized with `mop/index.yaml`.
- Maintain deterministic defaults (seed from settings) while allowing `randomize` overrides for demo flair.

## Required Artifacts Per Slice
1. **Generator / Profiles** – new schema, Pydantic model, derived profile helper, sample JSON under `data/demo_samples/v0.1/`.
2. **Flask API** – `create_app()` factory, `/healthz`, `/generate/person|vehicle|profile|bundle`, unit tests.
3. **Demo CLI** – `scripts/demo_data.py` shim + helper module using `rich`, docs, tests.
4. **make demo** – Makefile targets, `scripts/demo_start_api.sh`, docs describing automation + expected output.
5. **Runbook** – `docs/demo/06-runbook.md`, README links, API/CLI screenshots if applicable.
6. **Smoke Tests** – `tests/smoke/` suite, CLI smoke coverage, pytest marker docs.
7. **Prompt Archive** – `archive/demo_v1/...`, refreshed MOP + sub-prompts for v2, `docs/demo/changelog_v2.md` summarizing deltas.

## Definition of Done
- `pytest` + `pytest -m smoke` pass locally.
- Docs (`docs/api.md`, `docs/demo/**`, README) describe the new workflow end-to-end.
- `make demo` completes without manual intervention (API auto-start + CLI/API previews).
- Sample JSON bundles exist under `data/demo_samples/v0.1/` for decks/talking points.
- All prompt updates are versioned and linked from `mop/index.yaml`.
