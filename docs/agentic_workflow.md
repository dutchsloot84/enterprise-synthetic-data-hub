# Agentic Workflow Overview

Version: 0.1.1
Last Updated: 2026-01-06

## Directory Map
- `/mop/` – master orchestrator prompt + index
- `/prompts/` – slice prompts (sub-prompts, future, agentic_ai, powerbi_dashboards)
- `/agentic/` – tasks, critic templates, validator scripts
- `/schemas/v0.1/` – YAML definitions for Person, Vehicle, Profile, and metadata
- `/src/enterprise_synthetic_data_hub/generation/` – canonical generator orchestration package
- `/src/generator/` – compatibility shim that re-exports the package generator
- `/src/enterprise_synthetic_data_hub/api/` – Flask API aligned with schema + generator
- `/src/api/` – compatibility shim for API entrypoints
- `/tests/` – regression coverage for schema/generator/API/demo flow
- `/data/output/` – generator outputs (sample dataset + metadata JSON)
- `/data/snapshots/<version>/` – governed CSV/JSON bundles emitted by the CLI/exporter
- `/data/demo_runs/` – timestamped demo flow artifacts produced by the orchestrator
- `/data/demo_samples/` – canned demo payloads and regeneration instructions
- `/data/static/` – reserved for seed files or lookup tables

## Workflow Steps
1. **Analyze** – run repo scan, read the MOP + applicable prompts, record plan.
2. **Execute** – implement cohesive multi-file updates scoped to the selected task.
3. **Validate** – run validator scripts + targeted `pytest` modules.
4. **Export** – invoke `python -m enterprise_synthetic_data_hub.cli.main generate-snapshot` when CLI behavior changes to refresh governed artifacts.
5. **Critic** – complete the relevant critic checklist(s) and capture findings.
6. **Document** – update docs/prompts/tasks and summarize diffs/tests.

## Agent Tasks
Located in `agentic/tasks/` and versioned individually. Each task lists:
- Required prompts
- Validators + critics to run
- Output expectations (diff summary, logs, TODOs)

## Validators & Critics
- Validators live in `agentic/validators` and are runnable via `python <file>`.
- Current validator entry points:
  - `python agentic/validators/schema_validator.py`
  - `python agentic/validators/generator_validator.py`
  - `python agentic/validators/cli_validator.py`
  - `python agentic/validators/api_validator.py`
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
