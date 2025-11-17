# Agent Task – Schema Update
Version: 0.1.0
Source Prompt: prompts/sub-prompts/02_schema_design_person_vehicle.md

## Goal
Evolve Person/Vehicle schemas while maintaining compatibility with generator,
API, and tests.

## Workflow
1. **Analyze**
   - Run repo scan noting current schema version directories.
   - Review open PRs/docs referencing schemas.
2. **Plan**
   - List targeted fields, rationale, and downstream impacts.
   - Decide whether change is patch/minor/major per MOP rules.
3. **Execute**
   - Update YAML under `/schemas/<version>/`.
   - Propagate changes to generator/API/tests as needed.
4. **Validate**
   - `python agentic/validators/schema_validator.py`
   - `pytest tests/test_schema_validation.py`
5. **Critic**
   - Complete `agentic/critic/schema_critic.md`.
6. **Document**
   - Update `/docs` + prompt footers if instructions changed.
   - Summarize diffs + validator outputs.

## Required Outputs
- Updated schemas with version metadata
- Validation logs
- Critic summary + follow-up tasks
