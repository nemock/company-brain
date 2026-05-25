---
id: competitor-flightpath-eng
title: "FlightPath"
type: competitor
namespace: competitive
summary: "Direct fictional competitor in engineering analytics; per-seat pricing, recently raised a Series B and moving up-market."
auto_inject: false
applicable_when: null
confidence: 0.85
verified_at: 2026-04-15
verified_by: nemock
staleness_signal: "Re-snapshot pricing page quarterly; refresh after any major announcement."
tags: [competitor, direct]
legal_name: "FlightPath Engineering Inc"
canonical_url: "https://flightpath-eng.example.com"
edges:
  - target: source-web-snapshot-flightpath-pricing-2026-04-15
    type: related_to
    weight: 0.85
    note: "Current pricing snapshot."
  - target: source-press-release-flightpath-2026-q1-series-b
    type: related_to
    weight: 0.8
    note: "Series B announcement informs our reading of their trajectory."
related: []
source_url: null
controlled_document: false
---

# FlightPath

## Summary

Direct fictional competitor in engineering analytics, moving from mid-market into enterprise.

## Positioning (per public signals)

"Engineering analytics for fast-moving teams." Per-seat pricing starting at $15/dev. Three tiers, with the top tier gated behind a contact-sales motion. Series B in Q1 2026.

## Where they're strong

- Brand awareness — most-mentioned competitor in our customer interviews.
- Slack digest functionality is mature.
- Established enterprise sales motion.

## Where we differ (per our hypothesis, not per their public claims)

- They price per seat; we price per workspace ([decision-003](../../decisions/decision-003-workspace-pricing-not-seat-based.md)).
- They are moving up-market; we are explicitly staying in the 50–250-engineer band ([pillar-icp-vpe-scaling-saas](../../pillars/pillar-icp-vpe-scaling-saas.md)).
- They have per-developer views; we don't and won't ([pillar-no-developer-surveillance](../../pillars/pillar-no-developer-surveillance.md)).

## Edges

`related_to` the current pricing snapshot and the Series B press release.
