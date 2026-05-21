---
id: indication-for-use-cardiotrace-pro-2025-q3
title: "IFU: CardioTrace Pro v2 (2025 Q3, expanded)"
type: indication-for-use
namespace: competitive
summary: "CardioTrace Pro expanded IFU from the 2025 clearance: adds post-cardiac-event surveillance and 14-day continuous wear."
auto_inject: false
applicable_when: null
confidence: 0.85
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Refresh if CardioTrace files a further IFU expansion or contraction."
tags: [ifu, competitor, current]
population: "Adult patients aged 18 years and older with documented or suspected arrhythmia or in the post-cardiac-event surveillance window"
condition: "Documented arrhythmia, suspected arrhythmia, OR post-cardiac-event surveillance"
intervention: "Continuous ambulatory ECG recording for up to 14 days, transmitted to a clinician-reviewable platform"
setting: "Home and outpatient clinical settings"
belongs_to_product: product-vitalisens-cardio
edges:
  - target: indication-for-use-cardiotrace-pro-2023-q1
    type: preceded_by
    weight: 0.95
    note: "Successor to the 2023 IFU. The IFU history chain: 2023-q1 → 2025-q3."
  - target: competitor-cardiotrace-inc
    type: related_to
    weight: 0.9
    note: "Belongs to CardioTrace's product."
  - target: regulatory-clearance-K231234-cardiotrace-pro-v2
    type: related_to
    weight: 0.95
    note: "The 510(k) that cleared this expanded IFU."
  - target: source-fda-510k-summary-K231234-cardiotrace
    type: derived_from
    weight: 0.9
    note: "IFU language captured from the public 510(k) summary."
  - target: source-press-release-cardiotrace-2025-q3-launch
    type: derived_from
    weight: 0.7
    note: "Press release announced the expansion; not the primary regulatory source."
related: []
source_url: null
controlled_document: false
---

# IFU: CardioTrace Pro v2 (2025 Q3, expanded)

## Summary

CardioTrace's expanded IFU as cleared in 2025 Q3. Two key changes vs. the 2023 IFU: post-cardiac-event surveillance was added, and labeled wear time was extended to 14 days.

## Content

The expansion has two notable elements:

1. **Population/condition broadening**: the original IFU required documented arrhythmia or palpitations; the new IFU allows suspected arrhythmia and post-event surveillance. This is a meaningful indication expansion.
2. **Wear time extension**: 14 days vs. the prior 7-day window. CardioTrace markets this aggressively.

For Vitalisens, this expansion matters in two ways:

- It establishes a useful predicate for our planned 510(k) (`regulatory-clearance-K243189-vitalisens-cardio`).
- The 14-day wear claim is something we deliberately do **not** match (see `decision-003-7-day-wear-not-14-day` and the underlying pattern of pad failure beyond day 10).

## Edges

`preceded_by` the 2023 IFU is the **IFU history chain** — the primary use of this edge type in the medical-device profile. An agent walking the chain from this node can find the prior IFU in one hop.

## Notes

This is the second IFU in the CardioTrace product's history. If a third IFU lands, it would have `preceded_by: indication-for-use-cardiotrace-pro-2025-q3` and the chain extends. The maintain skill (v0.4.0) will surface long chains where they exist.
