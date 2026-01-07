# Demo Prompt & Feature Changelog – v2.0

| Date | Change | Files |
| --- | --- | --- |
| 2024-06-09 | Archived v1 prompts under `archive/demo_v1/` and created v2 MOP + slice prompts for 08–14. | `archive/demo_v1/**`, `mop/master_orchestrator_prompt.md`, `prompts/demo_mop.md`, `prompts/sub-prompts/*.md`, `mop/index.yaml` |
| 2024-06-09 | Added profiles schema/model/helper + sample JSON bundles for demo storytelling. | `schemas/v0.1/profile_schema.yaml`, `src/enterprise_synthetic_data_hub/models/profile.py`, `src/enterprise_synthetic_data_hub/generation/profiles.py`, `data/demo_samples/v0.1/*.json` |
| 2024-06-09 | Delivered local Flask API, demo CLI, `make demo`, and smoke tests to power the live walkthrough. | `src/enterprise_synthetic_data_hub/api/app.py`, `scripts/demo_data.py`, `Makefile`, `scripts/demo_start_api.sh`, `tests/smoke/**` |
| 2026-01-06 | Documented demo profiles and orchestration alignment (profile info CLI, demo flow, runbook refresh). | `config/demo.yaml`, `src/enterprise_synthetic_data_hub/cli/profile_info.py`, `scripts/run_demo_flow.py`, `docs/demo/**` |
