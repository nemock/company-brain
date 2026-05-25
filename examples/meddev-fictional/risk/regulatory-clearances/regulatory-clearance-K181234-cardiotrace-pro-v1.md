---
id: regulatory-clearance-K181234-cardiotrace-pro-v1
title: 510(k) K181234 — CardioTrace Pro (original)
type: regulatory-clearance
namespace: competitive
summary: Fictional 510(k) clearance for CardioTrace Pro original device; cleared 2023-02-14;
  predicate for the 2025 expansion clearance.
auto_inject: false
applicable_when: null
confidence: 0.85
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: Frozen — historical clearance.
tags:
- 510k
- clearance
- competitor
- historical
clearance_number: K181234
clearance_type: 510k
clearance_date: 2023-02-14
applicant: CardioTrace Inc
device_name: CardioTrace Pro
product_codes:
- DRT
summary_url: https://example.com/fda/cdrh/K181234-summary.pdf
edges:
- target: competitor-cardiotrace-inc
  type: related_to
  weight: 0.9
  note: Belongs to CardioTrace.
- target: indication-for-use-cardiotrace-pro-2023-q1
  type: related_to
  weight: 0.95
  note: The IFU this clearance authorized.
- target: regulatory-clearance-K231234-cardiotrace-pro-v2
  type: followed_by
  weight: 0.95
  note: auto-added inverse of preceded_by from regulatory-clearance-K231234-cardiotrace-pro-v2
related: []
source_url: null
controlled_document: false
---

# 510(k) K181234 — CardioTrace Pro (original)

## Summary

The original 510(k) clearance for CardioTrace Pro. Fictional. Issued 2023-02-14 under product code DRT. Cited as the predicate in CardioTrace's later 2025 filing.

## Content

This clearance is referenced here because:

- It is the upstream predicate for `regulatory-clearance-K231234-cardiotrace-pro-v2`.
- It anchors the original IFU (`indication-for-use-cardiotrace-pro-2023-q1`).

For Vitalisens, this clearance is one possible predicate in our own filing. The decision to cite this vs. the v2 (broader) clearance vs. PulseGuard's clearance is a regulatory strategy choice not captured here.

## Edges

No `preceded_by` edges out of this node because it is the upstream end of the chain in our (limited) competitive archive. If we later learn about an earlier CardioTrace predicate, it would attach via `preceded_by` here.

## Notes

All fields (K-number, date, applicant) are fictional. The `summary_url` points at `example.com` and would resolve to nothing in reality.
