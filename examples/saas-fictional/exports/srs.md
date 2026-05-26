# Software Requirements Specification (SRS)

> Vault: `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/saas-fictional` · Profile: `default`

> _v0.4.0 scaffold — full implementation pending in v1.x. Adopters: fill in the placeholders below and re-run `cb render`._

## 1. Scope

_[Adopters: 1–2 paragraphs. What software does this specify?]_

## 2. Software architecture overview

_[Adopters: 2–3 paragraphs describing major components and their interactions.]_

## 3. Functional requirements (software class)

- [requirement-sw-001-oauth-for-integrations] **Software Requirement: OAuth for All Third-Party Integrations** — The software shall use OAuth 2.0 for all third-party integrations (GitHub, Linear, Jira). Personal access tokens are not supported in v1.

## 4. Non-functional requirements

_[Adopters: performance, security, observability, accessibility, internationalization, supportability.]_

## 5. External interfaces

_[Adopters: APIs consumed, APIs produced, file formats, protocols.]_

## 6. Features in scope

- [feature-team-cycle-time-dashboard] **Feature: Team-Level Cycle Time Dashboard** — The flagship dashboard view: per-team cycle time over time, plus a 4-week trailing average and a comparison to the team's own historical baseline.
- [feature-weekly-slack-digest] **Feature: Weekly Slack Digest** — An opt-in weekly Slack digest summarising each team's cycle time, deploy frequency, and notable changes. Posted to a configured channel.

## 7. Use cases

- [use-case-quarterly-board-prep] **Use Case: Quarterly Board Prep** — VPE assembles engineering velocity story for the board with Loftwing as the data source; target time under 1 hour, down from the typical 4–6.

## 8. Software-specific risks

_No risk-insight nodes captured. Run `intake risk` (medical-device profile)._

## Traceability

_[Adopters: trace each software requirement back to a system requirement and forward to a test case.]_

---

_company-brain v0.6.0 · srs scaffold generated 2026-05-25 from vault at `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/saas-fictional`._
