# Governance Overview

This proof of concept is intentionally small yet enterprise-aligned. To keep the
work auditable and extendable:

- **Who can propose schema changes?** Test leads, product owners, and designated
data stewards may open issues/PRs. LLM agents must include human reviewers
before merging schema modifications.
- **Decision logging.** All major changes (schema, generator logic, data access)
must be captured in `DECISIONS_LOG.md` along with rationale and approval notes.
- **Prompt discipline.** LLM agents must follow the Master Operating Prompt
(MOP) and AEV + Critic processes in `/prompts` before executing significant
changes.
- **Pause-for-approval checkpoints.** Schema, generator, and dataset version
changes require explicit confirmation from a human owner prior to execution.

This governance layer is intentionally lightweight but enforces consistent
communication between QA, engineering, data stewards, and AI collaborators.
