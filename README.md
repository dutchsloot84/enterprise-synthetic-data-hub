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
- CLI exports governed CSV + JSON bundles, but downstream API consumers still rely on the older CSV layout until Slice 06.
- No public API or external storage layers.
- Schema coverage currently limited to v0.1 Person, Vehicle, and dataset metadata definitions.

## High-Level Architecture
```
src/enterprise_synthetic_data_hub/
  config/          # Settings, dataset size, seeds, versioning hints
  models/          # Pydantic schemas for Person, Vehicle, dataset metadata
  generation/      # Rule definitions and snapshot orchestration (stubs)
  validation/      # Schema + structural validation utilities
  io/              # Export helpers (CSV/JSON writers + manifest)
  cli/             # CLI entrypoint for governed snapshot exports
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
3. **Generate the governed snapshot**
   ```bash
   python -m enterprise_synthetic_data_hub.cli.main generate-snapshot \
       --output-dir data/snapshots/v0.1 \
       --records 200
   ```
   _Optional flags_: `--seed` overrides the deterministic seed and `--records` sets the record count.

4. **Run validators**
   ```bash
   python agentic/validators/schema_validator.py
   python agentic/validators/generator_validator.py
   python agentic/validators/cli_validator.py
   python agentic/validators/api_validator.py
   ```

## Snapshot Outputs
- `data/snapshots/v0.1/persons_v0_1.csv` – governed Persons CSV exported via the CLI.
- `data/snapshots/v0.1/vehicles_v0_1.csv` – governed Vehicles CSV.
- `data/snapshots/v0.1/dataset_v0_1.json` – combined JSON payload (metadata + records).
- `data/snapshots/v0.1/metadata_v0_1.json` – standalone metadata JSON.
- `data/snapshots/v0.1/snapshot_manifest_v0_1.json` – manifest enumerating file names + record counts.
- `data/output/sample_dataset_v0_1.json` – small, developer-focused JSON sample (unchanged).

## CLI Usage Example
```bash
# small sample with deterministic seed
python -m enterprise_synthetic_data_hub.cli.main generate-snapshot \
    --output-dir /tmp/snapshot_v0_1 --records 50 --seed 123

# default settings (records pulled from DatasetSettings)
python -m enterprise_synthetic_data_hub.cli.main generate-snapshot
```

The command prints the exported file paths so QA engineers can copy/paste them
into validators, API configs, or notebooks.

## Next Steps
- Align the Flask API with the governed CSV layout so it serves the same schema as the CLI exports.
- Add distribution mechanisms (S3/Snowflake) after the API layer stabilizes.
