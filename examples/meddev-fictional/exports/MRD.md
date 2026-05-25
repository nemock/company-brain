# Marketing Requirements Document

> Vault: `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/meddev-fictional` · Profile: `medical-device`

## 1. Executive summary

The 2 governing principles of this company shape every section that follows. The product set is anchored on 2 products, positioned against 2 known competitors.

**Top principles:**
- [pillar-disposable-pad-business-model] **Disposable Pad as the Recurring-Revenue Engine** — The Vitalisens Pad is a 7-day replaceable disposable; recurring pad revenue, not the wearable, is the long-term unit economic.
- [pillar-icp-ambulatory-cardiac-patients] **ICP: Adult Ambulatory Cardiac Patients** — We serve adult cardiac patients in ambulatory settings during the 7- to 30-day window after a cardiac event or during arrhythmia workup.

**What we are explicitly not doing** (full detail in §10):
- [pillar-no-pediatric-use] Non-Goal: We Do Not Pursue Pediatric Use
- [pillar-no-physical-documentation] Non-Goal: No Physical Documentation

## 2. Vision and positioning

The company's positioning rests on the following pillars:

### Disposable Pad as the Recurring-Revenue Engine [pillar-disposable-pad-business-model]

The Vitalisens Pad is a 7-day replaceable disposable; recurring pad revenue, not the wearable, is the long-term unit economic.

_Applies when:_ pricing, business model, pad, disposable, recurring revenue, unit economics, LTV, reimbursement, channel

### ICP: Adult Ambulatory Cardiac Patients [pillar-icp-ambulatory-cardiac-patients]

We serve adult cardiac patients in ambulatory settings during the 7- to 30-day window after a cardiac event or during arrhythmia workup.

_Applies when:_ ICP, target market, audience, indication scope, patient population, who we serve, expansion, pediatric, geriatric, in-patient, home-health


**Vision sources** (founder-vision, strategic-thesis, domain-expertise):

- [source-domain-expertise-saunders-cardiology-2026] _domain-expertise_ — Domain Expertise: Saunders, 20 Years of Cardiology Workflow
- [source-strategic-thesis-disposable-pad-recurring-revenue] _strategic-thesis_ — Strategic Thesis: Disposable Pad as Recurring Revenue Engine
- [source-vision-saunders-2026-cardiac-workflow-thesis] _founder-vision_ — Founder Vision: The Cardiac Workflow Bottleneck (Saunders, 2026)


## 3. Indications for use

**Our IFU:**

### IFU: Vitalisens Cardio (planned, 2026 Q1) [indication-for-use-vitalisens-cardio-2026-q1]

- **Population:** Adult patients aged 18 years and older
- **Condition:** Suspected cardiac arrhythmia or post-cardiac-event surveillance
- **Intervention:** Continuous ambulatory ECG recording over a 7-day pad cycle, transmitted to a clinician-reviewable application
- **Setting:** Home and outpatient clinical settings; not for in-patient acute monitoring


**IFU comparison matrix** (latest IFU per product):

| Product | Population | Condition | Intervention | Setting |
|---|---|---|---|---|
| Vitalisens Cardio [indication-for-use-vitalisens-cardio-2026-q1] | Adult patients aged 18 years and older | Suspected cardiac arrhythmia or post-cardiac-event surveillance | Continuous ambulatory ECG recording over a 7-day pad cycle, transmitted to a clinician-reviewable application | Home and outpatient clinical settings; not for in-patient acute monitoring |

## 4. Market and personas

**Personas:**

- [persona-ambulatory-cardiac-patient] **Persona: Ambulatory Cardiac Patient** — Adult patient discharged from cardiology service with continuous-monitoring orders for 7-30 days; mobile, lives at home, manages own pad changes.


**Named customer references:**

- [customer-northstar-cardiology-2025] Northstar Cardiology Group (trial customer) — Fictional multi-site cardiology group; first trial customer; running a 14-patient pilot during Q1-Q2 2026.

## 5. Market requirements

- [requirement-mkt-001-continuous-ecg-during-ambulatory] **Market Requirement: Continuous ECG During Ambulatory Use** — Cardiologists need continuous (not intermittent) ECG capture during the ambulatory window; intermittent recording misses paroxysmal events.

## 6. Competitive landscape

### CardioTrace Inc [competitor-cardiotrace-inc]

Direct fictional competitor in adult ambulatory cardiac telemetry; two 510(k) clearances with expanding IFU history; competes head-on with Vitalisens.

