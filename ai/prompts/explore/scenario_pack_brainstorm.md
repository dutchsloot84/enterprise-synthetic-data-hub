# Prompt: Scenario Pack Brainstorm (Explore)

## Invariant Header
- Deterministic by default; use structured, low-variance output.
- Propose diffs only (explicit patch blocks) when suggesting spec/ADR changes.
- Do not edit or reveal secrets.
- No internal URLs.
- Repo docs are the source of truth; if a path is unknown, search the repo and reference the correct path.

## Inputs required
- Domain and target audience
- Constraints and non-goals
- Existing scenario docs (or request repo search)
- Coverage gaps to address

## Output Template
- Summary
- Scenario list (bounded, numbered)
- Coverage notes
- Patch Proposals (explicit diff blocks, if needed)
- Decision Log
  - Assumptions
  - Decisions
  - Alternatives considered (1–2)
  - Risks & mitigations
  - Files touched
