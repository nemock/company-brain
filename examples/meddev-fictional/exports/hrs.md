# Hardware Requirements Specification (HRS)

> Vault: `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/meddev-fictional` · Profile: `medical-device`

> _v0.4.0 scaffold — full implementation pending in v1.x. Adopters: fill in the placeholders below and re-run `cb render`._

## 1. Scope

_[Adopters: 1–2 paragraphs. What hardware does this specify?]_

## 2. Hardware architecture overview

_[Adopters: 2–3 paragraphs describing major modules, mechanical, electrical, and integration boundaries.]_

## 3. Functional requirements (hardware class)

_No hardware-class requirements captured. Run `intake` and add requirement nodes with `requirement_class: hardware`._

## 4. Performance / environmental / mechanical requirements

_[Adopters: temperature range, humidity, ingress protection, drop, vibration, EMC, battery life, weight, thermal.]_

## 5. External interfaces

_[Adopters: physical connectors, mounting interfaces, host-system attachment, packaging.]_

## 6. Features in scope

- [feature-continuous-ecg-recording] **Feature: Continuous Dual-Channel ECG Recording** — Vitalisens Cardio continuously records dual-channel ECG throughout the monitoring window, with motion artifact rejection via accelerometer.
- [feature-pad-quick-replace] **Feature: Pad Quick-Replace** — Snap-fit pad interface with orientation cues and electronic step-by-step instructions; supports self-service replacement in under 5 minutes.


## 8. Hardware-specific risks

- [risk-insight-pad-adhesion-failure-affects-data-quality] **Risk Insight: Pad Adhesion Failure Cascades into Data-Quality Failure** — Pad adhesion failure does not just lose signal — it tends to fail silently, producing noisy data that looks plausible. Detection matters as much as prevention.

## Traceability

_[Adopters: trace each hardware requirement back to a system requirement and forward to a verification activity.]_

---

> This is a planning artifact. It is not a controlled document and is not part of any design history file, risk management file, or traceability matrix per ISO 14971, IEC 62304, or 21 CFR 820.

_company-brain v0.5.0 · hrs scaffold generated 2026-05-25 from vault at `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/meddev-fictional`._
