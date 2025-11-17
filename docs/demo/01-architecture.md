# Architecture – Enterprise Synthetic Data Hub
Version: 0.1.0
Last Updated: 2024-06-03

## Textual Diagram
```
[Prompts & Governance]
        |
[MOP + A-E-V tasks] --> [src/enterprise_synthetic_data_hub]
        |                                |
    [agentic/]                        [generation/ | models/ | io/ | validation/ | cli/ | api/]
        |                                |
    [Critics & Validators] --> [data/snapshots/v0.1 + manifests]
```

## Component Breakdown
| Layer | Description | Key Paths |
| --- | --- | --- |
| Governance & Prompts | Defines how humans/LLMs collaborate using Master Operating Prompt, slice prompts, and critic templates. | `mop/`, `prompts/`, `governance/` |
| Agentic Tasks & Validators | Executable guidance plus validation scripts that enforce schema, generator, CLI, and API expectations. | `agentic/tasks/`, `agentic/validators/`, `agentic/critic/` |
| Core Package | Python package that owns configuration, Pydantic schemas, generator logic, validation helpers, IO/export utilities, CLI, and API stubs. | `src/enterprise_synthetic_data_hub/` |
| Data Artifacts | Deterministic snapshots, manifests, and samples exported by the CLI/generator. | `data/snapshots/v0.1/`, `data/output/` |
| Tests | Pytest suites verifying schema conformance and generation behavior. | `tests/` |

## Data Flow
1. **Configuration** – `src/enterprise_synthetic_data_hub/config/dataset_settings.py` declares dataset size, seed, and version.
2. **Schema Enforcement** – Pydantic models in `src/enterprise_synthetic_data_hub/models/` guarantee Person + Vehicle shape.
3. **Generation** – `generation/snapshot_generator.py` fabricates Person and Vehicle entities, linking them by IDs and applying
   deterministic rules (UUID IDs, LOB metadata, VIN/license formats).
4. **Validation** – Validators under `src/enterprise_synthetic_data_hub/validation/` and standalone scripts in
   `agentic/validators/` catch schema drift.
5. **Export** – IO helpers in `src/enterprise_synthetic_data_hub/io/` plus the CLI entrypoint at
   `src/enterprise_synthetic_data_hub/cli/main.py` write governed CSV + JSON outputs and snapshot manifests.
6. **Distribution Stubs** – `src/enterprise_synthetic_data_hub/api/` outlines the Flask/API alignment work targeted for later
   slices.

## Technology Highlights
- Python 3.11 package with Pydantic models and deterministic seed management.
- Prompt-driven development backed by critics and validators for each slice.
- Human-ready documentation plus future-focused folders (`future/agentic_ai`, `future/powerbi_dashboards`).

## Integration Points
- Validators integrate with CI or manual runs (`python agentic/validators/*.py`).
- CLI can be triggered locally or within automation to produce regulated snapshots.
- API stubs ensure future service surfaces share the same schema as the governed exports.
