# Agentic Workflow Overview

Version: 0.1.0
Last Updated: 2024-05-31

## Directory Map
- `/mop/` – master orchestrator prompt + index
- `/prompts/` – slice prompts (sub-prompts, future, agentic_ai, powerbi_dashboards)
- `/agentic/` – tasks, critic templates, validator scripts
- `/schemas/v0.1/` – YAML definitions for Person, Vehicle, and dataset metadata
- `/src/enterprise_synthetic_data_hub/generation/` – canonical generator orchestration package
- `/src/generator/` – compatibility shim that re-exports the package generator
- `/src/api/` – Flask API aligned with schema + generator
- `/tests/` – regression coverage for schema/generator/API
- `/data/output` – generator outputs
- `/data/static` – reserved for seed files or lookup tables

## Workflow Steps
1. **Analyze** – run repo scan, read the MOP + applicable prompts, record plan.
2. **Execute** – implement cohesive multi-file updates scoped to the selected task.
3. **Validate** – run validator scripts + targeted `pytest` modules.
4. **Critic** – complete the relevant critic checklist(s) and capture findings.
5. **Document** – update docs/prompts/tasks and summarize diffs/tests.

## Agent Tasks
Located in `agentic/tasks/` and versioned individually. Each task lists:
- Required prompts
- Validators + critics to run
- Output expectations (diff summary, logs, TODOs)

## Validators & Critics
- Validators live in `agentic/validators` and are runnable via `python <file>`.
- Critics are markdown checklists (`agentic/critic/*.md`) referenced in PRs.

## Version Rules
- Schema version currently `v0.1`; keep generator/API references in sync.
- Increment agent task or prompt versions when instructions change.
- Document version bumps in commit/PR summaries.

## Running Agent Tasks
1. Choose a task file (e.g., `task_full_pipeline.md`).
2. Follow the Analyze → Execute → Validate instructions.
3. Run the required validators/tests listed in the task.
4. Complete the critic checklist(s) and attach findings to the PR.

## MOP Interaction
- The MOP describes governance + required directories.
- `mop/index.yaml` provides machine-readable mapping for orchestrators.
- Sub-prompts reference validators and critics so automated agents can compose
  multi-step workflows safely.
