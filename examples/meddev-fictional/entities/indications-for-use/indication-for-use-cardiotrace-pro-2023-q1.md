---
id: indication-for-use-cardiotrace-pro-2023-q1
title: "IFU: CardioTrace Pro v1 (2023 Q1, original clearance)"
type: indication-for-use
namespace: competitive
summary: "CardioTrace Pro v1 original IFU as cleared in 2023; ambulatory ECG in adults with documented arrhythmia or palpitations."
auto_inject: false
applicable_when: null
confidence: 0.85
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Frozen — this is the historical IFU. Update only if FDA re-released documents change."
tags: [ifu, competitor, historical]
population: "Adult patients aged 18 years and older with documented arrhythmia or symptomatic palpitations"
condition: "Documented cardiac arrhythmia or symptomatic palpitations"
intervention: "Continuous ambulatory ECG recording transmitted to a clinician-reviewable platform"
setting: "Home and outpatient clinical settings"
belongs_to_product: product-vitalisens-cardio
edges:
  - target: competitor-cardiotrace-inc
    type: related_to
    weight: 0.9
    note: "Belongs to CardioTrace's product."
  - target: regulatory-clearance-K181234-cardiotrace-pro-v1
    type: related_to
    weight: 0.95
    note: "The 510(k) that cleared this IFU."
  - target: source-fda-510k-summary-K231234-cardiotrace
    type: derived_from
    weight: 0.7
    note: "Cross-referenced in CardioTrace's later 510(k) summary."
related: []
source_url: null
controlled_document: false
---

# IFU: CardioTrace Pro v1 (2023 Q1, original clearance)

## Summary

The original CardioTrace Pro IFU as cleared in early 2023. Captured here as a historical snapshot so the IFU expansion in 2025 can be compared against it.

## Content

The 2023 IFU was deliberately narrow — focused on patients who already had documented arrhythmia or specific symptoms. This was a typical first-clearance scope.

## Edges

`derived_from` the CardioTrace K231234 summary because that later summary cross-references the original IFU when establishing predicate continuity.

## Notes

This node uses `belongs_to_product: product-vitalisens-cardio` only because the v0.1.0 schema requires `belongs_to_product` to be set and we don't model competitor products as their own product nodes in this example. A v1.x improvement would be to add competitor products as `product` nodes (perhaps with a namespace-based separation between ours and theirs). For now, this points at our product as a placeholder — flag if `cb validate` ever inspects this for semantic correctness.
