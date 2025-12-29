# A-E-V Workflow Explainer
Version: 0.1.0
Last Updated: 2024-06-03

## Why Analyze → Execute → Validate
The POC relies on prompt-driven collaboration between humans and LLM agents. The A-E-V loop standardizes how each slice moves
from idea to governed artifacts, ensuring deterministic outcomes even when multiple contributors touch the repo.

## Analyze
- Review the Master Operating Prompt (`mop/master_orchestrator_prompt.md`) and relevant slice prompt under `prompts/sub-prompts/`.
- Inventory impacted files/directories (schemas, generator modules, CLI, docs).
- Identify validators/critics that must run before sign-off.

## Execute
- Apply code or doc changes with deterministic seeds, naming, and versioning.
- Update prompts/tests/docs when interfaces change (e.g., schema tweaks require README + validator updates).
- Keep commits scoped to a slice/task capsule to preserve traceability.

## Validate
- Run automated checks: `pytest`, `agentic/validators/schema_validator.py`, `generator_validator.py`, `cli_validator.py`,
  `api_validator.py` as applicable.
- Invoke critics from `agentic/critic/` plus the new demo critic to review narrative accuracy.
- Capture validator + critic output inside PR summaries or task capsules.

## Governance Alignment
- Pause-for-approval checkpoints (schemas, generator behavior, dataset version changes) ensure stakeholders review risky moves.
- All prompts include version headers and change logs to maintain deterministic instructions.
- Docs under `/docs/demo` inherit the same discipline: each file lists version + last updated to simplify audits.

## Demo Implications
- We can explain to stakeholders exactly how new work will be proposed, executed, and validated.
- Agentic workflows reduce onboarding time because every task references the same prompts, validators, and critics.
- The critic mesh prevents demo drift: any inaccurate statement is caught before handoff.
