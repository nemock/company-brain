---
id: decision-003-workspace-pricing-not-seat-based
title: "Decision 003: Workspace-Based Pricing, Not Per-Seat"
type: decision
namespace: pricing
summary: "Loftwing prices per workspace (per company), not per developer seat. Three workspace tiers; no per-seat scaling."
auto_inject: false
applicable_when: null
confidence: 0.88
verified_at: 2026-02-10
verified_by: nemock
staleness_signal: "Revisit if churn data shows workspace-tier-cap discomfort (e.g., teams hovering at 90% of the next tier and downgrading rather than upgrading)."
tags: [decision, pricing]
edges:
  - target: pillar-team-level-signal
    type: supports
    weight: 0.85
    note: "Pricing by team-equivalent unit (workspace) aligns with how we measure."
  - target: source-customer-interview-2026-03-vpe-northgate
    type: derived_from
    weight: 0.75
    note: "Northgate VPE explicitly called per-seat 'a non-starter.'"
  - target: source-web-snapshot-flightpath-pricing-2026-04-15
    type: contradicts
    weight: 0.7
    note: "FlightPath prices per seat — we are deliberately going the other way."
related: []
source_url: null
controlled_document: false
---

# Decision 003: Workspace-Based Pricing, Not Per-Seat

## Summary

Workspace-based tiers. Not per-seat. Not per-developer.

## Alternatives Considered

1. **Per-seat ($X per developer per month).** Rejected — Northgate and three other interviewees explicitly named this as a non-starter for their decision process.
2. **Per-active-developer (only bill for developers who logged into Loftwing).** Rejected — discourages adoption; we want the dashboard widely viewable.
3. **Per-workspace tiered ($X/month for up to N developers tracked).** Chosen.

## Decision

Three workspace tiers:

- **Starter** — $99/month, up to 25 developers tracked, GitHub-only integration.
- **Team** — $299/month, up to 100 developers tracked, all three integrations.
- **Scale** — $899/month, up to 250 developers tracked, all three integrations + Slack digest + custom dashboards.

Nothing above Scale in v1.

## Rationale

- Aligns with our team-level-signal pillar (pricing by team-equivalent unit, not by individual).
- Matches the budget that our ICP can authorize without procurement (under $1k/mo per the Northgate interview).
- Three tiers is enough; more creates analysis paralysis.

## What This Rules Out

- **Per-seat pricing.** Not in v1 or v2.
- **Per-active-user pricing.** Not in v1 or v2.
- **Unlimited-developer tier.** No tier above 250 developers in v1; that is the natural top of our ICP band.
- **Custom-priced enterprise contracts.** Customers above 250 developers are out of ICP. We say no.

## Edges

`supports` the team-level pillar. `derived_from` the Northgate interview. `contradicts` FlightPath's per-seat model — deliberate differentiation, not a mistake.
