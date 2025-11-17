# Master Operating Prompt (MOP) – Enterprise Synthetic Data POC

## Purpose
Guide LLM agents and human collaborators working inside the
`enterprise-synthetic-data-hub` repository. This POC targets a stable snapshot of
~200 synthetic Person + Vehicle records for CSAA/Mobilitas QA teams.

## Agentic Mode (GPT-5.1)
- **Repo Scan First** – every task begins with a lightweight inventory of
  directories, naming conventions, schema files, generator modules, APIs, and
  tests. Capture discoveries in the task notes.
- **Plan → Execute → Validate → Document** – write the plan before editing
  files, execute cohesive multi-file updates, validate with automated critic
  checks plus tests, then document what changed.
- **Task Capsules** – each agent task inside `/agentic/tasks` is versioned,
  self-contained, and references the authoritative prompts + schemas.
- **Critic Mesh** – all multi-file changes must call at least one critic under
  `/agentic/critic` and capture findings in the PR summary.
- **Validator Hooks** – schema, generator, and API validators live under
  `/agentic/validators` and should run in CI or locally when relevant files are
  touched.

## Key Constraints & Decisions
- Scope: **Persons + Vehicles only** (no Policy/Claim yet).
- Dataset behavior: **single deterministic snapshot** stored under
  `data/snapshots/<version>/`.
- Generation style: **rule-based, privacy-safe**, realistic formats (VIN, DL).
- IDs: `person_id` and `vehicle_id` must be UUID/GUID strings.
- Cross-LOB metadata: include `lob_type` on both Person and Vehicle records.
- Governance: follow lightweight rules in `/governance`.
- Repository structure must retain `/mop`, `/prompts`, `/agentic`, `/schemas`,
  `/src`, `/tests`, `/data`, and `/docs`.
- Agent tasks, prompts, docs, and validators each maintain semantic version
  notes within the file header (e.g., `Version: 0.1.0`).

## Directory Index
- `/mop/master_orchestrator_prompt.md` – this document.
- `/mop/index.yaml` – machine-readable reference for agents/orchestrators.
- `/prompts/sub-prompts` – actionable slice prompts with AEV + critic guidance.
- `/agentic/tasks` – composable agent workflows such as
  `task_full_pipeline.md`.
- `/agentic/critic` – critic lenses for schema/generator/api/repo.
- `/agentic/validators` – executable validator scripts (callable via Python).
- `/schemas/v0.1` – authoritative YAML schemas for person + vehicle.
- `/src/generator` – standalone generator entry points that wrap the package.
- `/src/api` – API surfaces aligned with generator outputs.
- `/tests` – regression coverage for schemas, generators, APIs, validators.
- `/docs` – repo maps, workflow descriptions, and runbooks.

## AEV Workflow (Analyze → Execute → Validate)
1. **Analyze**
   - Perform repo scan + dependency inspection.
   - Select the relevant sub-prompt under `prompts/sub-prompts/`.
   - Summarize plan, including critic + validator hooks, for review.
2. **Execute**
   - Apply multi-file updates per plan.
   - Keep naming/versioning consistent with schemas + data outputs.
   - Update `agentic/tasks` or prompts when workflows change.
3. **Validate**
   - Run validators/tests tied to touched artifacts.
   - Invoke applicable critic template(s) and record findings.
   - Produce diff summary + follow-up actions.

## Pause-for-Approval Checkpoints
- Schema modifications (Person, Vehicle, metadata).
- Generator rule changes that affect business meaning.
- Updates altering dataset versions or snapshot counts.
- New external data export surfaces (API, Power BI, etc.).
- Breaking changes to agentic workflows or validators.

## Critic Role
- Schema critic validates structure, enumerations, and version alignment.
- Generator critic checks field coverage, deterministic rules, and seed usage.
- API critic ensures routes follow naming, versioning, and dependency rules.
- Repo critic confirms directories/prompts/docs remain in sync.

## Agent Task Versioning Rules
- Each task doc starts with `Version: x.y.z` and a change log.
- Increment the **minor** version when steps change; patch when clarifying
  language; major for breaking workflow updates.
- Reference the originating prompt version and validator requirements.

## Sub-Prompts (Agentic)
Use the following slices as needed:
- `00_restructure_for_agentic_workflow.md`
- `01_pipeline_scaffold.md`
- `02_schema_design_person_vehicle.md`
- `03_generator_v0.1.md`
- `04_validation_suite.md`
- `05_cli_and_usage_examples.md`
- `06_api_layer.md`
- Future prompts live in `prompts/future/`
- AI-augmentation + dashboards under `prompts/agentic_ai/` and
  `prompts/powerbi_dashboards/`

Each sub-prompt embeds the enhanced AEV pattern, repo-awareness checklist, and
critic triggers tailored to that slice. Reference them explicitly in task notes,
PR descriptions, and in `agentic/tasks/*` workflows.
