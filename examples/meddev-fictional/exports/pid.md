# Project Initiation Document

> Vault: `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/meddev-fictional` · Profile: `medical-device`

> _v0.4.0 scaffold — full implementation pending in v1.x. Adopters: fill in the placeholders below and re-run `cb render`._

## 1. Purpose

_[Adopters: state the project's purpose in 1–2 sentences. The pillars below should anchor it.]_

Governing pillars:
- [pillar-disposable-pad-business-model] **Disposable Pad as the Recurring-Revenue Engine** — The Vitalisens Pad is a 7-day replaceable disposable; recurring pad revenue, not the wearable, is the long-term unit economic.
- [pillar-icp-ambulatory-cardiac-patients] **ICP: Adult Ambulatory Cardiac Patients** — We serve adult cardiac patients in ambulatory settings during the 7- to 30-day window after a cardiac event or during arrhythmia workup.
- [pillar-no-pediatric-use] **Non-Goal: We Do Not Pursue Pediatric Use** — Vitalisens will not pursue indications, labeling, marketing, or clinical claims for pediatric patients (under 18) in v1 or v2 of the product.
- [pillar-no-physical-documentation] **Non-Goal: No Physical Documentation** — Vitalisens does not produce printed IFU, printed quick-start cards, printed user manuals, or printed in-box collateral. All documentation is online.

## 2. Scope

_[Adopters: define in-scope and out-of-scope. Reference any non-goal pillars from the decision-log section below.]_

Products in scope:
- [product-vitalisens-cardio] **Vitalisens Cardio** — Adult ambulatory cardiac telemetry wearable; continuous ECG capture, Bluetooth uplink to clinician app, 7-day pad cycle.
- [product-vitalisens-pad] **Vitalisens Pad** — 7-day single-use adhesive sensor pad; couples patient skin to the Vitalisens Cardio wearable; the recurring-revenue consumable.

## 3. Key stakeholders

- [stakeholder-cardiology-program-director] **Stakeholder: Cardiology Program Director (buying decision maker)** — The cardiology program director at a multi-site practice; signs MCT vendor contracts and owns the patient-monitoring SLA.

## 4. Success criteria

_[Adopters: list 3–5 measurable success criteria. Tie each to a decision or a pillar.]_

Decisions on file that shape success criteria:
- [decision-001-online-only-documentation] **Decision 001: Online-Only Documentation** — All Vitalisens documentation (IFU, user manual, quick-start, clinician guide) is electronic only. No printed inserts ship with any product.
- [decision-002-prescription-only-not-otc] **Decision 002: Prescription-Only, Not Over-the-Counter** — Vitalisens will be sold by prescription only (Rx). We will not pursue over-the-counter (OTC) labeling, packaging, or distribution in v1 or v2.
- [decision-003-7-day-wear-not-14-day] **Decision 003: 7-Day Pad Wear Time** — Vitalisens Pad is rated for 7 days of continuous wear. We will not pursue a 14-day variant in v1.

## 5. Risks

- [risk-insight-pad-adhesion-failure-affects-data-quality] **Risk Insight: Pad Adhesion Failure Cascades into Data-Quality Failure** — Pad adhesion failure does not just lose signal — it tends to fail silently, producing noisy data that looks plausible. Detection matters as much as prevention.

## 6. Milestones

_[Adopters: outline 3–6 milestones with target dates. v0.4.0 has no milestone node type; lessons-learned and project-charter cover related lifecycle data.]_

---

> This is a planning artifact. It is not a controlled document and is not part of any design history file, risk management file, or traceability matrix per ISO 14971, IEC 62304, or 21 CFR 820.

_company-brain v0.8.0 · PID scaffold generated 2026-05-27 from vault at `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/meddev-fictional`._
