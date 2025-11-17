# Agent Task – Generator Update
Version: 0.1.0
Source Prompt: prompts/sub-prompts/03_generator_v0.1.md

## Goal
Modify the synthetic generator to support new rules, fields, or outputs while
maintaining determinism and schema alignment.

## Workflow
1. **Analyze**
   - Repo scan focusing on `/src/enterprise_synthetic_data_hub/generation` (plus `/src/generator` shim).
   - Inspect `/data/output` for current artifacts.
2. **Plan**
   - Document rule changes, seeds, and affected schemas/tests.
   - Identify validator + critic coverage.
3. **Execute**
   - Update generator code, metadata, and docs.
   - Regenerate sample output + metadata JSON under `data/output/` if necessary.
4. **Validate**
   - `python agentic/validators/generator_validator.py`
   - `pytest tests/test_generator.py`
5. **Critic**
   - Complete `agentic/critic/generator_critic.md`.
6. **Document**
   - Update prompts/docs referencing generator behavior.
   - Summarize outputs + TODOs.

## Required Outputs
- Updated code + sample data metadata
- Validator/test results
- Critic insights
