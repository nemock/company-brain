---
id: requirement-user-001-self-service-pad-replacement
title: "User Requirement: Self-Service Pad Replacement"
type: requirement
namespace: requirements
summary: "Adult patients (or their caregiver) must be able to replace the pad at home without clinic intervention, within 5 minutes, using only the in-box instructions."
auto_inject: false
applicable_when: null
confidence: 0.88
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Refresh after each cohort's user-feedback round."
tags: [requirement, user]
requirement_class: user
edges:
  - target: pillar-disposable-pad-business-model
    type: supports
    weight: 0.8
    note: "Recurring pad model assumes self-service replacement."
  - target: feature-pad-quick-replace
    type: related_to
    weight: 0.9
    note: "Implementing feature."
  - target: source-customer-interview-2026-04-12-nurse-anderson
    type: derived_from
    weight: 0.7
    note: "User requirement validated against the trial cohort's feedback."
related: []
source_url: null
controlled_document: false
---

# User Requirement: Self-Service Pad Replacement

## Summary

The patient (or their at-home caregiver) must be able to replace the pad themselves without coming back to the clinic, in under five minutes, using only the in-box (electronic) instructions.

## Content

Specific user expectations:

- The pad must snap on with unambiguous orientation cues.
- The pad backing must release cleanly without contaminating the adhesive surface.
- The clinician app must guide first-time pad changes with photo-illustrated steps.
- A user who has done one pad change should not need to consult the app for subsequent changes.

This requirement makes the recurring-pad business model operationally viable. If pad changes required a clinic visit, the unit economics and the patient burden both collapse.

## Edges

`supports` into the pillar makes the dependency explicit: violate this requirement, undermine the pillar.

## Notes

`requirement_class: user` distinguishes this from market or system requirements. Different classes have different controlled-documentation lineage. company-brain treats all three as planning-level nodes; the QMS process would re-author this language into design inputs if it ever became part of a controlled record.
