# Demo Critic Check – Synthetic Data POC
Version: 0.1.0
Last Updated: 2024-06-03

## Purpose
Verify the demo system artifacts for correctness, completeness, and alignment with the implemented code through Slice 07.

## Inputs
- `/docs/demo/**/*.md`
- `/README.md`, `/docs/api.md`, `/mop/master_orchestrator_prompt.md`
- Relevant source files under `/src/enterprise_synthetic_data_hub`

## Evaluation Dimensions
1. **Accuracy** – Every statement about schemas, generator behavior, validators, and exports must match the repository.
2. **Completeness** – All required files exist and contain the sections described in the sub-prompts.
3. **Consistency** – Terminology matches README + prompts (Persons, Vehicles, governed snapshot, v0.1, A-E-V).
4. **Alignment to Slices 01–07** – Slice summaries correctly describe objectives/outcomes without skipping steps.
5. **Clarity** – Docs, slides, and talking points are understandable by stakeholders with mixed technical depth.

## Critic Instructions
- Scan each artifact top-to-bottom.
- Highlight any inconsistency with repo facts, missing sections, or vague statements.
- Provide concrete fix suggestions referencing file paths and line numbers.
- Block sign-off until all issues are resolved.

## Output Format
Return a checklist such as:
```
[ ] Accuracy – detail if mismatch is found
[ ] Completeness – explain missing artifacts/sections
[ ] Consistency – cite terminology issues
[ ] Alignment – verify slice descriptions
[ ] Clarity – note unclear prose or slides
```
Add action items under each unchecked box.
