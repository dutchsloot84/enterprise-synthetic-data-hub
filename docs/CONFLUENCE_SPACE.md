# Enterprise Synthetic Data Hub Confluence Space (Pilot)

> **Audience fit:** Designed for Leadership & Governance **and** End-Users (QA, Underwriting, Actuarial, Claims Analysts).  
> **Status legend:** ✅ Pilot-ready | 🧭 Future-state | ⭕ Optional | 🔒 Governance/Risk note

---

## 1) Sitemap / Table of Contents

### Space Home (Required ✅)
- **Welcome & Quick Start**
  - One-page overview of the Pilot, what it does today, and who it serves.
  - Links to “Generate Your First Pilot-Ready Dataset” and Governance Portal.
  - 🔒 **Risk note:** Explicitly state “No real or masked PII is used.”

### Knowledge Hub — **Synthetic Data 101 (Insurance Edition)** (Required ✅)
- **1.1 What Synthetic Data *Is* (and Is NOT)** ✅
  - Plain-English definitions, non-technical metaphors, and “Leadership TL;DR.”
- **1.2 Why Synthetic Beats Masked or Anonymized PII** ✅
  - Safety, auditability, and risk reduction framing.
- **1.3 Deterministic Seeds & Reproducibility** ✅
  - Why repeatable data matters for QA and compliance.
- **1.4 Synthetic Markers & Trust Signals** ✅
  - How markers prevent confusion with real data.
- **1.5 Reduced Test Flakiness & Audit Risk** ✅
  - Practical benefits tied to deterministic data and governance.

### Team-Specific Use Cases (Required ✅)
- **2.1 QA / Automation** ✅
- **2.2 Claims** ✅
- **2.3 Underwriting** ✅
- **2.4 Actuarial** ✅

### Interactive Learning Path — **Generate Your First Pilot-Ready Dataset** (Required ✅)
- **3.1 Start Here: 30-Minute Onboarding** ✅
- **3.2 Step-by-Step Learning Path** ✅
- **3.3 Trust Checkpoints** ✅
- **3.4 Reuse & Share Pilot Datasets** ✅

### Governance & Ethics Portal (Required ✅)
- **4.1 PII Safety Guarantees** ✅
- **4.2 Determinism & Reproducibility** ✅
- **4.3 Bias Testing in the Pilot** ✅
- **4.4 NAIC-Style Principles Mapping (High-Level)** ✅
- **4.5 Known Limitations & Non-Goals** ✅

### Feedback Loop — Human-in-the-Loop (Required ✅)
- **5.1 Report a Synthetic Data Bug** ✅
- **5.2 Realism Gap / Edge-Case Miss Log** ✅
- **5.3 Data Issue vs System Issue Triage** ✅
- **5.4 How Feedback Shapes the Roadmap** ✅

### Optional Reference Library (Optional ⭕)
- **CLI Reference** ⭕
- **Demo API Reference (Pilot-only)** ⭕
- **Scenario Catalog & Dataset Index** ⭕
- **Pilot Release Notes** ⭕

---

## 2) Page Templates (with required sections + intent)

> **Template key:**  
> **Required sections** are marked with **[Required]**.  
> **Pilot-ready** content is marked **✅**.  
> **Future-state** content is marked **🧭**.  
> **Leadership TL;DR** is required on Knowledge Hub pages.

---

### Space Home — “Welcome & Quick Start” (Required ✅)
**Intent:** Orient every visitor in under 2 minutes.

**Required Sections**
- **[Required] Purpose of the Pilot (✅):** What the Hub does today and why it exists.
- **[Required] Who This Space Is For (✅):** Leadership & Governance; End-Users.
- **[Required] What You Can Do Today (✅):** Generate deterministic synthetic Persons, Vehicles, Profiles; use CLI; demo Flask API.
- **[Required] What’s Coming Next (🧭):** Roadmap placeholders with clear labels.
- **[Required] Start Here (✅):** Link to Learning Path + Knowledge Hub.
- **[Required] Risk & Compliance Snapshot (✅ 🔒):** “No real or masked PII. Rule-based only.”

---

## 3) Knowledge Hub — “Synthetic Data 101 (Insurance Edition)” (Required ✅)

### 3.1 Page Template: **What Synthetic Data Is (and Is NOT)** ✅
**Intent:** Establish trust and shared vocabulary.

**Required Sections**
- **[Required] Plain-English Definition (✅):**  
  *Synthetic data is **manufactured data** created by rules and patterns—not derived from real policyholders or claims.*
- **[Required] What It Is NOT (✅ 🔒):**  
  “Not masked PII. Not anonymized PII. Not a subset of real data.”
- **[Required] Conceptual Metaphor (✅):**  
  *“Movie set vs real city”*: looks realistic, but nothing inside is real.
