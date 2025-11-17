# Slice 00 – Repository Restructure for Agentic Workflow
Version: 0.1.0
Last Updated: 2024-05-31

## Purpose
Upgrade the repository so GPT-5.1-capable agents can perform multi-step
workflows, maintain critic coverage, and keep schemas/generator/API assets
aligned.

## Analyze – Repo Awareness
1. `ls` the repo root and note folders missing from the required structure.
2. Inspect `mop/`, `prompts/`, and `agentic/` to understand available tasks and
   critics.
3. Capture current schema + generator locations (legacy paths still exist under
   `src/enterprise_synthetic_data_hub`).
4. Map all docs that describe workflows so updates remain in sync.

## Plan – Multi-step Reasoning
- Draft a step-by-step plan covering directory creation, prompt migration, and
  documentation updates.
- Define which files will be touched and which validators/critics must run.
- Call out blockers or pause-for-approval items before editing anything.

## Execute – Implementation Notes
- Create the `/mop`, `/prompts`, and `/agentic` tree exactly as defined in the
  MOP. Preserve legacy files if still referenced.
- Update prompts to use AEV + critic references and to include repo scan
  guidance.
- Ensure schema/generator/API references point to the new canonical paths.

## Validate – Required Steps
- Run `python agentic/validators/schema_validator.py` to confirm schema files
  exist and match the version stub.
- Run `python agentic/validators/generator_validator.py` to ensure the new
  generator can be imported and produces aligned columns.
- Run `python agentic/validators/api_validator.py` or `pytest tests/test_api.py`
  after touching API files.

## Critic Hooks
- Always include `agentic/critic/repo_critic.md` after structural changes.
- Include `schema_critic.md` if schema directories or files moved.

## Final Diff Report
Summarize:
- New directories/files
- Updated prompts/docs
- Validator + critic results
