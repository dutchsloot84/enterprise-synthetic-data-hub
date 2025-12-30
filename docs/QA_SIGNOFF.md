# QA Sign-off Log

## QA Sign-off Summary — 2025-12-30 (Windows / Git Bash / Python 3.13.2)

### Environment
- OS: Windows + Git Bash
- Python: 3.13.2
- Branch: develop (clean working tree)
- Date: Dec 30, 2025

### PASS — Core health & deterministic behavior
- Settings load with deterministic defaults (dataset_version=v0.1, seed 20240601, marker enterprise-synthetic-data-hub v0.1)
- scripts/demo_validate.py passes: Person schema checks, Vehicle schema checks, Synthetic marker checks
- Test suite: pytest -m demo => 14 passed (includes golden determinism, API contract, negative-path)

### PASS — Live API manual verification
- Manual Flask start on 127.0.0.1:5000
- /healthz returns status ok + plan + seed
- /generate/profile returns deterministic JSON and includes synthetic_source marker
- Invalid request returns HTTP 400 with error envelope {"error":{"code":"invalid_request",...}}

### PASS — Snapshot artifacts generation
- Orchestrator Step 1 generated snapshot artifacts under scripts/data/demo_runs/<timestamp>_baseline/
- dataset JSON + metadata + manifest + README + CSVs present

### Known issues / follow-up
- scripts/run_demo_flow.py fails on Windows at API start due to (a) scripts/scripts path bug and (b) bash/WSL/MSYS issues.
- python -m enterprise_synthetic_data_hub.cli.demo --help prints nothing because module is not a __main__ entrypoint; demo CLI is invoked via run_demo() or other entrypoint.
