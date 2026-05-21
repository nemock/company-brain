---
id: pattern-pad-adhesion-failure-precedes-data-dropout
title: "Pattern: Pad Adhesion Failure Precedes Data Dropout"
type: pattern
namespace: product-data
summary: "Across the Q1 2026 cohort, every observed data-dropout event was preceded (by hours to days) by partial pad adhesion failure; full detachment is the late stage of a slow drift."
auto_inject: false
applicable_when: null
confidence: 0.8
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Re-evaluate after each cohort. Pattern may not hold for different pad chemistries."
tags: [pattern, pad, data-quality]
edges:
  - target: source-internal-data-q1-2026-pad-attach-rate
    type: derived_from
    weight: 0.9
    note: "Pattern observed in this cohort's data."
  - target: risk-insight-pad-adhesion-failure-affects-data-quality
    type: supports
    weight: 0.85
    note: "Pattern is the evidence base for the risk insight."
related: []
source_url: null
controlled_document: false
---

# Pattern: Pad Adhesion Failure Precedes Data Dropout

## Summary

In the Q1 2026 cohort, every data-dropout event we observed was preceded — typically by hours, sometimes by days — by partial pad adhesion failure. Pad detachment is not a binary event; it's the late stage of a drift that can be detected earlier.

## Content

The pattern (n=2 dropouts in 14 patients):

- Patient A: pad lifted at one electrode at hour 8; full single-channel data degradation by hour 14; reseated overnight.
- Patient B: pad lifted progressively starting hour 14; near-total detachment by hour 18.

In both cases:

- Signal-quality metrics on the device-side were already trending down before the patient noticed.
- A real-time alarm threshold tied to signal-quality scoring would likely have caught the drift.

## Edges

`derived_from` the internal data source; `supports` the risk-insight.

## Notes

Two observations is a small base for a strong pattern claim. The 0.8 confidence reflects that. As more cohorts accumulate, this pattern should either strengthen or be revised. The maintain skill will surface it for re-evaluation.
