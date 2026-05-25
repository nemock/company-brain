# Lessons Learned

> Vault: `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/saas-fictional` · Profile: `default`

> _v0.4.0 scaffold — full implementation pending in v1.x. Adopters: fill in the placeholders below and re-run `cb render`._

## What worked

_[Adopters: 3–5 bullets on what worked, citing patterns and hypotheses confirmed.]_

Patterns observed:
- [pattern-engaged-vpes-share-dashboard-url-early] **Pattern: Engaged VPEs Share the Dashboard URL Early** — Across the Q1 2026 customer interviews, every VPE who retained had shared the Loftwing dashboard URL in their team's Slack within the first week.

## What didn't

_[Adopters: 3–5 bullets on what didn't work, citing hypotheses falsified or decisions revisited.]_

Hypotheses on file:
- [hypothesis-dashboard-url-shared-in-slack-predicts-retention] **Hypothesis: Dashboard URL Shared in Slack Within 7 Days Predicts 90-Day Retention** — Teams whose VPE shares the Loftwing dashboard URL in their team's Slack within the first 7 days will retain at 90 days at materially higher rates.
- [hypothesis-self-serve-under-10-min-converts-25pct] **Hypothesis: Self-Serve Under 10 Minutes Converts at 25%+** — If a new user can sign up, connect an integration, and see a dashboard in under 10 minutes, trial-to-paid conversion will sustain at 25% or higher.

## What we'd do differently

_[Adopters: changes for the next project.]_

## Reusable decisions

Decisions whose rationale travels well beyond this project:
- [decision-001-plg-first-not-enterprise] **Decision 001: PLG-First, Not Enterprise Sales** — Loftwing's GTM motion is product-led growth (self-serve signup, in-product activation, in-product upgrade) — not enterprise sales with demos and procurement cycles.
- [decision-002-three-integrations-only-in-v1] **Decision 002: Three Integrations Only in v1 (GitHub, Linear, Jira)** — Loftwing v1 ships with exactly three integrations: GitHub, Linear, and Jira. No GitLab, Bitbucket, Azure DevOps, or other issue trackers until v2.
- [decision-003-workspace-pricing-not-seat-based] **Decision 003: Workspace-Based Pricing, Not Per-Seat** — Loftwing prices per workspace (per company), not per developer seat. Three workspace tiers; no per-seat scaling.

## Open questions that surfaced

- [question-add-team-health-sentiment-input] Question: Add a Team-Health Sentiment Input?
- [question-when-to-add-gitlab-support] Question: When to Add GitLab Support?

---

_company-brain v0.4.0 · lessons-learned scaffold generated 2026-05-25 from vault at `/Volumes/Casima/claudeCode/CompanyWiki/company-brain/examples/saas-fictional`._
