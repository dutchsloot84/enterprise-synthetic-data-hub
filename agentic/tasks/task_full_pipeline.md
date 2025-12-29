# Agent Task – Full Pipeline Workflow
Version: 0.1.0
Source Prompts: 00–06 (see `mop/index.yaml`)

## Goal
Execute Plan → Implement → Validate → Document workflow that spans schema,
generator, validation, and API surfaces.

## Multi-step Workflow
1. **Plan**
   - Perform repo scan (dir + dependency list).
   - Select relevant slice prompts; note validator + critic coverage.
   - Produce task breakdown with owners/timestamps.
2. **Implement**
   - Update schemas/generator/API/tests/docs per plan.
   - Keep commits scoped but multi-file when necessary.
3. **Validate**
   - Run all touched validators (`agentic/validators/*`).
   - Execute `pytest` modules covering modified code.
   - Capture outputs in task log.
4. **Critic**
   - Run repo critic plus any scoped critics.
   - Summarize findings + remediation steps.
5. **Document**
   - Update `/docs/agentic_workflow.md` (or relevant files) when workflows
     change.
   - Provide final diff summary referencing files + tests.

## Required Validators
- `python agentic/validators/schema_validator.py`
- `python agentic/validators/generator_validator.py`
- `python agentic/validators/cli_validator.py`
- `python agentic/validators/api_validator.py`
- Additional validators/tests as needed per modifications.

## Critic Hooks
- `agentic/critic/repo_critic.md` (always)
- Add schema/generator/api critics based on touched components.

## Outputs
- Completed checklist stored with PR/task notes
- Links to validator + critic logs
- Follow-up backlog items if gaps remain
