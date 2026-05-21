---
id: stakeholder-cardiology-program-director
title: "Stakeholder: Cardiology Program Director (buying decision maker)"
type: stakeholder
namespace: market
summary: "The cardiology program director at a multi-site practice; signs MCT vendor contracts and owns the patient-monitoring SLA."
auto_inject: false
applicable_when: null
confidence: 0.75
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Refresh after the next stakeholder mapping exercise or if buying authority shifts."
tags: [stakeholder, buyer]
edges:
  - target: customer-northstar-cardiology-2025
    type: related_to
    weight: 0.8
    note: "The trial customer's program director is the archetype this stakeholder describes."
related: []
source_url: null
controlled_document: false
---

# Stakeholder: Cardiology Program Director

## Summary

The clinician-administrator at a multi-site cardiology practice who decides which monitoring vendors the practice uses. Owns the operational quality of the patient-monitoring program — uptime, data quality, clinician satisfaction, patient experience.

## Content

What they evaluate:

- **Data quality.** Are we getting clean signals on cohort patients? How often do we have to call patients back for re-application?
- **Clinical workflow fit.** Does the clinician app slot into our EHR review pattern? How long does triage take?
- **Reimbursement.** Are we coding correctly? Are we leaving money on the table?
- **Patient experience.** Are patients calling support a lot? Are they pulling pads off early?

What they do NOT evaluate (much):

- Pricing per device. They care about per-patient economics over the monitoring window.
- Sensor specs in isolation. They care about whether the monitoring report is clinically actionable.

## Edges

The `related_to` edge into the trial customer makes the abstract stakeholder concrete in our pilot.

## Notes

A second stakeholder archetype — the practice's purchasing/contracts lead — is implicit. We have not promoted that to its own node because it has not driven any decision in this vault yet.
