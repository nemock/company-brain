---
id: product-line-vitalisens-cardiac-monitoring
title: "Vitalisens Cardiac Monitoring (product line)"
type: product-line
namespace: products
summary: "Vitalisens' cardiac monitoring product line: one wearable plus one disposable pad. The line is the family for both SKUs."
auto_inject: false
applicable_when: null
confidence: 0.95
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Reconsider if a second wearable variant is added or if the pad gains a separate sub-line."
tags: [product-line]
edges:
  - target: product-vitalisens-cardio
    type: part_of
    weight: 1.0
    note: "The wearable belongs to this product line."
  - target: product-vitalisens-pad
    type: part_of
    weight: 1.0
    note: "The disposable pad belongs to this product line."
related: []
source_url: null
controlled_document: false
---

# Vitalisens Cardiac Monitoring (product line)

## Summary

The product line that contains the Vitalisens Cardio wearable and the Vitalisens Pad disposable. Both are required for end-to-end use.

## Content

In v1, the line has exactly two SKUs:

- **Vitalisens Cardio** — the wearable. Capital good. One-per-patient.
- **Vitalisens Pad** — the 7-day disposable. Recurring consumable.

A patient cannot use the line without both. The pad has a defined consumption cadence (weekly during the monitoring window). The wearable has an expected service life of multiple monitoring episodes; the pad is single-use.

## Edges

Both `part_of` edges are weight 1.0 because the line is literally just the two SKUs in v1.

## Notes

If a second wearable form factor (e.g. patch vs. lanyard) ships in v2, this line either expands or splits. Decision deferred to v2.
