---
id: fact-pad-attach-rate-2026-q1
title: "Fact: Pad Attach Rate at Day 1 — 2026 Q1 Cohort"
type: fact
namespace: metrics-snapshots
summary: "Q1 2026 trial cohort day-1 pad attach rate: 89% (12 of 14 patients with continuous data through hour 24)."
auto_inject: false
applicable_when: null
confidence: 0.95
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Q1 cohort snapshot is permanent. Q2 snapshot will be a separate fact node."
tags: [fact, metric-snapshot]
metric_id: metric-pad-attach-rate-day-1
edges:
  - target: metric-pad-attach-rate-day-1
    type: part_of
    weight: 1.0
    note: "Snapshot of this metric."
  - target: source-internal-data-q1-2026-pad-attach-rate
    type: derived_from
    weight: 0.95
    note: "Data origin."
related: []
source_url: null
controlled_document: false
---

# Fact: Pad Attach Rate at Day 1 — 2026 Q1 Cohort

## Summary

For the Q1 2026 trial cohort at Northstar Cardiology (n=14), the pad attach rate at hour 24 was 89% (12 patients with continuous data; 2 patients with partial pad lift in the first 24 hours).

## Content

The two failures were:

- Patient A: pad lifted on one electrode within the first 12 hours; reseated by patient overnight; data quality recovered.
- Patient B: pad detached almost completely by hour 18; required full replacement by morning.

Both failures were detected through routine review, not through real-time alarming. (Real-time alarming is captured as `risk-control-idea-disconnection-alarm-via-app`.)

## Edges

`part_of` the metric node; `derived_from` the internal-data source.

## Notes

`metric_id: metric-pad-attach-rate-day-1` makes this a time-series snapshot. Under the v0.4.0 confidence-decay rules, a high-volatility metric snapshot has a 30-day half-life. By the time the Q2 cohort lands, this fact's effective confidence will have decayed, and the maintain skill will surface it for re-verification or supersession.