- **[Required] Why It Matters in Insurance (✅):**  
  Safe test data without legal exposure.
- **[Required] Leadership TL;DR (✅):**  
  3 bullets: safety, repeatability, audit clarity.

### 3.2 Page Template: **Why Synthetic Beats Masked or Anonymized PII** ✅
**Intent:** Address governance and legal comfort directly.

**Required Sections**
- **[Required] Risk Comparison Table (✅ 🔒):** Synthetic vs masked vs anonymized.
- **[Required] Safer by Design (✅):** Rule-based generation, no linkage to real people.
- **[Required] Auditability (✅):** Clear provenance, deterministic seeds.
- **[Required] Leadership TL;DR (✅).**

### 3.3 Page Template: **Deterministic Seeds & Reproducibility** ✅
**Intent:** Explain how repeatability drives trust and QA quality.

**Required Sections**
- **[Required] Plain-English Explanation (✅):**  
  *A “seed” is a repeatable starting point; same inputs = same outputs.*
- **[Required] Why QA Cares (✅):** Eliminates flaky test data.
- **[Required] Why Governance Cares (✅ 🔒):**  
  Enables audit trails; proves dataset provenance.
- **[Required] Leadership TL;DR (✅).**

### 3.4 Page Template: **Synthetic Markers & Trust Signals** ✅
**Intent:** Remove confusion about whether data is real.

**Required Sections**
- **[Required] What is a Synthetic Marker? (✅):**  
  A visible indicator embedded in data to signal “synthetic.”
- **[Required] Why Markers Matter (✅ 🔒):**  
  Prevents accidental misuse, improves transparency.
- **[Required] How to Recognize Markers (✅):**  
  Example of tagged fields in CSV/JSON (no real values).
- **[Required] Leadership TL;DR (✅).**

### 3.5 Page Template: **Reduced Test Flakiness & Audit Risk** ✅
**Intent:** Tie technical design to measurable outcomes.

**Required Sections**
- **[Required] QA Impact (✅):** Stable tests, fewer false failures.
- **[Required] Governance Impact (✅ 🔒):** Predictable, repeatable evidence.
- **[Required] Leadership TL;DR (✅).**

---

## 4) Team-Specific Use Cases (Required ✅)

### 4.1 QA / Automation (Required ✅)
**Intent:** Immediate test-data clarity and reliability.

**Required Sections**
- **[Required] Current Pain (✅):** Flaky tests, data access delays, compliance review.
- **[Required] Pilot Solution (✅):** Deterministic synthetic datasets with seeds.
- **[Required] Example Requests (✅):**  
  “1000 synthetic auto claims with shared vehicle IDs.”
- **[Required] Success Metrics (✅):**  
  *Qualitative:* reduced triage time.  
  *Quantitative:* fewer test reruns; faster CI cycles.

### 4.2 Claims (Required ✅)
**Intent:** Validate workflows without exposure to real claims data.

**Required Sections**
- **[Required] Current Pain (✅):** Limited access, restricted claims data, manual approval.
- **[Required] Pilot Solution (✅):** Synthetic claim scenarios for training and testing.
- **[Required] Example Requests (✅):**  
  “Bodily injury claims with staged fraud signals.”
- **[Required] Success Metrics (✅).**

### 4.3 Underwriting (Required ✅)
**Intent:** Model validation without PII risk.

**Required Sections**
- **[Required] Current Pain (✅):** PII risk in underwriting datasets.
- **[Required] Pilot Solution (✅):** Rule-based policyholder profiles.
- **[Required] Example Requests (✅):**  
  “Commercial auto risk profiles by state.”
- **[Required] Success Metrics (✅).**

### 4.4 Actuarial (Required ✅)
**Intent:** Scenario testing and loss modeling for the pilot.

**Required Sections**
- **[Required] Current Pain (✅):** Restricted data access; difficult scenario replication.
- **[Required] Pilot Solution (✅):** Deterministic datasets for repeatable scenarios.
- **[Required] Example Requests (✅):**  
  “Catastrophe-style claim frequency simulations.”
- **[Required] Success Metrics (✅).**

---

## 5) Interactive Learning Path — “Generate Your First Pilot-Ready Dataset” (Required ✅)

### 5.1 Page Template: **Start Here: 30-Minute Onboarding** ✅
**Intent:** Zero-to-first dataset with confidence.

**Required Sections**
- **[Required] What You’ll Learn (✅):** Request → Generate → Validate → Reuse.
- **[Required] Time & Tools (✅):** CLI, optional API, sample artifacts.
- **[Required] Trust Checkpoints (✅ 🔒):**  
  “How do I know this is synthetic?”
- **[Required] Expected Outputs (✅):** CSV, JSON, manifest, README.

