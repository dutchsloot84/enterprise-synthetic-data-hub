# Contributor Quickstart (Demo-Safe)

This proof of concept favors minimal, deterministic changes over sweeping refactors. Use the patterns below to keep the demo stable and governed.

## How to add a field
- Update the relevant Pydantic model (e.g., `src/enterprise_synthetic_data_hub/models/person.py` or `.../vehicle.py`) with the new attribute and validation defaults.
- Thread the field through the generator: extend the source lists/constants and setters in `src/enterprise_synthetic_data_hub/generation/generator.py`.
- Adjust schema tests (`tests/test_schema_person.py`, `tests/test_schema_vehicle.py`) and any smoke contract tests that assert payload shapes.

## How to add a rule
- Append a new rule builder in `src/enterprise_synthetic_data_hub/generation/rules_person.py` or `.../rules_vehicle.py` that returns a descriptive string (used by `/healthz`).
- Apply the rule inside `generator.py` where the entity is constructed; keep random choices seeded via the local `rng` instance to preserve determinism.
- Add a focused test in `tests/generation/` or `tests/api/` that asserts the rule’s outcome without increasing record counts or runtime.

## How to add a new entity (pattern only)
- Mirror the existing structure: create a Pydantic model under `src/enterprise_synthetic_data_hub/models/`, a rules module under `generation/`, and extend `generation/generator.py` with seeded builders plus metadata counts.
- Extend API wiring in `src/enterprise_synthetic_data_hub/api/app.py` following the `/generate/<entity>` pattern, plus a smoke test in `tests/smoke/`.
- Keep the scope demo-sized (do not add auth, scaling, or AI-driven logic) and update sample artifacts under `data/demo_samples/` only if the payload contract changes.
