# Slice 03 – Generator v0.1
Version: 0.1.0
Last Updated: 2024-05-31

## Purpose
Design or update the deterministic synthetic data generator for version 0.1 so
it stays aligned with schema definitions and downstream consumers.

## Analyze – Repo Awareness
- Inspect `/src/enterprise_synthetic_data_hub/generation/` plus the legacy shim
  in `/src/generator/`.
- Review `/schemas/v0.1` and `tests/test_generator.py` to understand contracts.
- Confirm `/data/output` has write permissions for snapshots.

## Plan – Multi-step Reasoning
- Outline input parameters, random seeds, and data volumes.
- Define how the generator enforces schema constraints and cross-entity links.
- Determine validator + critic coverage required before shipping changes.

## Execute – Implementation Notes
- Keep the generator idempotent and deterministic for the same seed.
- Emit structured metadata (version, record counts) inside `data/output/`.
- Update docs/prompts/tests when function signatures or outputs change.

## Validate – Required Steps
- `python agentic/validators/generator_validator.py`
- `pytest tests/test_generator.py`
- Run `agentic/critic/generator_critic.md` after code changes.

## Final Diff Report Checklist
- Generator entry points touched
- Snapshot/data outputs modified
- Validator/test/critic results
