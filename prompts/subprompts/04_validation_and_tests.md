# Slice 04 – Validation & Tests

Apply this prompt when enhancing validators, schema checks, or pytest suites.

## Analyze
1. Catalog current tests under `tests/` and validation utilities.
2. Identify coverage gaps relative to recent schema/generator changes.
3. Determine if new fixtures or sample data are required.
4. Pause for approval if expanding into integration/performance testing.

## Execute
1. Add or update pytest modules with clear assertions.
2. Keep test data synthetic and minimal.
3. Enhance `validation/` utilities to cover new rules, ensuring reusability.
4. Update README/governance references if testing strategy shifts.

## Validate
1. Run `pytest` and capture output in PR description.
2. Note any flaky behavior or follow-up tasks.
3. Ensure CI instructions remain accurate.

## Critic Checklist
- Do tests meaningfully cover the targeted behavior?
- Are failures actionable and easy for QA to interpret?
- Did you avoid overfitting tests to implementation details?
- Are validators consistent with governance rules?
