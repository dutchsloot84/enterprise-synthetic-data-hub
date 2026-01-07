# Generator v0.1 Deep Dive
Version: 0.1.1
Last Updated: 2026-01-06

## Objective
Deliver a reproducible Person + Vehicle dataset that reflects governed insurance attributes without referencing production data.

## Key Modules
| Module | Role |
| --- | --- |
| `src/enterprise_synthetic_data_hub/config/dataset_settings.py` | Declares dataset size (default ~200 records), deterministic seed, and snapshot version identifier. |
| `src/enterprise_synthetic_data_hub/models/person.py` & `vehicle.py` & `profile.py` | Pydantic schemas enforcing GUID IDs, demographics, contact info, VIN/license formats, profile summaries, and `lob_type`. |
| `src/enterprise_synthetic_data_hub/generation/generator.py` | Fabricates Persons and Vehicles, links them by `person_id`, derives Profiles, injects metadata, and streams rows into structured payloads. |
| `src/enterprise_synthetic_data_hub/io/exporters.py` | Writes governed CSVs (`persons_v0_1.csv`, `vehicles_v0_1.csv`) and JSON bundles plus `snapshot_manifest_v0_1.json`. |
| `tests/test_generator.py` | Confirms deterministic counts, schema compliance, and referential integrity. |

## Determinism & Governance
- **Seed Control** – CLI flag `--seed` overrides the default seed so QA can reproduce exact datasets.
- **Snapshot Naming** – All exports reference the governed `v0.1` tag to prevent mixing with future schema versions.
- **Manifest Tracking** – `snapshot_manifest_v0_1.json` lists every generated file, record counts, and timestamps for auditing.
- **Metadata Parity** – `dataset_v0_1.json` and `metadata_v0_1.json` combine record counts, generation settings, and contact info.

## Data Model Highlights
- Persons carry demographics, addresses, LOB classification, and GUID `person_id`.
- Vehicles reference their owning `person_id`, include VIN, registration, and `lob_type` for personal vs. commercial lines.
- Profiles combine the key Person + Vehicle attributes into a narration-friendly record (`full_name`, `vehicle_summary`, `risk_rating`).
- Cross-entity validations ensure each vehicle maps to a valid person, and manifest totals match CLI parameters.

## Execution Path
1. Run `python -m enterprise_synthetic_data_hub.cli.main generate-snapshot --records 200 --output-dir data/snapshots/v0.1`.
2. CLI loads dataset settings, seeds RNG, and invokes `generation/generator.generate_snapshot_bundle()`.
3. Generator streams records through IO helpers, creating CSV + JSON outputs plus metadata + profiles.
4. Validators, smoke tests, and docs confirm schema compliance before sharing the snapshot.

## Sample Bundles
- `data/demo_samples/v0.1/persons_sample.json`
- `data/demo_samples/v0.1/vehicles_sample.json`
- `data/demo_samples/v0.1/profiles_sample.json`
- `data/demo_samples/v0.1/bundle_sample.json`

Use these curated artifacts for slides, the runbook, or quick API/CLI demos when a full snapshot isn’t needed.

## Demo Talking Points
- Rule-based approach keeps PII risk near zero while simulating realistic insurance scenarios.
- Deterministic design guarantees reproducibility for QA regressions and agentic workflows.
- The generator is extendable: new entities or attributes can plug in through the same config/schema/validation stack.
