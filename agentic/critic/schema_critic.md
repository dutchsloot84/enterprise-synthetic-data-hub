# Schema Critic Checklist
Version: 0.1.0

1. **Scope Confirmation**
   - [ ] Schemas touched? list files + versions.
2. **Structure Review**
   - [ ] All required metadata fields present (version, last_updated, field_count).
   - [ ] Field names align with generator/API usage.
3. **Constraints**
   - [ ] Types/enums consistent with governance.
   - [ ] Cross-entity keys (person_id, vehicle_id) documented.
4. **Validation Hooks**
   - [ ] `schema_validator.py` executed (attach output).
   - [ ] `pytest tests/test_schema_validation.py` run.
5. **Docs & Prompts**
   - [ ] Docs referencing schema updated.
   - [ ] Prompt/task instructions remain accurate.
6. **Findings**
   - Summary:
   - Follow-ups:
