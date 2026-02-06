# Insurance Compliance Guardrails (compliance_guardrails.md)

## 1) NAIC Model AI Bulletin Alignment (Pilot Minimum)
The Synthetic Data Hub must align with NAIC Model AI Bulletin principles: transparency, accountability, fairness, and data governance. The guardrails below are mandatory for any Pilot dataset release.

## 2) Mandatory PII Scrubbing Rules — Person Schema
These rules apply **regardless** of synthetic origin to prevent accidental realism or risk of re-identification.

### 2.1 Direct Identifiers
- **person_id:** Must be a UUID generated within the system (no external IDs).
- **driver_license_number:** Must be synthetic and conform to the approved regex pattern; real-world formatting or state-specific issuance rules must not be used.

### 2.2 Quasi-Identifiers
- **date_of_birth:** Must stay within approved ranges and be validated as a real calendar date.
- **address_line_1 / address_line_2 / city / postal_code:** Must be synthetic; no real addresses, PO boxes tied to real facilities, or precise geolocation.
- **postal_code:** Must stay within curated pilot ranges; avoid full ZIP+4 where it could imply real households.

### 2.3 Sensitive Combinations
- Disallow combinations that could be mistaken for real customers (e.g., full name + exact DOB + full street address).
- At least one of the following must be generalized when emitting a Person record:
  - street address precision (e.g., use synthetic numbering without real street names)
  - DOB granularity (e.g., year-only buckets when appropriate for external shares)

## 3) “No Claims Advice” Rule
The AI **must never** generate legal or claims advice in any field (including notes, metadata, or free-text fields). This applies to any future “notes” fields and API responses.

**Examples of prohibited output:**
- “File a claim within 30 days to preserve rights.”
- “You are entitled to coverage under policy section 2.1.”

## 4) Audit & Accountability
- Every dataset export must record: who triggered the export, timestamp, seed, dataset version, and the outcome of fidelity gates.
- Any compliance failure must block export and surface the reason in the audit log.
