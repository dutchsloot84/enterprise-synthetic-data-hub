# Demo Sub-Prompt – Generate Demo Artifacts
Version: 0.1.0
Last Updated: 2024-06-03

## Purpose
Produce the six markdown artifacts under `/docs/demo` that explain the POC, architecture, slice progress, generator v0.1,
A-E-V loop, and roadmap. These docs should let any teammate understand and present the POC without digging through the entire
repo.

## Inputs
- Repository facts from `README.md`, `/docs`, `/schemas/v0.1`, `/src/enterprise_synthetic_data_hub`, `/prompts`, and
  `/governance`.
- Slice intent derived from existing prompts 00–06 plus the overall mobilization notes in `/mop`.

## Expected Outputs
1. `00-overview.md` – executive summary, problem statement, solution snapshot, business impact.
2. `01-architecture.md` – textual architecture diagram + component descriptions tied to repo paths.
3. `02-slice-summary.md` – chronological summary of Slices 01–07, emphasizing scope and delivered artifacts.
4. `03-generator-v0.1.md` – deep dive on deterministic generation strategy, schemas, and snapshot manifest.
5. `04-aev-explainer.md` – walkthrough of Analyze → Execute → Validate workflow and critic coverage.
6. `05-roadmap.md` – Phase 2+ roadmap anchored to known backlog items (API hardening, exports, dashboards, automation).

## A-E-V Workflow
1. **Analyze** – Confirm statements against code and documentation; capture exact filenames/functions where helpful.
2. **Execute** – Write complete markdown with sections, tables, and bullet lists. Cite repo paths to orient engineers.
3. **Validate** – Re-read for factual accuracy, determinism, and alignment with existing prompts. Ensure no future-scope claims
   beyond what the roadmap explicitly flags as upcoming.

## Style & Tone
- Professional, concise sentences with scannable headings.
- Use numbered/bulleted lists to highlight slice outcomes and roadmap steps.
- Reference real artifacts (e.g., `src/enterprise_synthetic_data_hub/generation/snapshot_generator.py`).

## Completion Criteria
- All six files exist and contain deterministic, human-ready prose.
- Information aligns with Slices 01–07 and repository state.
- No placeholders, TODOs, or speculative implementation details.
