---
id: decision-001-plg-first-not-enterprise
title: "Decision 001: PLG-First, Not Enterprise Sales"
type: decision
namespace: gtm
summary: "Loftwing's GTM motion is product-led growth (self-serve signup, in-product activation, in-product upgrade) — not enterprise sales with demos and procurement cycles."
auto_inject: false
applicable_when: null
confidence: 0.9
verified_at: 2026-01-22
verified_by: nemock
staleness_signal: "Revisit if we have a credible enterprise pipeline (e.g., five inbound enterprise deals quarter-over-quarter) that the team cannot service through the self-serve motion."
tags: [decision, gtm, plg]
edges:
  - target: pillar-self-serve-over-enterprise-sales
    type: supports
    weight: 0.95
    note: "This decision is the operational expression of the pillar."
  - target: source-customer-interview-2026-03-vpe-northgate
    type: derived_from
    weight: 0.7
    note: "Northgate's stated preference for self-serve crystallised the call."
related: []
source_url: null
controlled_document: false
---

# Decision 001: PLG-First, Not Enterprise Sales

## Summary

PLG, not enterprise sales, in v1 and the foreseeable v2.

## Alternatives Considered

1. **Enterprise-sales-first.** Build a sales team, target Fortune 500 eng orgs, sell six-figure annual contracts. Rejected — wrong fit for our ICP and our cash position; ICP doesn't want to be sold to.
2. **Hybrid (PLG for under 100 devs, sales for above 100).** Rejected — fragments the team's focus; PLG and sales are different operational rhythms.
3. **PLG-first, sales-assisted only when invited.** Chosen.

## Decision

Loftwing is PLG-first. Signup → integration → dashboard → upgrade is fully self-serve. We do not employ AEs or BDRs in v1. We accept inbound conversations from interested companies, but the default motion is self-serve.

## Rationale

- Our ICP (VPE at scaling B2B SaaS) does not want a sales cycle for a tool decision in this band.
- Self-serve is the only motion compatible with a small founding team.
- The team-level-metrics pillar is the kind of thing customers adopt because the dashboard is good, not because a sales rep convinced them.

## What This Rules Out

- **Hiring AEs / BDRs in v1.** No outbound sales motion. No SDR org.
- **Forced demos before signup.** Trial signup is one click away from the homepage.
- **Six-figure annual contracts.** Pricing tops out below the procurement-required threshold (see [decision-003](decision-003-workspace-pricing-not-seat-based.md)).
- **Custom enterprise contract language.** We sign self-serve SaaS terms only in v1.

## Edges

`supports` the self-serve pillar. `derived_from` the Northgate interview's pivotal statement.
