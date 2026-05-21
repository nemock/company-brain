---
id: fact-pad-attach-rate-2026-q2
title: "Fact: Pad Attach Rate at Day 1 — 2026 Q2 Cohort (interim)"
type: fact
namespace: metrics-snapshots
summary: "Q2 2026 interim cohort day-1 pad attach rate: 91% (10 of 11 patients enrolled to date); reflects updated application coaching."
auto_inject: false
applicable_when: null
confidence: 0.85
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Update at cohort closure; promote to final snapshot when n stabilizes."
tags: [fact, metric-snapshot, interim]
metric_id: metric-pad-attach-rate-day-1
edges:
  - target: metric-pad-attach-rate-day-1
    type: part_of
    weight: 1.0
    note: "Snapshot of this metric."
  - target: fact-pad-attach-rate-2026-q1
    type: preceded_by
    weight: 0.9
    note: "Time series: Q1 → Q2 cohort. Q2 succeeds Q1."
related: []
source_url: null
controlled_document: false
---

# Fact: Pad Attach Rate at Day 1 — 2026 Q2 Cohort (interim)

## Summary

Q2 2026 cohort interim measurement: 91% day-1 attach rate (10/11 enrolled patients). Slight improvement over Q1 attributed to updated application coaching protocol.

## Content

Interim snapshot — cohort still enrolling. Final number may differ. Captured here to demonstrate the time-series chain and to show how interim measurements are flagged with reduced confidence vs. closed-cohort snapshots.

## Edges

`preceded_by: fact-pad-attach-rate-2026-q1` — this is the time-series chain pattern. The fact node uses the same `preceded_by` edge as IFU history chains and predicate device chains. One edge type, many use cases.

## Notes

Lower confidence (0.85 vs. 0.95) than the Q1 snapshot because the cohort is not closed. Will be revisited and the confidence raised when enrollment closes.
