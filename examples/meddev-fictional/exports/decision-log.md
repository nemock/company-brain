# Decision Log

> Vault: `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/meddev-fictional` · Profile: `medical-device`

> _v0.4.0 scaffold — full implementation pending in v1.x. Adopters: fill in the placeholders below and re-run `cb render`._

## Active decisions

### Decision 001: Online-Only Documentation [decision-001-online-only-documentation]

**Namespace:** `operations` · **Confidence:** 0.92 · **Verified:** 2026-05-21

All Vitalisens documentation (IFU, user manual, quick-start, clinician guide) is electronic only. No printed inserts ship with any product.

**Rules out:**

- **Printed IFU inserts.** The IFU is not printed at any point in the supply chain.
- **Printed quick-start cards.** No "getting started" cards ship in the box.
- **Printed user manuals.** No paper manuals are distributed.
- **Distributor-printed collateral.** Distributors are contractually prohibited from generating their own printed versions of the IFU or user manual.
- **PDF-by-email as the documentation distribution channel.** Documentation must live at a stable URL, not be emailed.

### Decision 002: Prescription-Only, Not Over-the-Counter [decision-002-prescription-only-not-otc]

**Namespace:** `regulatory` · **Confidence:** 0.95 · **Verified:** 2026-05-21

Vitalisens will be sold by prescription only (Rx). We will not pursue over-the-counter (OTC) labeling, packaging, or distribution in v1 or v2.

**Rules out:**

- **OTC labeling.** Packaging and IFU will explicitly state Rx-only.
- **Consumer retail channels.** Vitalisens will not be sold in pharmacies, big-box retail, or DTC consumer e-commerce.
- **Consumer-direct marketing claims.** Marketing addresses clinicians (and patients via clinician referral), not general consumers.
- **OTC clearance pursuit.** No regulatory effort is allocated to an OTC pathway.

### Decision 003: 7-Day Pad Wear Time [decision-003-7-day-wear-not-14-day]

**Namespace:** `product-design` · **Confidence:** 0.88 · **Verified:** 2026-05-21

Vitalisens Pad is rated for 7 days of continuous wear. We will not pursue a 14-day variant in v1.

**Rules out:**

- **A 14-day Vitalisens Pad variant in v1.** No engineering work toward 14-day adhesion validation.
- **Labeling that implies extended wear.** IFU language will be explicit about the 7-day window.
- **Off-label "you can keep it on longer" marketing.** No language that encourages extended wear.



## Non-goal pillars (durable boundaries)

- [pillar-no-pediatric-use] **Non-Goal: We Do Not Pursue Pediatric Use** — Vitalisens will not pursue indications, labeling, marketing, or clinical claims for pediatric patients (under 18) in v1 or v2 of the product.
- [pillar-no-physical-documentation] **Non-Goal: No Physical Documentation** — Vitalisens does not produce printed IFU, printed quick-start cards, printed user manuals, or printed in-box collateral. All documentation is online.

---

> This is a planning artifact. It is not a controlled document and is not part of any design history file, risk management file, or traceability matrix per ISO 14971, IEC 62304, or 21 CFR 820.

_company-brain v0.5.0 · decision-log scaffold generated 2026-05-25 from vault at `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/meddev-fictional`._
