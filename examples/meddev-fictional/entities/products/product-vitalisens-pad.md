---
id: product-vitalisens-pad
title: "Vitalisens Pad"
type: product
namespace: products
summary: "7-day single-use adhesive sensor pad; couples patient skin to the Vitalisens Cardio wearable; the recurring-revenue consumable."
auto_inject: false
applicable_when: null
confidence: 0.88
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Revisit when pad chemistry, adhesion validation, or labeling changes."
tags: [product, disposable, consumable]
edges:
  - target: product-line-vitalisens-cardiac-monitoring
    type: part_of
    weight: 1.0
    note: "Belongs to the cardiac-monitoring product line."
  - target: pillar-disposable-pad-business-model
    type: supports
    weight: 0.9
    note: "Pad IS the recurring revenue engine the pillar describes."
  - target: decision-003-7-day-wear-not-14-day
    type: derived_from
    weight: 0.9
    note: "7-day wear is the labeled use."
related: []
source_url: null
controlled_document: false
---

# Vitalisens Pad

## Summary

Single-use adhesive sensor pad with embedded electrodes. Snaps to the Vitalisens Cardio wearable. Labeled for 7 days of continuous wear. Replaced weekly during a monitoring episode.

## Content

In v1, one pad SKU:

- Hydrocolloid-based adhesive; hypoallergenic by primary panel.
- Two dry electrodes positioned per standard ambulatory ECG placement.
- Snap-fit interface compatible with Vitalisens Cardio.
- Color-coded by orientation to reduce mis-application.
- Packaged singly in sealed pouches; box-of-7 standard distribution unit.

## Edges

`supports` into the business-model pillar because the pad is the operational vehicle for the recurring-revenue thesis.

`derived_from` the 7-day-wear decision is the labeling reality.

## Notes

A second pad formulation for sensitive skin is an open question — see `question-second-pad-formulation-for-sensitive-skin`. Note that the question is intentionally open; in v1 we ship one pad.
