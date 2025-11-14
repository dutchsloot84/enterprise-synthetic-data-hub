# Enterprise Synthetic Data Hub (POC)

## Project Overview
The Enterprise Synthetic Data Hub is a two-week proof of concept for CSAA / Mobilitas. It delivers an enterprise-aligned foundation for generating privacy-safe synthetic data that represents Persons and Vehicles. The focus is on scaffolding, governance, and prompt-driven collaboration so future human and LLM contributors can extend the solution quickly.

## POC Scope
- Generate a **single snapshot dataset** with a few hundred coherent Person + Vehicle records.
- Use rule-based generation only (no real or production data).
- Provide stable, versioned snapshots stored under `data/snapshots/`.
- Implement Person, Vehicle, and dataset metadata schemas.
- Provide minimal CLI, validation, and export stubs that will be expanded later.

## Value Proposition
- **Consistent test data across all workstreams (Mobilitas & CSAA).**
- **Reduced inconsistent regression failures.**
- **Accelerated QA onboarding (common, shared synthetic dataset).**
- **Reduced time to build and maintain test scenarios.**
- **Unified test data across Mobilitas (Commercial) and CSAA (Personal Lines).**
- **Foundation for “Synthetic Data as a Service” in future (API, S3, etc.).**
- **Enabler for AI-driven test automation and analytics.**
- **Improved auditability and repeatability (versioned snapshots, schema + tests).**

## Current Limitations
- Generator logic is not implemented yet.
- Snapshot data is not generated yet (placeholders only).
- No public API or external storage layers.
- Only Person + Vehicle schemas are defined in the POC.

## High-Level Architecture
```
src/enterprise_synthetic_data_hub/
  config/          # Settings, dataset size, seeds, versioning hints
  models/          # Pydantic schemas for Person, Vehicle, dataset metadata
  generation/      # Rule definitions and snapshot orchestration (stubs)
  validation/      # Schema + structural validation utilities
  io/              # Export helpers (CSV/JSON) – stubs
  cli/             # CLI entrypoint stub for future workflows
  api/             # Placeholder notes for a future API layer

data/snapshots/    # Versioned, stable dataset artifacts (POC uses v0.1)
tests/             # Pytest suite for schema + metadata validation
governance/        # Roles, decision log, data stewardship rules
prompts/           # Master Operating Prompt + sub-prompts for AEV work
future/            # Stubs for agentic AI and Power BI extensions
```

## Quickstart
1. **Set up environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .[dev]
   ```
2. **Run tests**
   ```bash
   pytest
   ```

## Next Steps
- Implement rule-based generator logic in `src/enterprise_synthetic_data_hub/generation/generator.py` using `prompts/subprompts/03_generator_rules_and_snapshot.md`.
- Add exporters that materialize the v0.1 snapshot under `data/snapshots/v0.1/`.
- Expand validation + CLI once generation exists.
