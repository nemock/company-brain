---
id: regulatory-clearance-K231234-cardiotrace-pro-v2
title: "510(k) K231234 — CardioTrace Pro (2025 expansion)"
type: regulatory-clearance
namespace: competitive
summary: "Fictional 510(k) clearance for CardioTrace Pro expanded indication; cleared 2025-08-30; preceded_by K181234 (original CardioTrace) and K221567 (PulseGuard)."
auto_inject: false
applicable_when: null
confidence: 0.85
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Refresh if FDA publishes additional context on this filing."
tags: [510k, clearance, competitor]
clearance_number: K231234
clearance_type: 510k
clearance_date: 2025-08-30
applicant: "CardioTrace Inc"
device_name: "CardioTrace Pro (expanded indication)"
product_codes: [DRT]
summary_url: "https://example.com/fda/cdrh/K231234-summary.pdf"
edges:
  - target: regulatory-clearance-K181234-cardiotrace-pro-v1
    type: preceded_by
    weight: 0.95
    note: "Primary predicate device — CardioTrace's own earlier clearance."
  - target: regulatory-clearance-K221567-pulseguard-rhythm
    type: preceded_by
    weight: 0.8
    note: "Secondary predicate — PulseGuard's clearance, cited for the expanded wear-time element."
  - target: competitor-cardiotrace-inc
    type: related_to
    weight: 0.9
    note: "Belongs to CardioTrace."
  - target: indication-for-use-cardiotrace-pro-2025-q3
    type: related_to
    weight: 0.95
    note: "The expanded IFU this clearance authorized."
  - target: source-fda-510k-summary-K231234-cardiotrace
    type: derived_from
    weight: 0.95
    note: "Source PDF used to populate this node."
related: []
source_url: null
controlled_document: false
---

# 510(k) K231234 — CardioTrace Pro (2025 expansion)

## Summary

The fictional second-generation CardioTrace 510(k) clearance. Cleared 2025-08-30. Cites two predicates: CardioTrace's own earlier clearance (K181234) and PulseGuard's clearance (K221567) — the latter primarily for the expanded wear-time claim.

## Content

This clearance is the most important competitive node in the vault. It demonstrates:

- IFU expansion (`indication-for-use-cardiotrace-pro-2025-q3` is the cleared IFU).
- A multi-predicate strategy (K181234 + K221567).
- The 14-day wear claim, which Vitalisens deliberately does not match.

For Vitalisens, this clearance is a candidate predicate for our planned filing. Citing it would establish substantial equivalence to a modern MCT device with broad IFU.

## Edges

Two `preceded_by` edges, the canonical pattern for predicate chains. An agent walking outward from this node sees both upstream clearances and their IFUs.

`derived_from` the 510(k) summary PDF makes the source explicit.

## Notes

Fictional. The K-number, date, and applicant are invented. The structure of the predicate chain (two predicates, one for the device-class and one for the expanded claim) follows realistic 510(k) practice, but the specific filings are not real.