- **Canonical URL:** https://cardiotrace-inc.example.com
- **IFU history:** [indication-for-use-cardiotrace-pro-2023-q1], [indication-for-use-cardiotrace-pro-2025-q3]
- **Clearances:** [regulatory-clearance-K181234-cardiotrace-pro-v1], [regulatory-clearance-K231234-cardiotrace-pro-v2]

### PulseGuard Medical [competitor-pulseguard-medical]

Adjacent fictional competitor; alternative architecture (in-clinic placement, in-home pad change); one 510(k) clearance frequently used as predicate.

- **Canonical URL:** https://pulseguard-medical.example.com
- **IFU history:** [indication-for-use-pulseguard-rhythm-2022-q4]
- **Clearances:** [regulatory-clearance-K221567-pulseguard-rhythm]



## 7. Regulatory landscape

**Clearances tracked:**

| Clearance | Type | Applicant | Device | Date | Predicates |
|---|---|---|---|---|---|
| [regulatory-clearance-K181234-cardiotrace-pro-v1] `K181234` | 510k | CardioTrace Inc | CardioTrace Pro | 2023-02-14 |  |
| [regulatory-clearance-K221567-pulseguard-rhythm] `K221567` | 510k | PulseGuard Medical Devices LLC | PulseGuard Rhythm | 2022-11-08 |  |
| [regulatory-clearance-K231234-cardiotrace-pro-v2] `K231234` | 510k | CardioTrace Inc | CardioTrace Pro (expanded indication) | 2025-08-30 | [regulatory-clearance-K181234-cardiotrace-pro-v1], [regulatory-clearance-K221567-pulseguard-rhythm] |
| [regulatory-clearance-K243189-vitalisens-cardio] `K243189` | 510k | Vitalisens (fictional) | Vitalisens Cardio | 2026-12-31 | [regulatory-clearance-K221567-pulseguard-rhythm], [regulatory-clearance-K231234-cardiotrace-pro-v2] |


**Regulations referenced:**
- [regulation-21-cfr-820-design-controls] Regulation: 21 CFR 820 (Quality System Regulation / Design Controls) — US FDA quality system regulation, including design controls subpart C. Vitalisens' controlled-document boundary is informed by this regulation.


**Standards referenced:**
- [standard-iso-14971-risk-management] Standard: ISO 14971 (Risk Management) — International standard for risk management of medical devices. Vitalisens uses its vocabulary for planning-level risk thinking; the controlled risk management file would also conform.

## 8. Evidence vs. vision split

A breakdown of which claims in this vault are grounded in evidence (customer interviews, market data, internal telemetry, FDA filings, web snapshots, press releases) and which are vision-driven (founder vision, strategic thesis, domain expertise). Both are legitimate; conflating them silently is the failure mode this section prevents.

- **Evidence-derived claims:** 7
- **Vision-derived claims:** 4
- **Uncited claims:** 14 _(should be addressed — every load-bearing claim should derive from a source)_

**Uncited claims to address:**
- [decision-001-online-only-documentation] Decision 001: Online-Only Documentation
- [decision-003-7-day-wear-not-14-day] Decision 003: 7-Day Pad Wear Time
- [fact-current-team-size-2026-q2] Fact: Team Size — 2026 Q2
- [fact-pad-attach-rate-2026-q2] Fact: Pad Attach Rate at Day 1 — 2026 Q2 Cohort (interim)
- [fact-stripe-fee-2-9-percent-plus-30c] Fact: Stripe US Card Processing Fee
- [hypothesis-7-day-wear-improves-compliance] Hypothesis: 7-Day Wear Improves Patient Compliance vs. 14-Day
- [hypothesis-rx-only-preserves-reimbursement] Hypothesis: Rx-Only Preserves Reimbursement Coding
- [indication-for-use-pulseguard-rhythm-2022-q4] IFU: PulseGuard Rhythm (2022 Q4)
- [indication-for-use-vitalisens-cardio-2026-q1] IFU: Vitalisens Cardio (planned, 2026 Q1)
- [pillar-no-pediatric-use] Non-Goal: We Do Not Pursue Pediatric Use
- [regulatory-clearance-K181234-cardiotrace-pro-v1] 510(k) K181234 — CardioTrace Pro (original)
- [regulatory-clearance-K221567-pulseguard-rhythm] 510(k) K221567 — PulseGuard Rhythm
- [regulatory-clearance-K243189-vitalisens-cardio] 510(k) K243189 — Vitalisens Cardio (planned)
- [requirement-sys-001-7-day-battery] System Requirement: 7-Day Continuous Battery Life

## 9. Open questions

