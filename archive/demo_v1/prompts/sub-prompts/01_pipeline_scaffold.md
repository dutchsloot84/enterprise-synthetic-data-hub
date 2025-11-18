# Slice 01 – Pipeline Scaffold
Version: 0.1.0
Last Updated: 2024-05-31

## Purpose
Align ingestion, generation, validation, and export directories with the
agentic workflow so multi-step tasks can run end-to-end.

## Analyze – Repo Awareness
- List the current `src/` modules that participate in ingestion/generation.
- Identify tests touching those modules.
- Review `agentic/tasks` to understand required integration points.

## Plan – Multi-step Reasoning
1. Map pipeline stages (ingest → enrich → validate → export).
2. For each stage, identify file(s) to edit/create.
3. Decide which validators and critics prove the scaffold works.
4. Outline doc/prompts updates needed to keep instructions synchronized.

## Execute – Implementation Notes
- Create/update generator wrappers in `/src/generator`.
- Document dependencies and run instructions in `/docs` or prompt footers.
- Keep naming + version strings consistent with `/schemas/v0.1` and `/data`.

## Validate – Required Steps
- `python agentic/validators/generator_validator.py`
- `pytest tests/test_generator.py`
- Trigger `agentic/critic/generator_critic.md` to capture findings.

## Final Diff Report Checklist
- Files touched per pipeline stage
- Validator/test output
- Critic notes + any TODOs
