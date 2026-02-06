# Prompt: Feature SDD Patch Plan (Orchestrated)

## Invariant Header
- Deterministic by default; use structured, low-variance output.
- Propose diffs only (explicit patch blocks).
- Do not edit or reveal secrets.
- No internal URLs.
- Repo docs are the source of truth; if a path is unknown, search the repo and reference the correct path.

## Inputs required
- Feature request and goals
- Scope boundaries and non-goals
- Relevant spec/ADR/doc paths (or request repo search)
- Constraints, risks, and timelines
- Existing tests or acceptance criteria

## Artifact Update Matrix
- If requirements change → update docs/requirements.md + tests + implementation + status notes (search repo for correct paths).
- If contract changes → update contract docs/tests (search repo for correct paths).
- If demo flow changes → update demo readiness docs/tests (search repo for correct paths).

## Output Template
- Summary
- Scope & assumptions
- Repository paths consulted
- Patch Plan (ordered steps)
- Patch Proposals (explicit diff blocks, if applicable)
- Validation plan (tests as executable specs)
- Decision Log
  - Assumptions
  - Decisions
  - Alternatives considered (1–2)
  - Risks & mitigations
  - Files touched
