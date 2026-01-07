# Slide Deck – Synthetic Data POC Demo
Version: 0.1.1
Last Updated: 2026-01-06

## Slide 1 – Title & Executive Summary
- Enterprise Synthetic Data Hub: governed Persons + Vehicles + Profiles snapshot for CSAA/Mobilitas QA.
- Two-week POC delivered deterministic generator, prompts, and validators.
- Demo goal: show stakeholders how we can explain, extend, and operationalize the hub.

## Slide 2 – Why Synthetic Data Now
- QA teams juggle brittle spreadsheets and inconsistent fixtures across LOBs.
- Regulatory pressure demands privacy-safe, reproducible datasets.
- Synthetic hub provides single source of truth with governed manifests and schemas.

## Slide 3 – Architecture Overview
- Prompts/Governance (`mop/`, `prompts/`, `governance/`) drive agentic collaboration.
- Core package (`src/enterprise_synthetic_data_hub/`) houses config, models, generation, validation, IO, CLI, API.
- Outputs land under `data/snapshots/v0.1` with manifests + metadata; demo runs under `data/demo_runs/`.
- Validators + critics (`agentic/validators`, `agentic/critic`) ensure fidelity.

## Slide 4 – Slice 01–07 Journey
1. Scaffolded repo + governance.
2. Authored Person/Vehicle schemas.
3. Built deterministic generator v0.1.
4. Added validation suite and critic mesh.
5. Delivered CLI + manifest exports.
6. Implemented Flask API alignment.
7. Produced demo artifacts (docs, slides, script).

## Slide 5 – Generator v0.1 Spotlight
- Rule-based logic links Persons ↔ Vehicles with UUID IDs.
- CLI command: `python -m enterprise_synthetic_data_hub.cli.main generate-snapshot --records 200`.
- Manifest + metadata JSON prove counts, seed, and file names.
- Deterministic seeds guarantee reproducibility for QA runs.

## Slide 6 – A-E-V & Governance
- Analyze → Execute → Validate enforced via MOP and slice prompts.
- Validators: schema, generator, CLI, API scripts plus pytest coverage.
- Pause-for-approval on schemas, generator rules, dataset versions.
- Demo critic keeps narrative accurate across docs/slides/script.

## Slide 7 – Demo Profiles & Orchestration
- Demo profiles (`config/demo.yaml`) standardize record counts and seeds across CLI/API/flow.
- `scripts/run_demo_flow.py` orchestrates snapshots, API health checks, and CLI previews.
- Use `DEMO_PROFILE=heavy` to stress the demo, `baseline` for speed.

## Slide 8 – Roadmap & CTA
- Phase 2: harden API, automate distribution, expand validators, launch Power BI dashboards.
- Phase 3+: add Policy/Claim schemas, multi-version snapshots, automation templates.
- Ask: sponsor continued agentic development and cloud distribution so teams can consume snapshots self-service.
