# System Requirements Document (SRD)

> Vault: `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/saas-fictional` · Profile: `default`

> _v0.4.0 scaffold — full implementation pending in v1.x. Adopters: fill in the placeholders below and re-run `cb render`._

## 1. Scope

_[Adopters: 1–2 paragraphs. What system does this document specify? What is in / out of scope?]_

## 2. System overview

_[Adopters: 2–3 paragraph overview. Reference the products and features below.]_

## 3. Functional requirements (system class)

- [requirement-sys-001-three-source-aggregation] **System Requirement: Three-Source Aggregation** — The system shall ingest and reconcile event streams from GitHub plus at least one of Linear or Jira, computing team-level rollups within 60 seconds of source-side changes.

## 4. Non-functional requirements

_[Adopters: performance, reliability, maintainability, scalability. v0.4.0 scaffold doesn't auto-extract these.]_

## 5. Interfaces

_[Adopters: external interfaces, integration points.]_

## 6. Constraints

_[Adopters: regulatory, environmental, technical constraints.]_

## 7. Features in scope

- [feature-team-cycle-time-dashboard] **Feature: Team-Level Cycle Time Dashboard** — The flagship dashboard view: per-team cycle time over time, plus a 4-week trailing average and a comparison to the team's own historical baseline.
- [feature-weekly-slack-digest] **Feature: Weekly Slack Digest** — An opt-in weekly Slack digest summarising each team's cycle time, deploy frequency, and notable changes. Posted to a configured channel.

## 8. Use cases

- [use-case-quarterly-board-prep] **Use Case: Quarterly Board Prep** — VPE assembles engineering velocity story for the board with Loftwing as the data source; target time under 1 hour, down from the typical 4–6.


## Traceability

_[Adopters: trace each system requirement back to the user or market requirement it serves.]_

---

_company-brain v0.4.0 · srd scaffold generated 2026-05-25 from vault at `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/saas-fictional`._
