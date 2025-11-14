# Slice 06 – Governance & Data Versions

Use this prompt when updating governance docs, decision logs, or dataset version
metadata.

## Analyze
1. Review existing content in `governance/` and metadata models.
2. Identify what policy or version change is required and why.
3. Determine whether the change affects downstream consumers; if so, pause for
   human approval.
4. Outline the update plan referencing impacted files.

## Execute
1. Edit governance markdown files with clear bullet points and rationale.
2. Update `DECISIONS_LOG.md` for every notable decision.
3. Adjust dataset metadata defaults/settings when bumping versions.
4. Communicate version changes in README and prompt docs.

## Validate
1. Ensure new governance rules align with legal/privacy expectations.
2. Confirm dataset version references match across code, docs, and data folders.
3. Solicit reviewer sign-off for policy changes.

## Critic Checklist
- Are roles/responsibilities clearly articulated?
- Is the dataset version history traceable and auditable?
- Did the update maintain alignment with the MOP pause checkpoints?
- Are next actions for implementers unambiguous?
