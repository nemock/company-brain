---
id: customer-northstar-cardiology-2025
title: "Northstar Cardiology Group (trial customer)"
type: customer
namespace: customers
summary: "Fictional multi-site cardiology group; first trial customer; running a 14-patient pilot during Q1-Q2 2026."
auto_inject: false
applicable_when: null
confidence: 0.85
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Update after the trial closes or if site count changes."
tags: [customer, trial]
edges:
  - target: source-customer-interview-2026-04-12-nurse-anderson
    type: related_to
    weight: 0.8
    note: "Interview was with a care-team member at this customer."
  - target: source-internal-data-q1-2026-pad-attach-rate
    type: related_to
    weight: 0.7
    note: "Trial cohort metrics derive from this customer's data."
related: []
source_url: null
controlled_document: false
---

# Northstar Cardiology Group (trial customer)

## Summary

A fictional 3-site cardiology group in the upper Midwest serving roughly 4,000 cardiac patients annually. Our first paid pilot, beginning Q1 2026 with 14 enrolled patients in the cohort.

## Content

Site profile:

- 3 outpatient clinics, 1 EP lab.
- ~12 cardiologists, 4 EPs.
- Existing MCT vendor relationship (with CardioTrace). Vitalisens is being tested side-by-side.
- Program director (the named stakeholder) is the champion.

The trial is structured as a real-world performance assessment, not a regulatory clinical trial. Outcomes inform our trajectory toward 510(k) submission but are not part of the submission itself.

## Edges

Trial interactions feed the customer-interview source and the internal-data source. Both edges are `related_to` rather than `derived_from` because the data is multi-source — this customer is one input among several.

## Notes

Names are fictional. Any resemblance to a real cardiology group is coincidental.
