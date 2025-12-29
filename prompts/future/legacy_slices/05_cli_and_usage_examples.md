# Slice 05 – CLI & Usage Examples

Use this prompt when extending the CLI, documentation snippets, or developer
workflows related to running the generator/exporters.

## Analyze
1. Review `cli/main.py` and README quickstart instructions.
2. Identify user stories (QA engineer, data steward, etc.) that require CLI
   support.
3. Determine whether new commands alter governance expectations (pause if so).
4. Plan how usage examples will be documented.

## Execute
1. Extend the CLI with argparse or similar tooling; keep UX simple.
2. Provide usage examples in README or dedicated docs.
3. Wire CLI commands into generation/export pipelines once available.
4. Include TODO markers for features deferred to future phases.

## Validate
1. Run CLI smoke tests locally (e.g., `python -m ... generate-snapshot`).
2. Update automated tests if CLI behavior becomes more complex.
3. Ensure docs match actual command syntax/output.

## Critic Checklist
- Is the CLI intuitive for QA engineers with minimal Python background?
- Are examples accurate and reproducible?
- Do commands respect governance (e.g., dataset versioning)?
- Are next steps clearly identified when functionality is stubbed?
