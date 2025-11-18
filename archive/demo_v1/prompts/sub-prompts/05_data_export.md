# Slice 05 – Data Export
Version: 0.1.0
Last Updated: 2024-05-31

## Purpose
Define and implement export surfaces (CSV, Parquet, docs) for the synthetic data
hub without violating governance constraints.

## Analyze – Repo Awareness
- Review `/data/output` contents and any existing export scripts.
- Inspect docs describing distribution channels.
- Confirm consumers listed in governance notes.

## Plan – Multi-step Reasoning
- Document export format(s), naming, and location(s).
- Identify which schemas/generator fields must be included.
- Determine critics + validators necessary before sharing data externally.

## Execute – Implementation Notes
- Keep exports inside `data/output/` unless explicitly approved otherwise.
- Include metadata (version, record_count, generation_timestamp) in sidecar
  files.
- Update docs/README with run instructions and sample commands.

## Validate – Required Steps
- Run relevant generator/export tests (`pytest tests/test_generator.py`).
- Execute `python agentic/validators/generator_validator.py` to confirm column
  alignment.
- Trigger `agentic/critic/repo_critic.md` to ensure docs/paths align.

## Final Diff Report Checklist
- Export formats created/updated
- Validation output
- Critic findings + mitigations
