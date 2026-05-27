# Marketing Requirements Document

> Vault: `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/saas-fictional` · Profile: `default`

## 1. Executive summary

The 3 governing principles of this company shape every section that follows. The product set is anchored on 1 product, positioned against 2 known competitors.

**Top principles:**
- [pillar-icp-vpe-scaling-saas] **ICP: VPE at Scaling B2B SaaS (50–250 Engineers)** — Loftwing serves VPs of Engineering and CTOs at B2B SaaS companies between Series A and Series C (roughly 50–250 engineers).
- [pillar-self-serve-over-enterprise-sales] **Self-Serve Setup Over Enterprise Sales Motion** — A new user must be able to connect Loftwing to their stack and see the first dashboard in under 10 minutes, without talking to sales.
- [pillar-team-level-signal] **Team-Level Signal Over Individual-Contributor Metrics** — Every Loftwing metric and dashboard view is scoped to the team or higher; we do not surface or score individual contributors.

**What we are explicitly not doing** (full detail in §10):
- [pillar-no-consumer-market] Non-Goal: No Consumer Market
- [pillar-no-developer-surveillance] Non-Goal: No Developer Surveillance

## 2. Vision and positioning

The company's positioning rests on the following pillars:

### ICP: VPE at Scaling B2B SaaS (50–250 Engineers) [pillar-icp-vpe-scaling-saas]

Loftwing serves VPs of Engineering and CTOs at B2B SaaS companies between Series A and Series C (roughly 50–250 engineers).

_Applies when:_ ICP, target market, audience, who we serve, segment, persona, vertical, customer profile, deal size, sales motion

### Self-Serve Setup Over Enterprise Sales Motion [pillar-self-serve-over-enterprise-sales]

A new user must be able to connect Loftwing to their stack and see the first dashboard in under 10 minutes, without talking to sales.

_Applies when:_ pricing, sales motion, onboarding, signup, setup, time-to-value, GTM, PLG, self-serve, enterprise, demo, contact-sales

### Team-Level Signal Over Individual-Contributor Metrics [pillar-team-level-signal]

Every Loftwing metric and dashboard view is scoped to the team or higher; we do not surface or score individual contributors.

_Applies when:_ metrics, dashboards, surveillance, IC, individual, developer, ranking, scoring, performance, productivity, monitoring, observability of people


**Vision sources** (founder-vision, strategic-thesis, domain-expertise):

- [source-domain-expertise-12-years-eng-management] _domain-expertise_ — Domain Expertise: 12 Years of Engineering Management (Founder)
- [source-strategic-thesis-team-level-metrics] _strategic-thesis_ — Strategic Thesis: Team-Level Metrics Over Individual-Contributor Metrics
- [source-vision-loftwing-2026] _founder-vision_ — Founder Vision: Engineering Velocity is a Board-Level Conversation (Loftwing, 2026)

## 3. Market and personas

**Personas:**

- [persona-vpe-scaling-saas] **Persona: VPE at Scaling B2B SaaS** — VP of Engineering at a 50–250-engineer B2B SaaS company. Owns engineering velocity outcomes; answers to a non-technical board quarterly.


**Named customer references:**

- [customer-northgate-2026] Northgate (fictional Series-B SaaS, ~80 engineers) — First named customer reference; series-B B2B SaaS at ~80 engineers; on a Team plan; VPE was interviewed 2026-03-11.

## 4. Market requirements

- [requirement-mkt-001-board-legible-velocity-story] **Market Requirement: Board-Legible Engineering Velocity Story** — The product must let a VPE assemble a one-screen engineering-velocity story that a non-technical board reviewer can read in under 2 minutes.

## 5. Competitive landscape

### FlightPath [competitor-flightpath-eng]

Direct fictional competitor in engineering analytics; per-seat pricing, recently raised a Series B and moving up-market.

- **Canonical URL:** https://flightpath-eng.example.com

### Tetherline Analytics [competitor-tetherline-analytics]

Adjacent fictional competitor; positioned for the Fortune 500 enterprise engineering analytics market with a $200k+ annual minimum contract.

- **Canonical URL:** https://tetherline.example.com


## 6. Evidence vs. vision split

A breakdown of which claims in this vault are grounded in evidence (customer interviews, market data, internal telemetry, FDA filings, web snapshots, press releases) and which are vision-driven (founder vision, strategic thesis, domain expertise). Both are legitimate; conflating them silently is the failure mode this section prevents.

- **Evidence-derived claims:** 6
- **Vision-derived claims:** 4
- **Uncited claims:** 8 _(should be addressed — every load-bearing claim should derive from a source)_

