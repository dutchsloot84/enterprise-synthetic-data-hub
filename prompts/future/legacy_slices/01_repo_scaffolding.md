# Slice 01 – Repo Scaffolding

Use this prompt when adjusting project structure, bootstrapping new folders, or
updating foundational tooling.

## Analyze
1. Confirm desired structure against `README.md` and governance docs.
2. Map requested changes to specific directories/files (src, data, tests, etc.).
3. Identify any cascading updates (e.g., README diagrams, prompt references).
4. Pause if the structure change impacts API surface or dataset storage.

## Execute
1. Create/update directories following the `src/` layout and naming conventions.
2. Keep scaffolding minimal—prefer TODOs over speculative code.
3. Update `.gitignore`, tooling configs, and documentation to reflect changes.
4. Avoid removing existing folders without explicit approval.

## Validate
1. Ensure imports still resolve (`pytest -q`).
2. Document new structure in README or prompts as needed.
3. Log material architecture decisions in `governance/DECISIONS_LOG.md`.

## Critic Checklist
- Does the new structure remain easy for QA + LLM collaborators to navigate?
- Are there any governance or prompt updates required?
- Did you avoid introducing unused dependencies or dead scaffolding?
