# Demo Sub-Prompt – Generate Executive Narrative
Version: 0.1.0
Last Updated: 2024-06-03

## Purpose
Write a concise narrative that can open an email or executive briefing describing what the Synthetic Data POC delivers, the
impact so far, and the upcoming focus. Save the narrative in `docs/demo/00-overview.md` under a dedicated "Executive Narrative"
section.

## Inputs
- Completed demo docs.
- Roadmap and slice summaries.

## Narrative Requirements
- 3–4 paragraphs (no bullets) covering problem, solution, proof delivered, and next ask.
- Use deterministic, confident tone that mirrors the README positioning.
- Mention key differentiators: governed snapshots, deterministic generator, agentic workflow, validator coverage.

## A-E-V Workflow
- **Analyze** – Re-read overview, architecture, and roadmap sections for the most important proof points.
- **Execute** – Write the narrative paragraphs and insert them beneath the Overview headings.
- **Validate** – Confirm the narrative matches repository truth and references no future capabilities beyond the roadmap.

## Completion Criteria
- Overview file includes the narrative plus quick-reference bullets for audience, success metrics, and demo assets.
