---
id: fact-weekly-active-teams-2026-w14
title: "Fact: Weekly Active Teams — 2026 Week 14"
type: fact
namespace: product-metrics
summary: "Week of 2026-04-06: 47 distinct paying workspaces loaded a Loftwing dashboard at least once."
auto_inject: false
applicable_when: null
confidence: 0.9
verified_at: 2026-04-13
verified_by: nemock
staleness_signal: "Weekly snapshot; do not update — next week becomes its own fact node."
tags: [fact, product, weekly]
metric_id: metric-weekly-active-teams
edges:
  - target: source-internal-data-q1-2026-trial-cohort
    type: related_to
    weight: 0.5
    note: "Cohort data is the upstream source for activation tracking; weekly-active uses the same warehouse."
related: []
source_url: null
controlled_document: false
---

# Fact: Weekly Active Teams — 2026 Week 14

## Summary

47 distinct paying workspaces active in the week of 2026-04-06.

## Detail

The number was 41 in week 13 and 39 in week 12, so this is a real week-over-week rise (likely driven by the new Slack-digest feature shipped at end of week 12). The maintain skill's confidence decay applies because the metric is `volatility_class: high` — by week 22 this snapshot's confidence should be visibly degraded.
