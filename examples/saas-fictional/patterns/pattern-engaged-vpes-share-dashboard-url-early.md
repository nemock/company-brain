---
id: pattern-engaged-vpes-share-dashboard-url-early
title: "Pattern: Engaged VPEs Share the Dashboard URL Early"
type: pattern
namespace: activation
summary: "Across the Q1 2026 customer interviews, every VPE who retained had shared the Loftwing dashboard URL in their team's Slack within the first week."
auto_inject: false
applicable_when: null
confidence: 0.7
verified_at: 2026-04-09
verified_by: nemock
staleness_signal: "Validate with a structured cohort study in Q2 2026; until then this is an observed pattern, not a measured one."
tags: [pattern, activation]
edges:
  - target: source-customer-interview-2026-03-vpe-northgate
    type: derived_from
    weight: 0.7
    note: "Northgate VPE described shaping the team's Slack around the dashboard within the first week."
related: []
source_url: null
controlled_document: false
---

# Pattern: Engaged VPEs Share the Dashboard URL Early

## Summary

A consistently-observed early-engagement behavior worth measuring.

## Observation

Across all four Q1 2026 customer interviews with VPEs who had been on the platform 60+ days, all four reported having pasted the Loftwing dashboard URL into their team's Slack within the first week. The not-yet-engaged trial users we spoke with had not done this.

## Hypothesis this generates

See [hypothesis-dashboard-url-shared-in-slack-predicts-retention](../hypotheses/hypothesis-dashboard-url-shared-in-slack-predicts-retention.md). The hypothesis takes the pattern from "observation" to "predictive signal we can intervene on."

## What this pattern is NOT

Four interviews is a small sample. The pattern is a hypothesis-generator, not evidence. Treat it as such until the Q2 cohort study runs.

## Edges

`derived_from` the Northgate customer interview where the behavior was first explicitly described.
