---
id: decision-003-7-day-wear-not-14-day
title: "Decision 003: 7-Day Pad Wear Time"
type: decision
namespace: product-design
summary: "Vitalisens Pad is rated for 7 days of continuous wear. We will not pursue a 14-day variant in v1."
auto_inject: false
applicable_when: null
confidence: 0.88
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Revisit if pad adhesion data improves materially, or if a major payer aligns reimbursement around 14-day windows in a way that disadvantages 7-day."
tags: [decision, product-design, pad]
edges:
  - target: pillar-disposable-pad-business-model
    type: supports
    weight: 0.85
    note: "Wear time is the primary lever on pad turnover and recurring revenue."
  - target: pattern-pad-adhesion-failure-precedes-data-dropout
    type: derived_from
    weight: 0.8
    note: "Pattern observed in trial cohort drives the choice of 7 vs 14 days."
  - target: hypothesis-7-day-wear-improves-compliance
    type: related_to
    weight: 0.85
    note: "Specific bet about compliance vs wear time that this decision encodes."
related: []
source_url: null
controlled_document: false
---

# Decision 003: 7-Day Pad Wear Time

## Summary

The Vitalisens Pad is labeled for 7 days of continuous wear. We will not engineer, validate, or label a 14-day variant in v1.

## Alternatives Considered

1. **3-day pad.** Higher recurring revenue per patient, but unacceptable burden for patients and likely worse compliance.
2. **7-day pad.** Chosen.
3. **14-day pad.** Better patient burden, but pad-adhesion data in our trial cohort shows failure rates climbing sharply past day 10.
4. **Wearer-replaceable hybrid that supports both labels.** Rejected — single labeling avoids confusion and simplifies clinical guidance.

## Decision

7-day wear is the labeled and validated wear time for v1. Patients receive a fresh pad weekly. Clinical workflow assumes weekly pad replacement events.

## Rationale

- Adhesion data from the trial cohort shows clean performance through day 7, with failure rates rising past day 10. A 14-day label would push us into a window where pad failure (and the associated data-quality loss) becomes the dominant failure mode.
- Weekly cadence is intuitive for patients and aligns with typical follow-up patterns.
- The recurring-revenue model works at 7-day cadence; we do not need 14 days to make unit economics work.

## What This Rules Out

- **A 14-day Vitalisens Pad variant in v1.** No engineering work toward 14-day adhesion validation.
- **Labeling that implies extended wear.** IFU language will be explicit about the 7-day window.
- **Off-label "you can keep it on longer" marketing.** No language that encourages extended wear.

## Edges

`pattern-pad-adhesion-failure-precedes-data-dropout` is the evidence base. If that pattern weakens (i.e., we improve adhesion such that day-10+ failures become rare), this decision becomes a candidate for re-opening.

## Notes

Cardiotrace's 14-day claim is a competitive consideration but not a strategic one — they have a different pad chemistry and a different clinical positioning. This decision reflects what Vitalisens can credibly support, not what competitors are doing.
