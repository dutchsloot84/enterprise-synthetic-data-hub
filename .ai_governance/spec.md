# Synthetic Data Hub Pilot — Technical Constitution (spec.md)

## 1) Purpose & Scope
This specification establishes the governed, pilot-ready rules for synthetic insurance data generation. The intent is to prevent drift from compliance and fidelity requirements while enabling deterministic, auditable datasets.

## 2) Data Fidelity Targets (v0.1 Baseline)
These targets are mandatory for every dataset generated for Pilot export:

### 2.1 Line of Business (LOB) Weighting
- **Personal:** 70%
- **Commercial:** 30%

**Rationale:** Reflects current QA target mix for pilot scenarios while maintaining Commercial coverage for Mobilitas use cases.

### 2.2 Vehicle Year Range
- **Model Year:** 2008–2024 (inclusive)

**Rationale:** Aligns to late-model fleet distribution and avoids legacy extremes in early pilot data.

### 2.3 Geographic Coverage (POC Region)
- **Allowed States:** CA, AZ, NV, OR, WA
- **Postal Codes:** Must remain within curated state-specific ranges.

**Rationale:** Constrains synthetic outputs to the POC service footprint until pilot expansion is approved.

### 2.4 Determinism & Reproducibility
- All pilot datasets must be reproducible from a recorded seed and dataset version.
- Dataset metadata must include generation timestamp, record counts, and the seed used.

## 3) Schema Versioning Policy

### 3.1 Version Format
- Use semantic versioning: `vMAJOR.MINOR` (e.g., v0.1).

### 3.2 Non-Breaking Changes (MINOR)
A change is **non-breaking** if it:
- Adds optional fields only.
- Adds new enum values without removing existing values.
- Adds documentation-only updates (descriptions/examples) that do not alter validation.

### 3.3 Breaking Changes (MAJOR)
A change is **breaking** if it:
- Removes or renames fields.
- Changes required/optional status of existing fields.
- Narrows validation constraints (e.g., tighter ranges, regex updates) that could invalidate existing datasets.
- Changes referential integrity rules (e.g., cardinality between Person and Vehicle).

### 3.4 Governance for Version Bumps
- **Non-breaking:** Data Steward approval required.
- **Breaking:** Product Owner + Line-of-Business (LOB) sign-off required.
- Every schema change must update versioned artifacts and be recorded in the Decisions Log.

## 4) Fidelity Gates (Pre-Export Statistical Tests)
All datasets must pass **all** fidelity gates prior to export:

1. **Kolmogorov–Smirnov (KS) Test — DOB / Age Distribution**
   - Compare synthetic DOB/age distribution against the approved baseline distribution.
   - Fail if KS statistic exceeds configured threshold.

2. **Chi-Square Test — LOB Distribution**
   - Validate observed LOB counts against the 70/30 target.
   - Fail if p-value falls below configured significance level.

3. **Z-Test (Proportion) — Vehicle Model Year Bands**
   - Validate proportions across year bands (2008–2012, 2013–2018, 2019–2024) against baseline targets.
   - Fail if any band deviates beyond configured tolerance.

## 5) Export Preconditions
- All fidelity gates pass.
- Schema version and metadata are populated.
- Synthetic marker present on every entity.
- Audit log entry recorded for the export action.

## 6) Future Expansion (Out of Scope for v0.1)
- Policy and Claim schemas.
- Distribution to external storage (S3/Snowflake).
- Production auth and rate limiting.
