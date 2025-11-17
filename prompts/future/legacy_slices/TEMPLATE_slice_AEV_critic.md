# TEMPLATE – Slice Prompt (AEV + Critic)

## Analyze
1. Review the latest repository state relevant to this slice.
2. Identify constraints from the MOP, governance docs, and decision log.
3. Outline your intended change as a numbered plan.
4. Share questions or risks; pause if human approval is needed.

## Execute
1. Apply the minimal set of changes to satisfy the plan.
2. Keep code modular and well-documented.
3. Leave TODO comments for deferred work instead of partial implementations.
4. Update related docs/prompts when behavior changes.

## Validate
1. Run `pytest` or other relevant checks.
2. Summarize validation outcomes.
3. Capture follow-up tasks, linking back to this prompt if needed.

## Critic Checklist
- Do the changes respect privacy and synthetic-only rules?
- Did you follow the pause-for-approval requirements?
- Are schemas, tests, and docs consistent?
- Are TODOs + next steps clearly documented?
