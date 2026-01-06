# CI/CD Overview

## Workflow
- **Publish Snapshot** (`.github/workflows/publish-snapshot.yml`)
  - Triggers on `develop` branch pushes or manual dispatch.
  - Steps: checkout → Python 3.11 setup → `pip install -e .` → `python -m enterprise_synthetic_data_hub.cli.main generate-snapshot --output-dir data/published` → upload artifact → publish GitHub release (`snapshot-<sha>`).
  - Artifacts include CSV/JSON/NDJSON/Parquet outputs plus manifest checksums and stats for reproducibility.

## Expectations
- Local `pytest` runs should pass before pushing to `develop` to avoid broken releases.
- Manifest checksums and record counts are the canonical release contract; consumers should validate them on download.
- Seeds used during CI runs default to **20240601** unless overridden in workflow inputs.

## Consumption
- Download artifacts from the release created by the workflow (`snapshot-<sha>` tag).
- Verify checksums against `snapshot_manifest_*.json` before distributing or loading into downstream systems.

## Future Hardening (suggested)
- Gate releases on `pytest` and demo smoke markers.
- Add badge/reporting for manifest diff drift across commits.
