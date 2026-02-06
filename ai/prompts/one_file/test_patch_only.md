# Prompt: Test Patch Only (Single File)

## Invariant Header
- Deterministic by default; use structured, low-variance output.
- Propose diffs only (explicit patch blocks).
- Do not edit or reveal secrets.
- No internal URLs.
- Repo docs are the source of truth; if a path is unknown, search the repo and reference the correct path.

## Inputs required
- Target test file path
- Behavior to validate (spec/ADR reference)
- Constraints and non-goals
- Expected test outcomes

## Output Template
- Summary
- Scope & assumptions
- Proposed test diff (explicit patch block)
- Rationale (tests as executable specs)
- Decision Log
  - Assumptions
  - Decisions
  - Alternatives considered (1–2)
  - Risks & mitigations
  - Files touched
