# Generator Critic Checklist
Version: 0.1.0

1. **Scope Confirmation**
   - [ ] Generator modules touched? list files.
2. **Rule Review**
   - [ ] Deterministic seed usage documented.
   - [ ] Field coverage matches schema definitions.
   - [ ] Cross-entity linking (Person ↔ Vehicle) validated.
3. **Output Inspection**
   - [ ] Sample output stored in `data/output/`.
   - [ ] Metadata includes version + record counts.
4. **Validation Hooks**
   - [ ] `generator_validator.py` executed (attach output).
   - [ ] `pytest tests/test_generator.py` run.
5. **Docs & Prompts**
   - [ ] README/docs updated for new behavior.
   - [ ] Related tasks/prompts updated.
6. **Findings**
   - Summary:
   - Follow-ups:
