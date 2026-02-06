# Prompt: Design Tradeoffs (Explore)

## Invariant Header
- Deterministic by default; use structured, low-variance output.
- Propose diffs only (explicit patch blocks) when suggesting spec/ADR changes.
- Do not edit or reveal secrets.
- No internal URLs.
- Repo docs are the source of truth; if a path is unknown, search the repo and reference the correct path.

## Inputs required
- Problem statement and goals
- Constraints (performance, cost, compliance)
- Relevant repo docs/specs (or request repo search)
- Decision deadline or priority

## Output Template
- Summary
- Options (1–3)
- Tradeoff matrix (short, deterministic)
- Recommendation
- Patch Proposals (explicit diff blocks, if needed)
- Decision Log
  - Assumptions
  - Decisions
  - Alternatives considered (1–2)
  - Risks & mitigations
  - Files touched
