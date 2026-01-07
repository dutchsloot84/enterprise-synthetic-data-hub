# Architecture – Enterprise Synthetic Data Hub
Version: 0.1.1
Last Updated: 2026-01-06

## Textual Diagram
```
[Prompts & Governance]
        |
[MOP + A-E-V tasks] --> [src/enterprise_synthetic_data_hub]
        |                                |
    [agentic/]                        [generation/ | models/ | io/ | validation/ | cli/ | api/]
        |                                |
    [Critics & Validators] --> [data/snapshots/v0.1 + manifests + demo runs]
```

## Component Breakdown
| Layer | Description | Key Paths |
| --- | --- | --- |
| Governance & Prompts | Defines how humans/LLMs collaborate using Master Operating Prompt, slice prompts, and critic templates. | `mop/`, `prompts/`, `governance/` |
| Agentic Tasks & Validators | Executable guidance plus validation scripts that enforce schema, generator, CLI, and API expectations. | `agentic/tasks/`, `agentic/validators/`, `agentic/critic/` |
| Core Package | Python package that owns configuration, Pydantic schemas, generator logic, validation helpers, IO/export utilities, CLI, and API. | `src/enterprise_synthetic_data_hub/` |
| Demo Orchestration | Demo flow driver, API start/stop helpers, and preview steps. | `scripts/run_demo_flow.py`, `scripts/demo_flow/` |
| Data Artifacts | Deterministic snapshots, manifests, demo runs, and samples exported by the CLI/generator. | `data/snapshots/v0.1/`, `data/demo_runs/`, `data/demo_samples/` |
| Tests | Pytest suites verifying schema conformance and generation behavior. | `tests/` |

## Data Flow
1. **Configuration** – `src/enterprise_synthetic_data_hub/config/dataset_settings.py` declares dataset size, seed, and version. Demo profiles live in `config/demo.yaml`.
2. **Schema Enforcement** – Pydantic models in `src/enterprise_synthetic_data_hub/models/` guarantee Person + Vehicle + Profile shape.
3. **Generation** – `generation/generator.py` fabricates Person and Vehicle entities, linking them by IDs and applying deterministic rules. Profiles are derived via `generation/profiles.py`.
4. **Validation** – Validators under `src/enterprise_synthetic_data_hub/validation/` and standalone scripts in `agentic/validators/` catch schema drift.
5. **Export** – IO helpers in `src/enterprise_synthetic_data_hub/io/` plus the CLI entrypoint at `src/enterprise_synthetic_data_hub/cli/main.py` write governed CSV + JSON outputs and snapshot manifests.
6. **Demo & API** – `src/enterprise_synthetic_data_hub/api/app.py` exposes `/healthz` and `/generate/*` endpoints; `scripts/run_demo_flow.py` orchestrates snapshots, API health checks, and CLI previews.

## Technology Highlights
- Python 3.11 package with Pydantic models and deterministic seed management.
- Prompt-driven development backed by critics and validators for each slice.
- Human-ready documentation plus future-focused folders (`future/agentic_ai`, `future/powerbi_dashboards`).

## Integration Points
- Validators integrate with CI or manual runs (`python agentic/validators/*.py`).
- CLI can be triggered locally or within automation to produce regulated snapshots.
- API surface shares the same schema as governed exports and powers the demo CLI.
