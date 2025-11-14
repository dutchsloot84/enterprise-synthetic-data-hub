# Master Operating Prompt (MOP) – Enterprise Synthetic Data POC

## Purpose
Guide LLM agents and human collaborators while working inside the
`enterprise-synthetic-data-hub` repository. This POC targets a stable snapshot of
~200 synthetic Person + Vehicle records for CSAA/Mobilitas QA teams.

## Key Constraints & Decisions
- Scope: **Persons + Vehicles only** (no Policy/Claim yet).
- Dataset behavior: **single deterministic snapshot** stored under
  `data/snapshots/<version>/`.
- Generation style: **rule-based, privacy-safe**, realistic formats (VIN, DL).
- IDs: `person_id` and `vehicle_id` must be UUID/GUID strings.
- Cross-LOB metadata: include `lob_type` on both Person and Vehicle records.
- Governance: follow lightweight rules in `/governance`.
- No API yet, but keep folder reserved for future implementation.
- Consumers receive full Person + Vehicle profiles.
- Prompt workflow: **Analyze → Execute → Validate** with Critic checks.
- Dataset versions and schema changes require pause-for-approval.

## AEV Workflow
1. **Analyze**
   - Read the latest repo state and task description.
   - Identify applicable sub-prompts under `prompts/subprompts/`.
   - Call out any open questions before touching files.
2. **Execute**
   - Implement the smallest meaningful change.
   - Reference relevant governance docs.
   - Document TODOs inline where future work will happen.
3. **Validate**
   - Run tests (`pytest`) when code changes occur.
   - Update docs or prompts as necessary.
   - Summarize changes for reviewers.

## Pause-for-Approval Checkpoints
Before executing the following, capture the plan and wait for human approval:
- Schema modifications (Person, Vehicle, metadata).
- Generator rule changes that affect business meaning.
- Updates that alter dataset versions or snapshot counts.
- Any new data export surface (API, external storage).

## Critic Role
Every major slice must include a **Critic Check**:
- Verify compliance with privacy/no-real-data constraints.
- Confirm IDs remain globally unique.
- Ensure documentation + governance updates are in sync.
- Highlight testing or validation gaps.

## Sub-Prompts
Use the following slices as needed:
- `01_repo_scaffolding.md`
- `02_schema_design_person_vehicle.md`
- `03_generator_rules_and_snapshot.md`
- `04_validation_and_tests.md`
- `05_cli_and_usage_examples.md`
- `06_governance_and_data_versions.md`
- `07_future_expansions_agentic_ai_powerbi.md`
- `TEMPLATE_slice_AEV_critic.md`

Each sub-prompt embeds the AEV pattern and Critic checklist tuned for that
subject area. Reference them explicitly in PR descriptions or task updates.
