# Agent Task – API Update
Version: 0.1.0
Source Prompt: prompts/sub-prompts/06_api_layer.md

## Goal
Introduce or update API endpoints that expose generated data, ensuring versioned
paths and schema compliance.

## Workflow
1. **Analyze**
   - Scan `/src/api` and `/schemas` for current contracts.
   - Review API docs + tests.
2. **Plan**
   - Document endpoint changes, query params, and response payloads.
   - Determine data dependencies + validator coverage.
3. **Execute**
   - Implement routes/controllers + update imports.
   - Keep `API_VERSION` sourced from config or schema metadata.
4. **Validate**
   - `python agentic/validators/api_validator.py`
   - `pytest tests/test_api.py`
5. **Critic**
   - Complete `agentic/critic/api_critic.md`.
6. **Document**
   - Update `/docs/api.md` or relevant guides.
   - Summarize diffs + validation outcomes.

## Required Outputs
- Updated API code + docs
- Validator/test logs
- Critic summary
