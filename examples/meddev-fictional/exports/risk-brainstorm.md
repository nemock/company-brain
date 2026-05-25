# Risk Brainstorm

> Vault: `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/meddev-fictional` · Profile: `medical-device`

> _v0.4.0 scaffold — full implementation pending in v1.x. Adopters: fill in the placeholders below and re-run `cb render`._

> **This is a planning artifact, not a controlled risk management file per ISO 14971.**
> Promote anything durable from here into the controlled risk file under your QMS.

## Open hazards under consideration

- [hazard-skin-irritation-from-adhesive] **Hazard: Skin Irritation from Pad Adhesive** — Adhesive material on the Vitalisens Pad can cause skin irritation, allergic response, or contact dermatitis in some patients.

## Hazardous situations

- [hazardous-situation-pad-falls-off-during-sleep] **Hazardous Situation: Pad Detaches During Sleep, Patient Unaware** — Pad detaches partially or fully while the patient sleeps; the patient is unaware until morning; data is missing or degraded for that window.

## Potential harms

- [harm-missed-arrhythmia-event] **Harm: Missed Arrhythmia Event** — Clinically significant arrhythmia occurs during a window when the device is failing to capture usable data; the event is not detected and the clinician cannot act.

## Candidate mitigations / risk-control ideas

- [risk-control-idea-disconnection-alarm-via-app] **Risk Control Idea: Disconnection Alarm via Clinician App** — Use impedance monitoring + signal-quality assessment to detect pad detachment in real-time; surface an alert to the clinician app and a daily check-in to the patient.

## Risk insights

- [risk-insight-pad-adhesion-failure-affects-data-quality] **Risk Insight: Pad Adhesion Failure Cascades into Data-Quality Failure** — Pad adhesion failure does not just lose signal — it tends to fail silently, producing noisy data that looks plausible. Detection matters as much as prevention.

## Related decisions

- [decision-001-online-only-documentation] **Decision 001: Online-Only Documentation** — All Vitalisens documentation (IFU, user manual, quick-start, clinician guide) is electronic only. No printed inserts ship with any product.
- [decision-002-prescription-only-not-otc] **Decision 002: Prescription-Only, Not Over-the-Counter** — Vitalisens will be sold by prescription only (Rx). We will not pursue over-the-counter (OTC) labeling, packaging, or distribution in v1 or v2.
- [decision-003-7-day-wear-not-14-day] **Decision 003: 7-Day Pad Wear Time** — Vitalisens Pad is rated for 7 days of continuous wear. We will not pursue a 14-day variant in v1.

## Related pillars

- [pillar-disposable-pad-business-model] **Disposable Pad as the Recurring-Revenue Engine** — The Vitalisens Pad is a 7-day replaceable disposable; recurring pad revenue, not the wearable, is the long-term unit economic.
- [pillar-icp-ambulatory-cardiac-patients] **ICP: Adult Ambulatory Cardiac Patients** — We serve adult cardiac patients in ambulatory settings during the 7- to 30-day window after a cardiac event or during arrhythmia workup.
- [pillar-no-pediatric-use] **Non-Goal: We Do Not Pursue Pediatric Use** — Vitalisens will not pursue indications, labeling, marketing, or clinical claims for pediatric patients (under 18) in v1 or v2 of the product.
- [pillar-no-physical-documentation] **Non-Goal: No Physical Documentation** — Vitalisens does not produce printed IFU, printed quick-start cards, printed user manuals, or printed in-box collateral. All documentation is online.

## Residual-risk questions

_[Adopters: list the open questions about risk that are not yet resolved. Promote durable ones to `question` nodes._]

---

> This is a planning artifact. It is not a controlled document and is not part of any design history file, risk management file, or traceability matrix per ISO 14971, IEC 62304, or 21 CFR 820.

_company-brain v0.4.0 · risk-brainstorm scaffold generated 2026-05-25 from vault at `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/meddev-fictional`._
