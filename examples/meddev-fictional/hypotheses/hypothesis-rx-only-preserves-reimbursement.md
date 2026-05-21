---
id: hypothesis-rx-only-preserves-reimbursement
title: "Hypothesis: Rx-Only Preserves Reimbursement Coding"
type: hypothesis
namespace: regulatory
summary: "We hypothesize that the existing reimbursement coding for ambulatory cardiac monitoring assumes a prescribing physician, and that OTC distribution would jeopardize that coding."
auto_inject: false
applicable_when: null
confidence: 0.75
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Refresh after major CMS coding changes or any OTC-MCT FDA pathway development."
tags: [hypothesis, reimbursement]
edges:
  - target: decision-002-prescription-only-not-otc
    type: supports
    weight: 0.85
    note: "Decision relies on this hypothesis."
related: []
source_url: null
controlled_document: false
---

# Hypothesis: Rx-Only Preserves Reimbursement Coding

## Summary

The hypothesis: existing US reimbursement coding for ambulatory cardiac monitoring assumes a prescribing physician relationship. Moving to OTC distribution would either (a) require new coding work, or (b) reduce reimbursability.

## What Would Test This

- Specific CMS guidance on whether existing CPT/HCPCS codes for MCT require a prescribing physician.
- Payer policies from major commercial insurers.
- Precedent from other devices that have moved from Rx to OTC.

## Edges

`supports` `decision-002-prescription-only-not-otc` is the dependency. If we falsify this hypothesis (e.g., if CMS issues guidance that explicitly permits OTC MCT under existing codes), the decision becomes a candidate for re-opening.

## Notes

This is a planning-level hypothesis. Validating it would require either internal reimbursement counsel work or a formal coverage analysis — neither of which has happened yet. Confidence is moderate (0.75) reflecting both domain belief and uncertainty.
