# Slice 04 – Validation Suite
Version: 0.1.0
Last Updated: 2024-05-31

## Purpose
Strengthen automated validation so schemas, generator outputs, APIs, and docs
stay synchronized.

## Analyze – Repo Awareness
- Inventory scripts under `agentic/validators` and the tests in `/tests`.
- Review CI instructions in README/docs (if any) to ensure alignment.
- Identify which validators already run vs. which need implementation.

## Plan – Multi-step Reasoning
- Decide which validators/tests need updates.
- Determine data fixtures or sample outputs necessary for coverage.
- Map critic hooks (schema/generator/api/repo) to validations.

## Execute – Implementation Notes
- Keep validators lightweight and import-safe (no heavy deps by default).
- Provide CLI usage instructions at the bottom of each validator.
- Update `/docs` with how to run the suite.

## Validate – Required Steps
- Execute each validator touched and capture stdout in the PR/testing notes.
- Run targeted pytest modules (e.g., `pytest tests/test_schema_validation.py`).
- Trigger the relevant critic template to document validation findings.

## Final Diff Report Checklist
- Validators/Tests created or updated
- Execution output (pass/fail)
- Critic highlights + remediation actions
