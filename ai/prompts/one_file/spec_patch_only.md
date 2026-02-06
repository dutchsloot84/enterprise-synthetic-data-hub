# Prompt: Spec Patch Only (Single File)

## Invariant Header
- Deterministic by default; use structured, low-variance output.
- Propose diffs only (explicit patch blocks).
- Do not edit or reveal secrets.
- No internal URLs.
- Repo docs are the source of truth; if a path is unknown, search the repo and reference the correct path.

## Inputs required
- Target spec/ADR file path
- Change request and rationale
- Acceptance criteria
- Constraints and non-goals

## Output Template
- Summary
- Scope & assumptions
- Proposed spec diff (explicit patch block)
- Acceptance criteria (testable)
- Decision Log
  - Assumptions
  - Decisions
  - Alternatives considered (1–2)
  - Risks & mitigations
  - Files touched