**Uncited claims to address:**
- [fact-team-size-2026-q2] Fact: Loftwing Team Size — 2026 Q2
- [fact-weekly-active-teams-2026-w14] Fact: Weekly Active Teams — 2026 Week 14
- [hypothesis-dashboard-url-shared-in-slack-predicts-retention] Hypothesis: Dashboard URL Shared in Slack Within 7 Days Predicts 90-Day Retention
- [hypothesis-self-serve-under-10-min-converts-25pct] Hypothesis: Self-Serve Under 10 Minutes Converts at 25%+
- [requirement-mkt-001-board-legible-velocity-story] Market Requirement: Board-Legible Engineering Velocity Story
- [requirement-sw-001-oauth-for-integrations] Software Requirement: OAuth for All Third-Party Integrations
- [requirement-sys-001-three-source-aggregation] System Requirement: Three-Source Aggregation
- [requirement-user-001-self-serve-integration-setup] User Requirement: Self-Serve Integration Setup

## 7. Open questions

- [question-add-team-health-sentiment-input] **Question: Add a Team-Health Sentiment Input?** — Should Loftwing accept a weekly team-health sentiment input (e.g., a single-emoji pulse from each team's lead) and surface it alongside the velocity metrics?
- [question-when-to-add-gitlab-support] **Question: When to Add GitLab Support?** — Under what conditions should Loftwing add GitLab support, given v1 ships GitHub-only per decision-002?

## 8. What we are explicitly not doing


**Non-goal pillars** (durable boundaries):

### Non-Goal: No Consumer Market [pillar-no-consumer-market]

Loftwing is and remains a B2B SaaS product sold to companies. We do not sell to individual developers, indie hackers, or consumers.

_Applies when:_ consumer, B2C, individual developer, indie, freelancer, hobbyist, personal use, side project, retail, app store

### Non-Goal: No Developer Surveillance [pillar-no-developer-surveillance]

Loftwing will never ship features that score, rank, or surveil individual contributors. The smallest unit of analysis we expose is the team.

_Applies when:_ individual, IC, surveillance, scoring, ranking, developer monitoring, productivity score, performance review, leaderboard, contribution metrics, code metrics per person


**Decisions and what they rule out:**

### Decision 001: PLG-First, Not Enterprise Sales [decision-001-plg-first-not-enterprise]

- **Hiring AEs / BDRs in v1.** No outbound sales motion. No SDR org.
- **Forced demos before signup.** Trial signup is one click away from the homepage.
- **Six-figure annual contracts.** Pricing tops out below the procurement-required threshold (see [decision-003](decision-003-workspace-pricing-not-seat-based.md)).
- **Custom enterprise contract language.** We sign self-serve SaaS terms only in v1.

### Decision 002: Three Integrations Only in v1 (GitHub, Linear, Jira) [decision-002-three-integrations-only-in-v1]

- **GitLab support in v1.** GitLab users see a "coming in v2" message at signup.
- **Bitbucket support in v1.** Same.
- **Azure DevOps support in v1.** Same.
- **Pivotal Tracker, Asana, Shortcut, ClickUp.** Not in v1.
- **Generic webhook intake.** Not in v1.
- **Customer-built integrations against our API.** API doesn't ship to customers in v1.

### Decision 003: Workspace-Based Pricing, Not Per-Seat [decision-003-workspace-pricing-not-seat-based]

- **Per-seat pricing.** Not in v1 or v2.
- **Per-active-user pricing.** Not in v1 or v2.
- **Unlimited-developer tier.** No tier above 250 developers in v1; that is the natural top of our ICP band.
- **Custom-priced enterprise contracts.** Customers above 250 developers are out of ICP. We say no.



## 9. Sources

A bibliography of every source node in this vault, labeled by `source_kind`. Citations elsewhere in this document point at the node ids listed here.

| Source | Kind | Title |
|---|---|---|
| [source-citation-accelerate-book] | citation | Citation: Accelerate (Forsgren, Humble, Kim) |
| [source-customer-interview-2026-03-vpe-northgate] | customer-interview | Customer Interview: VPE at Northgate (2026-03-11) |
| [source-domain-expertise-12-years-eng-management] | domain-expertise | Domain Expertise: 12 Years of Engineering Management (Founder) |
| [source-internal-data-q1-2026-trial-cohort] | internal-data | Internal Data: Q1 2026 Trial Cohort |
| [source-market-data-dora-2025] | market-data | Market Data: Accelerate State of DevOps Report 2025 (fictional) |
| [source-press-release-flightpath-2026-q1-series-b] | press-release | Press Release: FlightPath Closes $40M Series B (2026-Q1) |
| [source-strategic-thesis-team-level-metrics] | strategic-thesis | Strategic Thesis: Team-Level Metrics Over Individual-Contributor Metrics |
| [source-vision-loftwing-2026] | founder-vision | Founder Vision: Engineering Velocity is a Board-Level Conversation (Loftwing, 2026) |
| [source-web-snapshot-flightpath-pricing-2026-04-15] | web-snapshot | Web Snapshot: FlightPath Pricing Page (2026-04-15) |

---

_company-brain v0.8.0 · MRD generated 2026-05-27 from vault at `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/saas-fictional`._
