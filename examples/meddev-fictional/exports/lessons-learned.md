# Lessons Learned

> Vault: `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/meddev-fictional` · Profile: `medical-device`

> _v0.4.0 scaffold — full implementation pending in v1.x. Adopters: fill in the placeholders below and re-run `cb render`._

## What worked

_[Adopters: 3–5 bullets on what worked, citing patterns and hypotheses confirmed.]_

Patterns observed:
- [pattern-pad-adhesion-failure-precedes-data-dropout] **Pattern: Pad Adhesion Failure Precedes Data Dropout** — Across the Q1 2026 cohort, every observed data-dropout event was preceded (by hours to days) by partial pad adhesion failure; full detachment is the late stage of a slow drift.

## What didn't

_[Adopters: 3–5 bullets on what didn't work, citing hypotheses falsified or decisions revisited.]_

Hypotheses on file:
- [hypothesis-7-day-wear-improves-compliance] **Hypothesis: 7-Day Wear Improves Patient Compliance vs. 14-Day** — We hypothesize that a 7-day wear cycle drives higher patient compliance (data completeness) than a 14-day cycle, despite the operational overhead of more pad changes.
- [hypothesis-rx-only-preserves-reimbursement] **Hypothesis: Rx-Only Preserves Reimbursement Coding** — We hypothesize that the existing reimbursement coding for ambulatory cardiac monitoring assumes a prescribing physician, and that OTC distribution would jeopardize that coding.

## What we'd do differently

_[Adopters: changes for the next project.]_

## Reusable decisions

Decisions whose rationale travels well beyond this project:
- [decision-001-online-only-documentation] **Decision 001: Online-Only Documentation** — All Vitalisens documentation (IFU, user manual, quick-start, clinician guide) is electronic only. No printed inserts ship with any product.
- [decision-002-prescription-only-not-otc] **Decision 002: Prescription-Only, Not Over-the-Counter** — Vitalisens will be sold by prescription only (Rx). We will not pursue over-the-counter (OTC) labeling, packaging, or distribution in v1 or v2.
- [decision-003-7-day-wear-not-14-day] **Decision 003: 7-Day Pad Wear Time** — Vitalisens Pad is rated for 7 days of continuous wear. We will not pursue a 14-day variant in v1.

## Open questions that surfaced

- [question-second-pad-formulation-for-sensitive-skin] Question: Do We Need a Sensitive-Skin Pad Formulation?
- [question-when-to-pursue-pediatric-clearance] Question: When to Pursue Pediatric Clearance?

---

> This is a planning artifact. It is not a controlled document and is not part of any design history file, risk management file, or traceability matrix per ISO 14971, IEC 62304, or 21 CFR 820.

_company-brain v0.6.0 · lessons-learned scaffold generated 2026-05-25 from vault at `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/meddev-fictional`._
