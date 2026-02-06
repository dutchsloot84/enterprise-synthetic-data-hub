# Mobilitas AI Prompt Library

## What this is
A Mobilitas-wide, reusable pattern for LLM-assisted delivery that treats prompts as governance artifacts while keeping them practical for daily engineering work.

## Why this exists
- **Repeatability:** consistent structure across prompts and roles.
- **Auditability:** deterministic outputs and explicit decision logs.
- **SDD alignment:** prompts require specs/ADRs to be updated via proposed diffs only.

## How this reduces risk
- Structured prompts with explicit outputs and required inputs.
- Propose-diffs-only updates for specs/ADRs (no silent edits).
- Review gating: diffs must be reviewed and approved.
- Redaction rules: no secrets or internal URLs.

## Quickstart
### How to use with Codex
1. Choose a role and prompt from the index below.
2. Provide the required inputs (paths, scope, constraints, acceptance criteria).
3. Run the prompt and review the proposed diffs before applying.

### How to run manually
1. Open the prompt file and paste it into your LLM.
2. Fill in the “Inputs required” section.
3. Review the output and apply the proposed diffs.

## Usage rules
- **Repo docs are the source of truth.** If a path is unknown, search the repo and reference the correct file.
- **Propose diffs only.** Do not silently rewrite specs/ADRs.
- **No secrets or internal URLs.** Redact or omit sensitive data.
- **Keep outputs deterministic and reviewable.** Use structured headings and short, stable formatting.

## Index
### Roles
- `ai/roles/spec_architect.md` — Define or refine specs and acceptance criteria with SDD alignment.
- `ai/roles/contract_guardian.md` — Protect and evolve API/data contracts with minimal breakage.
- `ai/roles/demo_critic.md` — Critique demo flows and readiness from a stakeholder perspective.

### Prompts
- `ai/prompts/orchestrate/feature_sdd_patch_plan.md` — Orchestrate multi-artifact updates with a patch plan.
- `ai/prompts/orchestrate/pre_pr_critic.md` — Critique a change set before PR creation.
- `ai/prompts/one_file/spec_patch_only.md` — Propose diffs for a single spec file.
- `ai/prompts/one_file/test_patch_only.md` — Propose diffs for a single test file.
- `ai/prompts/explore/design_tradeoffs.md` — Enumerate tradeoffs with deterministic, reviewable output.
- `ai/prompts/explore/scenario_pack_brainstorm.md` — Brainstorm scenarios in a structured, bounded way.
- `ai/prompts/_TEMPLATE.md` — Template for creating new prompts with invariants and decision log.

## Future Automation
These prompts can later be wrapped in CI or make targets to generate PRs for review. This keeps deterministic formatting while ensuring proposed diffs are reviewed before merge.

## FUTURE: Auto-apply mode (Option A)
A safe path to enable auto-apply later:
- Limit to low-risk docs (prompt catalogs/templates).
- Only via CI that opens a PR (never direct to main).
- Mandatory diff review and approvals.
- Deterministic formatting with lint checks.

