# Decisions Log

| Date       | Decision                                                                 | Owner            | Notes |
|------------|---------------------------------------------------------------------------|------------------|-------|
| 2024-06-01 | POC scope limited to Person + Vehicle schemas only.                      | Product Owner    | Enables fast delivery. |
| 2024-06-02 | Added dataset metadata schema to align with generator + governance.      | Data Steward     | Extends schema scope while staying in v0.1. |
| 2024-06-01 | Snapshot must be deterministic and stored under `data/snapshots/v0.1/`.   | Data Steward     | Supports auditability. |
| 2024-06-01 | Adopt prompt-driven AEV + Critic workflow for all major contributions.    | AI Lead          | Ensures consistent collaboration. |
| 2024-06-01 | CLI/exporter emits governed CSV/JSON bundle + manifest under `data/snapshots/v0.1/`. | Data Steward     | Enables QA teams to pull stable artifacts via CLI. |
