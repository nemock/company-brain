---
id: indication-for-use-pulseguard-rhythm-2022-q4
title: "IFU: PulseGuard Rhythm (2022 Q4)"
type: indication-for-use
namespace: competitive
summary: "PulseGuard Rhythm cleared IFU; ambulatory ECG, patient self-managed after clinic placement, adults with arrhythmia evaluation needs."
auto_inject: false
applicable_when: null
confidence: 0.8
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Refresh if PulseGuard files an updated IFU."
tags: [ifu, competitor]
population: "Adult patients aged 18 years and older referred for ambulatory cardiac evaluation"
condition: "Suspected cardiac arrhythmia under clinical evaluation"
intervention: "Clinic-placed continuous ambulatory ECG with patient-managed pad changes"
setting: "Home use following initial clinic placement"
belongs_to_product: product-vitalisens-cardio
edges:
  - target: competitor-pulseguard-medical
    type: related_to
    weight: 0.9
    note: "Belongs to PulseGuard's product."
  - target: regulatory-clearance-K221567-pulseguard-rhythm
    type: related_to
    weight: 0.95
    note: "The 510(k) that cleared this IFU."
related: []
source_url: null
controlled_document: false
---

# IFU: PulseGuard Rhythm (2022 Q4)

## Summary

PulseGuard Rhythm's IFU as cleared in late 2022. Single version — no IFU history chain. Notable for the explicit clinic-placement framing.

## Content

The IFU distinguishes itself by specifying clinic placement followed by patient-managed pad changes. This is a workflow distinction that maps to PulseGuard's positioning.

## Edges

Single competitor; single IFU. No `preceded_by` chain because there isn't one.

## Notes

This IFU's clearance (`regulatory-clearance-K221567-pulseguard-rhythm`) is widely cited as a predicate by other MCT 510(k) filings. The clearance itself is structurally important even though the company is smaller than CardioTrace.

Like the CardioTrace historical IFUs, this points `belongs_to_product` at our product as a placeholder. See note in `indication-for-use-cardiotrace-pro-2023-q1`.
