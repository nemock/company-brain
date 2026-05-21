---
id: metric-pad-attach-rate-day-1
title: "Metric: Pad Attach Rate at Day 1"
type: metric
namespace: metrics
summary: "Percent of trial-cohort patients whose pad is still attached and capturing data 24 hours after initial application; high-volatility cohort indicator."
auto_inject: false
applicable_when: null
confidence: 0.9
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Revisit if pad chemistry or application protocol changes."
tags: [metric, pad, kpi]
volatility_class: high
edges:
  - target: pillar-disposable-pad-business-model
    type: related_to
    weight: 0.7
    note: "Attach rate is a leading indicator for the pad business."
related: []
source_url: null
controlled_document: false
---

# Metric: Pad Attach Rate at Day 1

## Summary

Percent of trial-cohort patients whose pad is still attached and producing usable data 24 hours after initial application. High volatility — moves significantly week-to-week with cohort composition and application-training quality.

## Content

Why this metric:

- Day-1 attach is the leading indicator for the rest of the 7-day cycle. A pad that fails to seat properly almost never recovers.
- It is patient- and clinician-controllable, so it isolates application-quality from pad-chemistry issues.
- It is cheap to measure and informs decisions about training, packaging instructions, and pad design.

Computation:

- Numerator: patients with continuous data capture between hours 12-24 post-application.
- Denominator: patients enrolled in the cohort.
- Excludes: patients who voluntarily removed the pad in the first 24 hours (small cohort; tracked separately).

## Edges

Loose `related_to` into the business-model pillar — the metric is downstream of the pillar's strategic emphasis on pad performance.

## Notes

`volatility_class: high` means snapshot facts of this metric have a 30-day confidence half-life under the v0.4.0 `maintain` decay rules. This is deliberate — a 6-month-old attach-rate snapshot tells us very little.
