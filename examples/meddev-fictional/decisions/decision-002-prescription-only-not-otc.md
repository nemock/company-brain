---
id: decision-002-prescription-only-not-otc
title: "Decision 002: Prescription-Only, Not Over-the-Counter"
type: decision
namespace: regulatory
summary: "Vitalisens will be sold by prescription only (Rx). We will not pursue over-the-counter (OTC) labeling, packaging, or distribution in v1 or v2."
auto_inject: false
applicable_when: null
confidence: 0.95
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Revisit if FDA OTC pathway for cardiac monitoring becomes well-established, or if a strategic consumer-channel partnership becomes available."
tags: [decision, regulatory, strategy]
edges:
  - target: pillar-icp-ambulatory-cardiac-patients
    type: supports
    weight: 0.9
    note: "Rx-only is consistent with the clinical ICP."
  - target: hypothesis-rx-only-preserves-reimbursement
    type: related_to
    weight: 0.8
    note: "The hypothesis that drives this decision."
  - target: source-strategic-thesis-disposable-pad-recurring-revenue
    type: derived_from
    weight: 0.6
    note: "Rx channel aligns with the recurring-pad business model through clinical workflows."
related: []
source_url: null
controlled_document: false
---

# Decision 002: Prescription-Only, Not Over-the-Counter

## Summary

Vitalisens is and will remain a prescription medical device. We will not pursue OTC labeling, OTC clearance, or consumer retail distribution for the duration of v1 and v2.

## Alternatives Considered

1. **OTC from launch.** Rejected — would require a substantially different (and likely longer) regulatory pathway, and the resulting device would still need a clinician to interpret the ECG data.
2. **Rx for v1, OTC for v2.** Rejected — splitting the product into two regulatory regimes would fragment manufacturing, distribution, and reimbursement.
3. **Rx-only, indefinitely.** Chosen.
4. **Hybrid: clinic dispenses, patient self-applies.** This is actually our default Rx model and not a separate alternative; the patient self-applies the pad after the clinic prescribes the device.

## Decision

Vitalisens is Rx-only. The wearable is dispensed by the clinic; the patient or caregiver self-applies and replaces pads at home.

## Rationale

- ECG interpretation requires a clinician; selling without clinician involvement would be both clinically and regulatorily problematic.
- Reimbursement coding for ambulatory cardiac monitoring assumes a prescribing physician; Rx is the path that preserves reimbursement.
- The recurring-pad business depends on a clinical workflow, which Rx supports and OTC would disrupt.

## What This Rules Out

- **OTC labeling.** Packaging and IFU will explicitly state Rx-only.
- **Consumer retail channels.** Vitalisens will not be sold in pharmacies, big-box retail, or DTC consumer e-commerce.
- **Consumer-direct marketing claims.** Marketing addresses clinicians (and patients via clinician referral), not general consumers.
- **OTC clearance pursuit.** No regulatory effort is allocated to an OTC pathway.

## Edges

`hypothesis-rx-only-preserves-reimbursement` captures the testable underpinning of this decision. If that hypothesis weakens (e.g., reimbursement landscape shifts to favor OTC), this decision is the place to start re-evaluating.

## Notes

Two adjacent decisions are not made by this one: (a) which exact CPT/HCPCS codes Vitalisens targets, and (b) whether we pursue a class-I sister product for wellness monitoring. Both are out of scope for this decision; flag them as open if they come up.
