---
id: regulatory-clearance-K243189-vitalisens-cardio
title: "510(k) K243189 — Vitalisens Cardio (planned)"
type: regulatory-clearance
namespace: regulatory-planning
summary: "Vitalisens' planned 510(k) clearance; K-number placeholder; predicate citations include K231234 (CardioTrace v2) and K221567 (PulseGuard)."
auto_inject: false
applicable_when: null
confidence: 0.5
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Update as submission strategy firms up; revise on actual K-number assignment."
tags: [510k, clearance, planned, vitalisens]
clearance_number: K243189
clearance_type: 510k
clearance_date: 2026-12-31
applicant: "Vitalisens (fictional)"
device_name: "Vitalisens Cardio"
product_codes: [DRT]
summary_url: "https://example.com/fda/cdrh/K243189-summary.pdf"
edges:
  - target: regulatory-clearance-K231234-cardiotrace-pro-v2
    type: preceded_by
    weight: 0.85
    note: "Primary predicate — CardioTrace's expanded clearance establishes substantial equivalence for the MCT device class with modern IFU."
  - target: regulatory-clearance-K221567-pulseguard-rhythm
    type: preceded_by
    weight: 0.75
    note: "Secondary predicate — PulseGuard's clearance is widely cited as a reference anchor for MCT filings."
  - target: product-vitalisens-cardio
    type: related_to
    weight: 0.95
    note: "Clearance is for this product."
  - target: indication-for-use-vitalisens-cardio-2026-q1
    type: related_to
    weight: 0.95
    note: "Cited IFU in the planned submission."
related: []
source_url: null
controlled_document: false
---

# 510(k) K243189 — Vitalisens Cardio (planned)

## Summary

The planned 510(k) submission for Vitalisens Cardio. The K-number is a placeholder; the actual K-number is assigned by FDA on submission. Clearance date is a placeholder target, not a committed milestone.

## Content

The planned submission cites two predicates:

- **`regulatory-clearance-K231234-cardiotrace-pro-v2`** (primary): establishes substantial equivalence for the broader MCT device class with the modern (post-2024) IFU shape.
- **`regulatory-clearance-K221567-pulseguard-rhythm`** (secondary): widely-cited anchor for MCT filings, included to strengthen substantial-equivalence framing on workflow-related claims.

The cited IFU is `indication-for-use-vitalisens-cardio-2026-q1`. The submission is **planning**, not controlled regulatory work — when the submission is actually prepared, it will be authored in the QMS system under controlled change management.

## Edges

Two `preceded_by` edges — the canonical predicate-chain pattern. This node demonstrates the **outbound** end of the chain (us pointing to predicates), in contrast to PulseGuard's K221567 which is the **inbound** end (others pointing to it as a predicate).

## Notes

Lower confidence (0.5) than the other clearance nodes because this is forward-looking planning, not a fact about a cleared device. Confidence will rise to ~0.95 once the submission is filed and cleared.

`controlled_document: false` defensively, as with all `regulatory-clearance` nodes — this is a planning artifact about a future filing, not the filing itself.
