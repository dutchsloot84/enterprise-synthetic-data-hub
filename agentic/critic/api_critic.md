# API Critic Checklist
Version: 0.1.0

1. **Scope Confirmation**
   - [ ] API modules touched? list files/routes.
2. **Contract Review**
   - [ ] Route paths versioned correctly (e.g., `/v0.1/...`).
   - [ ] Request/response payloads align with schemas.
3. **Dependency Review**
   - [ ] Required packages listed (Flask/FastAPI etc.).
   - [ ] Environment variables/config documented.
4. **Validation Hooks**
   - [ ] `api_validator.py` executed (attach output).
   - [ ] `pytest tests/test_api.py` run.
5. **Docs & Prompts**
   - [ ] `/docs/api.md` updated as needed.
   - [ ] Task/prompt instructions remain accurate.
6. **Findings**
   - Summary:
   - Follow-ups:
