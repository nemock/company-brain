# Decision Log

> Vault: `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/saas-fictional` · Profile: `default`

> _v0.4.0 scaffold — full implementation pending in v1.x. Adopters: fill in the placeholders below and re-run `cb render`._

## Active decisions

### Decision 001: PLG-First, Not Enterprise Sales [decision-001-plg-first-not-enterprise]

**Namespace:** `gtm` · **Confidence:** 0.9 · **Verified:** 2026-01-22

Loftwing's GTM motion is product-led growth (self-serve signup, in-product activation, in-product upgrade) — not enterprise sales with demos and procurement cycles.

**Rules out:**

- **Hiring AEs / BDRs in v1.** No outbound sales motion. No SDR org.
- **Forced demos before signup.** Trial signup is one click away from the homepage.
- **Six-figure annual contracts.** Pricing tops out below the procurement-required threshold (see [decision-003](decision-003-workspace-pricing-not-seat-based.md)).
- **Custom enterprise contract language.** We sign self-serve SaaS terms only in v1.

### Decision 002: Three Integrations Only in v1 (GitHub, Linear, Jira) [decision-002-three-integrations-only-in-v1]

**Namespace:** `product` · **Confidence:** 0.85 · **Verified:** 2026-02-04

Loftwing v1 ships with exactly three integrations: GitHub, Linear, and Jira. No GitLab, Bitbucket, Azure DevOps, or other issue trackers until v2.

**Rules out:**

- **GitLab support in v1.** GitLab users see a "coming in v2" message at signup.
- **Bitbucket support in v1.** Same.
- **Azure DevOps support in v1.** Same.
- **Pivotal Tracker, Asana, Shortcut, ClickUp.** Not in v1.
- **Generic webhook intake.** Not in v1.
- **Customer-built integrations against our API.** API doesn't ship to customers in v1.

### Decision 003: Workspace-Based Pricing, Not Per-Seat [decision-003-workspace-pricing-not-seat-based]

**Namespace:** `pricing` · **Confidence:** 0.88 · **Verified:** 2026-02-10

Loftwing prices per workspace (per company), not per developer seat. Three workspace tiers; no per-seat scaling.

**Rules out:**

- **Per-seat pricing.** Not in v1 or v2.
- **Per-active-user pricing.** Not in v1 or v2.
- **Unlimited-developer tier.** No tier above 250 developers in v1; that is the natural top of our ICP band.
- **Custom-priced enterprise contracts.** Customers above 250 developers are out of ICP. We say no.



## Non-goal pillars (durable boundaries)

- [pillar-no-consumer-market] **Non-Goal: No Consumer Market** — Loftwing is and remains a B2B SaaS product sold to companies. We do not sell to individual developers, indie hackers, or consumers.
- [pillar-no-developer-surveillance] **Non-Goal: No Developer Surveillance** — Loftwing will never ship features that score, rank, or surveil individual contributors. The smallest unit of analysis we expose is the team.

---

_company-brain v0.4.0 · decision-log scaffold generated 2026-05-25 from vault at `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/saas-fictional`._
