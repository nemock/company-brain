---
id: hazardous-situation-pad-falls-off-during-sleep
title: "Hazardous Situation: Pad Detaches During Sleep, Patient Unaware"
type: hazardous-situation
namespace: risk-planning
summary: "Pad detaches partially or fully while the patient sleeps; the patient is unaware until morning; data is missing or degraded for that window."
auto_inject: false
applicable_when: null
confidence: 0.8
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Refresh if pad failure data changes materially."
tags: [hazardous-situation, pad]
edges:
  - target: harm-missed-arrhythmia-event
    type: related_to
    weight: 0.85
    note: "Hazardous situation can lead to this harm."
  - target: risk-control-idea-disconnection-alarm-via-app
    type: related_to
    weight: 0.8
    note: "Candidate mitigation."
  - target: pattern-pad-adhesion-failure-precedes-data-dropout
    type: derived_from
    weight: 0.7
    note: "Pattern provides the evidence base for this hazardous situation."
related: []
source_url: null
controlled_document: false
---

# Hazardous Situation: Pad Detaches During Sleep, Patient Unaware

## Summary

A pad lifts or detaches partially during patient sleep. The patient does not notice. The device may continue to produce signal that appears valid but is materially degraded. The window of impaired monitoring can extend for hours.

## Content

The hazardous-situation framing (ISO 14971) is: the **situation** under which the hazard (skin irritation, signal loss, etc.) could lead to a **harm** (missed arrhythmia event). This node names that situation in plain language for planning use.

Plausibility:

- Patient body movement during sleep can produce shear forces that exceed adhesive tolerance.
- Patient sweat or moisture during sleep affects adhesion.
- Patient cannot self-monitor while asleep.

## Edges

The `related_to` edge to `harm-missed-arrhythmia-event` makes the hazard chain visible: hazardous situation → harm.

## Notes

Not a controlled risk record. The QMS-side hazard analysis would formally classify and assign mitigations. Here we capture the thinking.
