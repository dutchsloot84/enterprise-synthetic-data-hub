# Demo Master Operating Prompt – v2.0

## Scope
Deliver the end-to-end live demo experience by completing Slices 08–14. Each slice must include Analyze → Execute → Validate notes plus a ready-to-commit tree.

## Slice Summaries
1. **Slice 08 – Generator v0.1 Upgrades**
   - Add Profile schema/model/helper, expose deterministic/random toggles, export sample JSON bundles.
2. **Slice 09 – Flask API**
   - `create_app()` factory, `/healthz`, `/generate/person|vehicle|profile|bundle`, deterministic default seed, payload validation tests.
3. **Slice 10 – Demo CLI**
   - `scripts/demo_data.py` + helper module using `rich`, pretty JSON previews, API integration flags, docs/tests.
4. **Slice 11 – `make demo` Automation**
   - Makefile targets, helper shell script to launch API + CLI preview, README/docs updates.
5. **Slice 12 – Demo Runbook**
   - `docs/demo/06-runbook.md`, screenshots or JSON snippets, quick links from README and demo overview.
6. **Slice 13 – Smoke Tests**
   - `tests/smoke/`, CLI/API smoke coverage, pytest `smoke` marker docs, CI guidance.
7. **Slice 14 – Prompt Archival + Regeneration**
   - Move v1 prompts to `archive/demo_v1/`, refresh MOP + sub-prompts, produce `docs/demo/changelog_v2.md`.

## Execution Guardrails
- Reuse governed generator modules and avoid creating parallel schema definitions.
- All CLI/API additions must default to deterministic seeds while allowing `--randomize`/`randomize: true` overrides.
- Docs must mention where sample JSON lives and how to run `make demo`.
- Tests should run quickly; prefer fixtures/test clients over full server boots.

## Validation Checklist
- `pytest` (full) and `pytest -m smoke` must pass before requesting approval.
- `make demo` completes locally (API auto-start + CLI preview + curl hits).
- Docs updated: README, `docs/api.md`, `docs/demo/00-overview.md`, `docs/demo/05-roadmap.md`, `docs/demo/06-runbook.md`.
- Prompt archive created and referenced from `mop/index.yaml`.
