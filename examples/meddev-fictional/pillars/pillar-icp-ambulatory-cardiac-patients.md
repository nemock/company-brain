---
id: pillar-icp-ambulatory-cardiac-patients
title: "ICP: Adult Ambulatory Cardiac Patients"
type: pillar
namespace: product-strategy
summary: "We serve adult cardiac patients in ambulatory settings during the 7- to 30-day window after a cardiac event or during arrhythmia workup."
auto_inject: true
applicable_when: "ICP, target market, audience, indication scope, patient population, who we serve, expansion, pediatric, geriatric, in-patient, home-health"
confidence: 0.9
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "If our Q1 2026 trial cohort shifts materially toward in-patient or post-procedure settings, this pillar needs review."
tags: [icp, strategy]
edges:
  - target: source-vision-saunders-2026-cardiac-workflow-thesis
    type: derived_from
    weight: 0.9
    note: "ICP derives directly from the founder's stated thesis on workflow-limited ambulatory cardiac monitoring."
  - target: pillar-no-pediatric-use
    type: related_to
    weight: 0.8
    note: "The non-pediatric pillar is the deliberate boundary of this ICP."
related: []
source_url: null
controlled_document: false
---

# ICP: Adult Ambulatory Cardiac Patients

## Summary

Vitalisens is built for adult cardiac patients (18+) in ambulatory settings during the recovery, workup, or surveillance window after a cardiac event or in the run-up to an electrophysiology workup. The product is not designed for in-patient acute use, surgical use, pediatric populations, or general-wellness consumers.

## Content

The fictional ICP is the adult cardiac patient whose physician needs continuous ambulatory ECG for diagnostic clarity but does not need (or want) the patient confined to a hospital monitoring environment. The patient is mobile, lives at home, manages their own pad replacements (with guidance), and benefits from a 7-day wearable that captures arrhythmic events between clinical visits.

This pillar rules in:

- 18+ adult patients.
- Ambulatory care (home, outpatient clinic, post-discharge).
- Arrhythmia evaluation, post-event surveillance, syncope workup.

This pillar rules out:

- Pediatric patients (see `pillar-no-pediatric-use`).
- ICU / in-patient acute monitoring.
- General-wellness or consumer fitness use.

## Edges

`derived_from` the founder-vision source captures *why* the ICP is shaped this way: the bottleneck in the ambulatory cardiac workflow is not measurement quality but measurement *continuity* and clinician-side workflow.

`related_to` the non-pediatric pillar makes the boundary visible during retrieval — any agent considering pediatric expansion should see both pillars together.

## Notes

Review trigger: a substantial shift in the trial cohort population, a strategic conversation about pediatric expansion, or a regulatory change that affects how MCT is classified.
