# System Requirements Document (SRD)

> Vault: `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/meddev-fictional` · Profile: `medical-device`

> _v0.4.0 scaffold — full implementation pending in v1.x. Adopters: fill in the placeholders below and re-run `cb render`._

## 1. Scope

_[Adopters: 1–2 paragraphs. What system does this document specify? What is in / out of scope?]_

## 2. System overview

_[Adopters: 2–3 paragraph overview. Reference the products and features below.]_

## 3. Functional requirements (system class)

- [requirement-sys-001-7-day-battery] **System Requirement: 7-Day Continuous Battery Life** — Vitalisens Cardio must operate for at least 7 days of continuous use between recharges under nominal conditions.

## 4. Non-functional requirements

_[Adopters: performance, reliability, maintainability, scalability. v0.4.0 scaffold doesn't auto-extract these.]_

## 5. Interfaces

_[Adopters: external interfaces, integration points.]_

## 6. Constraints

_[Adopters: regulatory, environmental, technical constraints.]_

## 7. Features in scope

- [feature-continuous-ecg-recording] **Feature: Continuous Dual-Channel ECG Recording** — Vitalisens Cardio continuously records dual-channel ECG throughout the monitoring window, with motion artifact rejection via accelerometer.
- [feature-pad-quick-replace] **Feature: Pad Quick-Replace** — Snap-fit pad interface with orientation cues and electronic step-by-step instructions; supports self-service replacement in under 5 minutes.


## 9. System-level risks

- [risk-insight-pad-adhesion-failure-affects-data-quality] **Risk Insight: Pad Adhesion Failure Cascades into Data-Quality Failure** — Pad adhesion failure does not just lose signal — it tends to fail silently, producing noisy data that looks plausible. Detection matters as much as prevention.

## Traceability

_[Adopters: trace each system requirement back to the user or market requirement it serves.]_

---

> This is a planning artifact. It is not a controlled document and is not part of any design history file, risk management file, or traceability matrix per ISO 14971, IEC 62304, or 21 CFR 820.

_company-brain v0.8.0 · srd scaffold generated 2026-05-27 from vault at `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/meddev-fictional`._
