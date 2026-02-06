# Synthetic Data Hub Pilot — Roadmap

## Goal
Create a repository environment where AI assistants cannot hallucinate or drift from insurance-specific compliance and fidelity constraints.

---

## Phase 1: Compliance Integration (Auth & PII Scrubbing)
**Objective:** Ensure every synthetic dataset is protected by compliance guardrails.

**Key Deliverables**
1. **Authentication & Authorization**
   - Add optional API auth middleware (env-driven) for all non-demo environments.
2. **PII Scrubbing & Validation**
   - Implement validation rules aligned with `compliance_guardrails.md`.
3. **Audit Logging**
   - Record exports with seed, dataset version, fidelity gate status, and actor identity.

**Exit Criteria**
- All Person records conform to mandatory PII scrubbing rules.
- Export actions are blocked on compliance failure.

---

## Phase 2: Fidelity Validation (Statistical Tests)
**Objective:** Enforce statistical fidelity before export.

**Key Deliverables**
1. **Fidelity Gate Test Suite**
   - Implement KS test for DOB/age distribution.
   - Implement Chi-square test for LOB distribution.
   - Implement Z-test for vehicle model year bands.
2. **Baseline Distributions**
   - Define and version baseline distributions in a governed config.
3. **Automated Enforcement**
   - Fail export if any fidelity gate fails.

**Exit Criteria**
- All datasets pass fidelity gates before export.
- Results are logged and traceable to a dataset version.

---

## Phase 3: Human-in-the-Loop (Approval Workflow)
**Objective:** Embed governance approvals into the delivery pipeline.

**Key Deliverables**
1. **Approval Workflow**
   - Add review checkpoints for schema and generator changes.
2. **Release Sign-Off**
   - Require Data Steward and Product Owner approvals based on versioning policy.
3. **Audit Trail**
   - Integrate decision log updates and approvals into release artifacts.

**Exit Criteria**
- Changes to schema/generator are blocked without approvals.
- All releases reference a decision log entry and audit record.
