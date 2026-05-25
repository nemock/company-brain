---
id: fact-trial-to-paid-q1-2026
title: "Fact: Trial-to-Paid Conversion — Q1 2026"
type: fact
namespace: gtm-metrics
summary: "Q1 2026 trial-to-paid conversion (cleanly defined) was 18%."
auto_inject: false
applicable_when: null
confidence: 0.95
verified_at: 2026-04-08
verified_by: nemock
staleness_signal: "Q1 2026 snapshot; do not update — Q2 becomes its own fact node."
tags: [fact, gtm, quarterly]
metric_id: metric-trial-to-paid-conversion
edges:
  - target: source-internal-data-q1-2026-trial-cohort
    type: derived_from
    weight: 0.95
    note: "Direct read from the Q1 cohort dataset."
related: []
source_url: null
controlled_document: false
---

# Fact: Trial-to-Paid Conversion — Q1 2026

## Summary

18% of Q1 2026 trial signups became paying customers by end of trial.

## Detail

- Trials in cohort: 213
- Converted to paid by end of trial: 38
- 38 / 213 = 17.8%, rounded to 18%.

Note: an alternative definition (activated AND paid) yields 22%; we explicitly prefer the cleaner "paid by end of trial" denominator-and-numerator. See [`source-internal-data-q1-2026-trial-cohort`](../sources/source-internal-data-q1-2026-trial-cohort.md) for the underlying data.

## Edges

`derived_from` the underlying cohort data. `metric_id` links to the metric this snapshot belongs to so confidence decay applies.
