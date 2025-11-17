# Demo Sub-Prompt – Generate Slide Deck
Version: 0.1.0
Last Updated: 2024-06-03

## Purpose
Author a markdown-based slide deck in `/docs/demo/slides/deck.md` that a presenter can read or convert into slides.

## Inputs
- Completed demo docs under `/docs/demo/0*.md`.
- Repository truths about architecture, generator, validators, and roadmap.

## Slide Requirements
1. Title & executive summary
2. Problem framing + value of synthetic data for insurance
3. Architecture walkthrough (annotate core directories/modules)
4. Slice 01–07 milestone timeline
5. Generator v0.1 spotlight
6. A-E-V + governance practices
7. Roadmap & call to action

## A-E-V Workflow
- **Analyze** – Pull bullet-ready facts from the demo docs.
- **Execute** – Structure slides as markdown sections with `## Slide X – Title` headings and concise bullet lists.
- **Validate** – Ensure the slide order mirrors the presenter script and narrative, contains no placeholders, and stays faithful
  to repo capabilities.

## Completion Criteria
- `deck.md` contains at least seven slides with titles, bullets, and optional callouts/quotes.
- Slides are deterministic and reference real repo artifacts.
