# Slice 02 – Schema Design (Person + Vehicle)

Use this prompt when adding/changing fields, constraints, or metadata for Person
and Vehicle models.

## Analyze
1. Review current schemas under `src/.../models/` and associated tests.
2. Check governance requirements for IDs, cross-LOB fields, and metadata.
3. Determine whether the change is additive or breaking; pause for approval if
   anything breaks compatibility.
4. Update the change plan in numbered steps.

## Execute
1. Modify schema files with Python 3.10+ typing and pydantic best practices.
2. Never remove `person_id`, `vehicle_id`, or `lob_type` fields.
3. Maintain UUID string formats and documentation.
4. Update dataset metadata and tests to match.
5. Add TODO comments explaining follow-on actions when necessary.

## Validate
1. Run `pytest` focusing on schema tests.
2. Confirm JSON schema examples (if present) are still valid.
3. Update `governance/DECISIONS_LOG.md` if business meaning changes.

## Critic Checklist
- Are global IDs still present and documented?
- Are cross-LOB requirements respected (`lob_type` consistent)?
- Does the change maintain backward compatibility or note migration steps?
- Have tests been updated proportionally?
