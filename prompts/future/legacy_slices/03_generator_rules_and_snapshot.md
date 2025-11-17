# Slice 03 – Generator Rules & Snapshot Creation

Use this prompt when implementing or modifying the rule-based generator and
snapshot materialization workflow.

## Analyze
1. Review `generation/` modules, config settings, and metadata requirements.
2. Confirm target record counts (~200 Persons, >=1 Vehicle each).
3. Ensure snapshot must remain deterministic for the POC.
4. Identify data formats that need realistic shapes (VIN, DL, postal codes).
5. Pause for approval before changing schema fields or dataset version numbers.

## Execute
1. Implement deterministic rule-based generation respecting governance rules.
2. Use `settings.random_seed` and store outputs under `data/snapshots/<version>/`.
3. Guarantee every Person has at least one Vehicle.
4. Record dataset metadata with accurate counts.
5. Update CLI/exporters/tests when behavior changes.

## Validate
1. Run `pytest` plus any targeted validators.
2. Optionally lint generation scripts for clarity.
3. Document snapshot contents in `data/snapshots/<version>/README...`.

## Critic Checklist
- Are privacy-safe rules followed (no real data)?
- Does the snapshot remain stable across runs?
- Are VIN/DL formats realistic and validated?
- Did you update metadata/version references consistently?
