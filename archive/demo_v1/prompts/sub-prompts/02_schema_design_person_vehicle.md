# Slice 02 – Schema Design (Person + Vehicle)
Version: 0.1.0
Last Updated: 2024-05-31

## Purpose
Define and evolve YAML schemas for Person and Vehicle data models that align
with the generator + API contracts.

## Analyze – Repo Awareness
- Inspect `/schemas/v0.1/*.yaml` for current field definitions.
- Check `tests/test_schema_validation.py` expectations.
- Note any downstream consumers (generator/API/tests) referencing schema fields.

## Plan – Multi-step Reasoning
- Document planned schema changes, expected impacts, and migration steps.
- Determine whether new versions or minor patches are required.
- Identify which validators (`schema_validator.py`) and critics
  (`schema_critic.md`) must run.

## Execute – Implementation Notes
- Update YAML definitions with descriptions, types, constraints, and enums.
- Maintain `version`, `last_updated`, and `field_count` metadata at the top of
  each schema file.
- If new versions are created, replicate directory structure under
  `/schemas/<version>/` and update docs/tests accordingly.

## Validate – Required Steps
- `python agentic/validators/schema_validator.py`
- `pytest tests/test_schema_validation.py`
- Run `agentic/critic/schema_critic.md` to capture results.

## Final Diff Report Checklist
- Schema files modified + reasons
- Version impact statement
- Validator/test/critic outputs
