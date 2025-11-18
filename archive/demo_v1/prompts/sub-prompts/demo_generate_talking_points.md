# Demo Sub-Prompt – Generate Presenter Talking Points
Version: 0.1.0
Last Updated: 2024-06-03

## Purpose
Craft a presenter-ready script stored at `/docs/demo/talking-points/presenter_script.md`. The script should mirror the slide
ordering and provide cues, transitions, and optional Q&A prompts.

## Inputs
- Slide deck from `/docs/demo/slides/deck.md`.
- Demo docs 00–05 for deeper context.

## Script Structure
1. Opening (hook + executive summary)
2. Slide-by-slide narration (one subsection per slide)
3. Anticipated stakeholder questions with short answers
4. Closing + CTA

## A-E-V Workflow
- **Analyze** – Review each slide and supporting doc for precise wording.
- **Execute** – Write in first-person presenter voice, referencing tangible artifacts (directories, validators, snapshots).
- **Validate** – Confirm the script is deterministic, free of placeholders, and ready for handoff to any presenter.

## Completion Criteria
- Script contains headings for each slide and explicit cues such as timing, handoffs, or demos.
- Includes at least three anticipated Q&A items aligned with repo realities.
