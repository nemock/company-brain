---
id: hypothesis-7-day-wear-improves-compliance
title: "Hypothesis: 7-Day Wear Improves Patient Compliance vs. 14-Day"
type: hypothesis
namespace: product-design
summary: "We hypothesize that a 7-day wear cycle drives higher patient compliance (data completeness) than a 14-day cycle, despite the operational overhead of more pad changes."
auto_inject: false
applicable_when: null
confidence: 0.65
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Re-evaluate at the close of the Q2 cohort and against any longitudinal data we acquire."
tags: [hypothesis, pad, compliance]
edges:
  - target: decision-003-7-day-wear-not-14-day
    type: supports
    weight: 0.8
    note: "Decision is anchored on this hypothesis being true."
  - target: pattern-pad-adhesion-failure-precedes-data-dropout
    type: supports
    weight: 0.85
    note: "Pattern is consistent with the hypothesis (compliance falls when pads fail late in cycle)."
related: []
source_url: null
controlled_document: false
---

# Hypothesis: 7-Day Wear Improves Patient Compliance vs. 14-Day

## Summary

We bet that 7-day cycles drive better data completeness than 14-day cycles because adhesion-related failures cluster late in the cycle. Falsifiable: compare data-completeness rates between 7-day-cycle cohorts (Vitalisens) and 14-day-cycle cohorts (CardioTrace, if data ever becomes available).

## What Would Test This

- Internal data from Vitalisens trial cohorts: does day-7 data completeness consistently outperform what would be expected from a 14-day cycle with adhesion failure clustered post-day-10?
- External data from CardioTrace cohorts (if available via clinician relationships): compares directly.
- Adverse-event reporting in the MAUDE database for both wear-time approaches.

## Edges

`supports` `decision-003-7-day-wear-not-14-day` — the decision depends on this hypothesis being true. If we falsify the hypothesis, the decision is a candidate for re-opening.

## Notes

Confidence 0.65 is deliberately modest — this is a real bet, not a sure thing. As evidence accumulates, confidence should track.