- [question-second-pad-formulation-for-sensitive-skin] **Question: Do We Need a Sensitive-Skin Pad Formulation?** — How many trial patients experience irritation severe enough to discontinue, and would a sensitive-skin pad variant address it in a tractable way?
- [question-when-to-pursue-pediatric-clearance] **Question: When to Pursue Pediatric Clearance?** — Under what conditions would Vitalisens flip from the non-pediatric pillar to actively pursuing a pediatric indication?

## 10. What we are explicitly not doing


**Non-goal pillars** (durable boundaries):

### Non-Goal: We Do Not Pursue Pediatric Use [pillar-no-pediatric-use]

Vitalisens will not pursue indications, labeling, marketing, or clinical claims for pediatric patients (under 18) in v1 or v2 of the product.

_Applies when:_ pediatric, child, children, adolescent, under-18, school-age, infant, neonatal, age-restricted indication, IFU expansion to younger populations

### Non-Goal: No Physical Documentation [pillar-no-physical-documentation]

Vitalisens does not produce printed IFU, printed quick-start cards, printed user manuals, or printed in-box collateral. All documentation is online.

_Applies when:_ documentation, IFU, user manual, quick start, in-box, packaging insert, printed insert, leaflet, instructions for use printing, e-IFU, electronic instructions for use, paper documentation


**Decisions and what they rule out:**

### Decision 001: Online-Only Documentation [decision-001-online-only-documentation]

- **Printed IFU inserts.** The IFU is not printed at any point in the supply chain.
- **Printed quick-start cards.** No "getting started" cards ship in the box.
- **Printed user manuals.** No paper manuals are distributed.
- **Distributor-printed collateral.** Distributors are contractually prohibited from generating their own printed versions of the IFU or user manual.
- **PDF-by-email as the documentation distribution channel.** Documentation must live at a stable URL, not be emailed.

### Decision 002: Prescription-Only, Not Over-the-Counter [decision-002-prescription-only-not-otc]

- **OTC labeling.** Packaging and IFU will explicitly state Rx-only.
- **Consumer retail channels.** Vitalisens will not be sold in pharmacies, big-box retail, or DTC consumer e-commerce.
- **Consumer-direct marketing claims.** Marketing addresses clinicians (and patients via clinician referral), not general consumers.
- **OTC clearance pursuit.** No regulatory effort is allocated to an OTC pathway.

### Decision 003: 7-Day Pad Wear Time [decision-003-7-day-wear-not-14-day]

- **A 14-day Vitalisens Pad variant in v1.** No engineering work toward 14-day adhesion validation.
- **Labeling that implies extended wear.** IFU language will be explicit about the 7-day window.
- **Off-label "you can keep it on longer" marketing.** No language that encourages extended wear.



## 11. Sources

A bibliography of every source node in this vault, labeled by `source_kind`. Citations elsewhere in this document point at the node ids listed here.

| Source | Kind | Title |
|---|---|---|
| [source-citation-aha-mct-guidelines-2024] | citation | Citation: AHA MCT Clinical Guidelines (fictional 2024 edition) |
| [source-customer-interview-2026-04-12-nurse-anderson] | customer-interview | Customer Interview: Nurse Anderson (Northstar Cardiology, 2026-04-12) |
| [source-domain-expertise-saunders-cardiology-2026] | domain-expertise | Domain Expertise: Saunders, 20 Years of Cardiology Workflow |
| [source-fda-510k-summary-K231234-cardiotrace] | fda-510k-summary | FDA 510(k) Summary: K231234 (CardioTrace Pro v2) |
| [source-internal-data-q1-2026-pad-attach-rate] | internal-data | Internal Data: Q1 2026 Pad Attach Rate Cohort |
| [source-market-data-cardiac-monitor-tam-2025] | market-data | Market Data: US Ambulatory Cardiac Monitor TAM (fictional 2025 report) |
| [source-press-release-cardiotrace-2025-q3-launch] | press-release | Press Release: CardioTrace Announces Pro Expanded Clearance (2025 Q3) |
| [source-strategic-thesis-disposable-pad-recurring-revenue] | strategic-thesis | Strategic Thesis: Disposable Pad as Recurring Revenue Engine |
| [source-vision-saunders-2026-cardiac-workflow-thesis] | founder-vision | Founder Vision: The Cardiac Workflow Bottleneck (Saunders, 2026) |
| [source-web-snapshot-cardiotrace-product-page-2026-05-20] | web-snapshot | Web Snapshot: CardioTrace Pro Product Page (2026-05-20) |

---

> This is a planning artifact. It is not a controlled document and is not part of any design history file, risk management file, or traceability matrix per ISO 14971, IEC 62304, or 21 CFR 820.

_company-brain v0.4.0 · MRD generated 2026-05-25 from vault at `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/meddev-fictional`._
