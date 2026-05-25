# Risk Register (planning)

> Vault: `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/meddev-fictional` · Profile: `medical-device`

> _v0.4.0 scaffold — full implementation pending in v1.x. Adopters: fill in the placeholders below and re-run `cb render`._

> **This is a planning register, not a controlled risk management file per ISO 14971.**
> The controlled file is a separate artifact created under your QMS.

## Hazards under consideration

- [hazard-skin-irritation-from-adhesive] **Hazard: Skin Irritation from Pad Adhesive** — Adhesive material on the Vitalisens Pad can cause skin irritation, allergic response, or contact dermatitis in some patients.

## Hazardous situations

- [hazardous-situation-pad-falls-off-during-sleep] **Hazardous Situation: Pad Detaches During Sleep, Patient Unaware** — Pad detaches partially or fully while the patient sleeps; the patient is unaware until morning; data is missing or degraded for that window.

## Potential harms

- [harm-missed-arrhythmia-event] **Harm: Missed Arrhythmia Event** — Clinically significant arrhythmia occurs during a window when the device is failing to capture usable data; the event is not detected and the clinician cannot act.

## Candidate risk-control ideas

- [risk-control-idea-disconnection-alarm-via-app] **Risk Control Idea: Disconnection Alarm via Clinician App** — Use impedance monitoring + signal-quality assessment to detect pad detachment in real-time; surface an alert to the clinician app and a daily check-in to the patient.

## Risk insights

- [risk-insight-pad-adhesion-failure-affects-data-quality] **Risk Insight: Pad Adhesion Failure Cascades into Data-Quality Failure** — Pad adhesion failure does not just lose signal — it tends to fail silently, producing noisy data that looks plausible. Detection matters as much as prevention.

---

> This is a planning artifact. It is not a controlled document and is not part of any design history file, risk management file, or traceability matrix per ISO 14971, IEC 62304, or 21 CFR 820.

_company-brain v0.5.0 · risk-register scaffold generated 2026-05-25 from vault at `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/meddev-fictional`._