### 5.2 Page Template: **Step-by-Step Learning Path** ✅
**Intent:** Teach *why* each step exists.

**Required Steps**
1. **Request (✅):** Define scenario + seed. *Why:* ensures reproducibility.
2. **Generate (✅):** Run CLI or API. *Why:* deterministic outputs.
3. **Validate (✅ 🔒):** Check synthetic markers + manifest. *Why:* trust & audit.
4. **Reuse (✅):** Save outputs, share in team catalog. *Why:* consistency.

**Callouts**
- **CLI vs API vs Artifact Reuse (✅):** When to use each pathway.

### 5.3 Page Template: **Trust Checkpoints** ✅
**Intent:** Reduce “Is this real?” confusion.

**Required Sections**
- **[Required] Synthetic Marker Check (✅ 🔒)**
- **[Required] Deterministic Seed Check (✅)**
- **[Required] Manifest Review (✅ 🔒)**

### 5.4 Page Template: **Reuse & Share Pilot Datasets** ✅
**Intent:** Enable rapid adoption across teams.

**Required Sections**
- **[Required] Dataset Naming Standards (✅)**
- **[Required] Storage Locations (✅)**
- **[Required] Reuse Do/Don’t List (✅ 🔒)**

---

## 6) Governance & Ethics Portal (Required ✅)

### 6.1 Page Template: **PII Safety Guarantees** ✅
**Intent:** Clear, non-negotiable safety statements.

**Required Sections**
- **[Required] Non-PII Guarantee (✅ 🔒):** “No real or masked PII.”
- **[Required] Rule-Based Generation (✅):** All records are synthetic.
- **[Required] Audit Readiness (✅ 🔒):** Traceable seeds and manifests.

### 6.2 Page Template: **Determinism & Reproducibility** ✅
**Intent:** Explain how audit trails are supported.

**Required Sections**
- **[Required] Deterministic Inputs (✅)**
- **[Required] Provenance & Seeds (✅ 🔒)**
- **[Required] Reproducibility Example (✅):** Same seed → same dataset.

### 6.3 Page Template: **Bias Testing in the Pilot** ✅
**Intent:** Honest baseline, no overclaims.

**Required Sections**
- **[Required] What We Test Today (✅):** Basic distribution checks.
- **[Required] What We Don’t Yet Test (🧭):** Advanced fairness metrics.
- **[Required] How Issues Are Logged (✅):** Link to Feedback Loop.

### 6.4 Page Template: **NAIC-Style Principles Mapping (High-Level)** ✅
**Intent:** Align with governance expectations without legal claims.

**Required Sections**
- **[Required] Principle-Based Mapping (✅ 🔒):** Transparency, accountability, auditability.
- **[Required] Not Legal Advice Disclaimer (✅ 🔒).**

### 6.5 Page Template: **Known Limitations & Non-Goals** ✅
**Intent:** Radical transparency.

**Required Sections**
- **[Required] Pilot Limitations (✅ 🔒):** Not production-scale; demo API only.
- **[Required] Non-Goals (✅ 🔒):** No real-world decisioning.
- **[Required] Future-State Roadmap (🧭).**

---

## 7) Feedback Loop — Human-in-the-Loop (Required ✅)

### 7.1 Page Template: **Report a Synthetic Data Bug** ✅
**Intent:** Simple path to report issues.

**Required Sections**
- **[Required] Bug Definition (✅):** Data is inconsistent or implausible.
- **[Required] Submission Template (✅):**  
  Dataset name, seed, expected vs actual.
- **[Required] Ownership & SLA (✅):** Who triages and when.

### 7.2 Page Template: **Realism Gap / Edge-Case Miss Log** ✅
**Intent:** Capture missing scenarios for future enhancements.

**Required Sections**
- **[Required] What to Log (✅):** Missing claim types, rare events.
- **[Required] Prioritization Criteria (✅):** Impact on pilot use cases.

### 7.3 Page Template: **Data Issue vs System Issue Triage** ✅
**Intent:** Reduce churn and speed resolution.

**Required Sections**
- **[Required] Decision Tree (✅):** Data quality vs platform defect.
- **[Required] Escalation Path (✅).**

### 7.4 Page Template: **How Feedback Shapes the Roadmap** ✅
**Intent:** Show feedback impact.

**Required Sections**
- **[Required] Monthly Review Cadence (✅)**
- **[Required] Public Backlog (✅)**
- **[Required] “You Said, We Did” Summary (✅)**

---

## 8) Inline Notes & Adoption/Governance Callouts

Use these callouts consistently across pages:
- **Adoption Callout:** “New? Start with the 30-minute Learning Path.”  
- **Governance Callout (🔒):** “No real or masked PII. Synthetic only.”  
- **Pilot vs Future Callout:** “✅ Pilot-ready today | 🧭 Roadmap item.”

