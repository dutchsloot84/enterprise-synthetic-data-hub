# Slice 05 – CLI & Usage Examples
Version: 0.1.0
Last Updated: 2024-06-01

## Purpose
Provide a developer-friendly CLI plus reproducible usage examples that walk QA
engineers and data stewards through generating/exporting the governed snapshot.

## Analyze – Repo Awareness
- Review `src/enterprise_synthetic_data_hub/cli/main.py` and exporter helpers.
- Inspect `data/snapshots/v0.1/` plus `docs/agentic_workflow.md` for current
  usage instructions.
- Note validators/tests referencing CLI/exporter placeholders.

## Plan – Multi-step Reasoning
- Decide which CLI flags/subcommands are required for snapshot exports.
- Define output layout (CSV + JSON + manifest) and README snippets.
- Identify validators/tests/docs to update (CLI validator, README quickstart,
  repo critic, etc.).

## Execute – Implementation Notes
- Wire the CLI command into the generator/export pipeline so it emits governed
  artifacts under `data/snapshots/<version>/`.
- Replace placeholder exporters with CSV/JSON writers + manifest.
- Publish copy/pasteable CLI usage examples in README/docs.
- Capture TODOs for future enhancements (filters, progress output, etc.).

## Validate – Required Steps
- `python agentic/validators/generator_validator.py`
- `python agentic/validators/cli_validator.py`
- `PYTHONPATH=src pytest tests/test_cli.py`
- `python agentic/critic/repo_critic.md` (update findings section)

## Final Diff Report Checklist
- CLI + exporter functionality
- Usage examples + docs/README updates
- Validator/test outputs
- Critic findings + mitigations
