---
id: requirement-mkt-001-continuous-ecg-during-ambulatory
title: "Market Requirement: Continuous ECG During Ambulatory Use"
type: requirement
namespace: requirements
summary: "Cardiologists need continuous (not intermittent) ECG capture during the ambulatory window; intermittent recording misses paroxysmal events."
auto_inject: false
applicable_when: null
confidence: 0.9
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Reconsider if a new clinical guideline accepts intermittent ambulatory ECG for arrhythmia evaluation."
tags: [requirement, market]
requirement_class: market
edges:
  - target: source-customer-interview-2026-04-12-nurse-anderson
    type: derived_from
    weight: 0.6
    note: "Customer interview informed the requirement."
  - target: source-citation-aha-mct-guidelines-2024
    type: derived_from
    weight: 0.9
    note: "Clinical guideline establishes continuous capture as standard of care."
  - target: feature-continuous-ecg-recording
    type: related_to
    weight: 0.9
    note: "Implementing feature."
related: []
source_url: null
controlled_document: false
---

# Market Requirement: Continuous ECG During Ambulatory Use

## Summary

The cardiology market expects continuous, not intermittent, ECG capture during the monitoring window. Intermittent loop recorders miss paroxysmal events that occur outside their windows.

## Content

This is a market requirement, **not** a controlled design input. It captures what cardiologists already expect and what clinical guidelines call for. The implementing system requirement and feature live elsewhere; this node exists to make the *why* legible.

Sources establishing this requirement:

- The 2024 AHA clinical guideline citation for ambulatory MCT.
- The customer-interview source where the nurse-coordinator described case examples of intermittent-monitor failures.

## Edges

This is a textbook example of a requirement traced to two sources. The validator should see both `derived_from` edges.

## Notes

The `requirement_class: market` field is mandatory per the schema. Do not flip this to `user` or `system` without re-examining the content — those have different controlled-documentation implications downstream.
