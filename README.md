# Enterprise Synthetic Data Hub (POC)

## Project Overview
The Enterprise Synthetic Data Hub is a two-week proof of concept for CSAA / Mobilitas. It delivers an enterprise-aligned foundation for generating privacy-safe synthetic data that represents Persons, Vehicles, and derived Profiles. The focus is on scaffolding, governance, and prompt-driven collaboration so future human and LLM contributors can extend the solution quickly.

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
- Local Flask API is designed for demo use only (no auth, not production hardened).
- Distribution targets (S3/Snowflake) remain future scope.
- Schema coverage currently limited to v0.1 Person, Vehicle, Profile, and dataset metadata definitions.

## High-Level Architecture
```
src/enterprise_synthetic_data_hub/
  config/          # Settings, dataset size, seeds, versioning hints
  models/          # Pydantic schemas for Person, Vehicle, dataset metadata
  generation/      # Rule definitions, snapshot orchestration, profile builder
  validation/      # Schema + structural validation utilities
  io/              # Export helpers (CSV/JSON writers + manifest)
  cli/             # Snapshot CLI + demo preview helpers
  api/             # Flask app exposing /healthz and /generate/* endpoints

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

4. **Preview demo data**
   ```bash
   python scripts/demo_data.py --records 5 --preview 2
   python scripts/demo_data.py --use-api --api-url http://127.0.0.1:5000 --records 3
   ```

5. **Run the local Flask API**
   ```bash
   export FLASK_APP=enterprise_synthetic_data_hub.api.app:app
   flask run
   ```

6. **Run validators**
   ```bash
   python agentic/validators/schema_validator.py
   python agentic/validators/generator_validator.py
   python agentic/validators/cli_validator.py
   python agentic/validators/api_validator.py
   ```

## Snapshot Outputs
- `data/snapshots/v0.1/persons_v0_1.csv` – governed Persons CSV exported via the CLI.
- `data/snapshots/v0.1/vehicles_v0_1.csv` – governed Vehicles CSV.
- `data/snapshots/v0.1/dataset_v0_1.json` – combined JSON payload (metadata + persons + vehicles + profiles).
- `data/snapshots/v0.1/metadata_v0_1.json` – standalone metadata JSON (includes `record_count_profiles`).
- `data/snapshots/v0.1/snapshot_manifest_v0_1.json` – manifest enumerating file names + record counts.
- `data/demo_samples/v0.1/*.json` – curated bundles for docs/slides.

## CLI Usage Examples
```bash
# small sample with deterministic seed
python -m enterprise_synthetic_data_hub.cli.main generate-snapshot \
    --output-dir /tmp/snapshot_v0_1 --records 50 --seed 123

# default settings (records pulled from DatasetSettings)
python -m enterprise_synthetic_data_hub.cli.main generate-snapshot

# colorful demo preview
python scripts/demo_data.py --records 3 --preview 2 --randomize
```

The command prints the exported file paths so QA engineers can copy/paste them
into validators, API configs, or notebooks.

## Demo Runbook & Automation
- Run `make demo` to orchestrate snapshot generation, a generator preview, and an automated API + CLI walk-through.
- Follow `docs/demo/06-runbook.md` for the narrated, copy/paste friendly playbook used in the live demo.

## Next Steps
- Add distribution mechanisms (S3/Snowflake) after the API layer stabilizes.
- Introduce Policy/Claim schemas and cross-entity validation flows.
