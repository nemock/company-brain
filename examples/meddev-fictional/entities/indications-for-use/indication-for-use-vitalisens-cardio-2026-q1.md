---
id: indication-for-use-vitalisens-cardio-2026-q1
title: "IFU: Vitalisens Cardio (planned, 2026 Q1)"
type: indication-for-use
namespace: regulatory-planning
summary: "Planned IFU for Vitalisens Cardio: ambulatory ECG recording in adult patients with suspected arrhythmia, in home and outpatient settings."
auto_inject: false
applicable_when: null
confidence: 0.75
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Revisit on every planned-clearance milestone; especially before submission."
tags: [ifu, planning]
population: "Adult patients aged 18 years and older"
condition: "Suspected cardiac arrhythmia or post-cardiac-event surveillance"
intervention: "Continuous ambulatory ECG recording over a 7-day pad cycle, transmitted to a clinician-reviewable application"
setting: "Home and outpatient clinical settings; not for in-patient acute monitoring"
belongs_to_product: product-vitalisens-cardio
edges:
  - target: product-vitalisens-cardio
    type: related_to
    weight: 0.95
    note: "Implementing product."
  - target: regulatory-clearance-K243189-vitalisens-cardio
    type: related_to
    weight: 0.9
    note: "Planned clearance that will cite this IFU."
  - target: pillar-icp-ambulatory-cardiac-patients
    type: supports
    weight: 0.85
    note: "IFU and ICP are aligned by construction."
related: []
source_url: null
controlled_document: false
---

# IFU: Vitalisens Cardio (planned, 2026 Q1)

## Summary

This is the IFU language we plan to submit. It is a planning artifact — not a controlled regulatory record. The submitted IFU will be re-authored under the QMS process before filing.

## Content

Plain-language version of the planned IFU:

Vitalisens Cardio is intended for adult patients (18 years and older) for whom continuous ambulatory ECG recording is clinically indicated, including patients with suspected arrhythmia and patients in the post-event surveillance window following a documented cardiac event. The device is used in home and outpatient clinical settings; it is not intended for in-patient acute monitoring or for use during invasive cardiac procedures.

## Edges

`supports` the ICP pillar — the IFU is the regulatory expression of the ICP we have chosen to serve.

## Notes

This IFU is intentionally narrower than CardioTrace's expanded IFU (`indication-for-use-cardiotrace-pro-2025-q3`). Narrow IFU + later targeted expansion is a deliberate regulatory strategy; see the founder-vision source for rationale.
