---
id: harm-missed-arrhythmia-event
title: "Harm: Missed Arrhythmia Event"
type: harm
namespace: risk-planning
summary: "Clinically significant arrhythmia occurs during a window when the device is failing to capture usable data; the event is not detected and the clinician cannot act."
auto_inject: false
applicable_when: null
confidence: 0.9
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Refresh if clinical importance of detection windows changes."
tags: [harm, clinical]
edges:
  - target: risk-control-idea-disconnection-alarm-via-app
    type: related_to
    weight: 0.85
    note: "Risk control idea targeting this harm."
related: []
source_url: null
controlled_document: false
---

# Harm: Missed Arrhythmia Event

## Summary

The clinically significant harm the device exists to prevent: an arrhythmic event happens while the device is the patient's primary monitoring tool, and the event is not detected because the device is failing.

## Content

In ISO 14971 vocabulary, this is the *harm* — the downstream clinical consequence — that the system of hazards and hazardous situations ultimately produces. For an MCT device, missed-event harm has both:

- A direct clinical component (the patient may not get appropriate care for a real arrhythmia).
- A diagnostic-confidence component (the monitoring window's negative findings are unreliable, requiring repeat monitoring).

## Edges

Targeted by `risk-control-idea-disconnection-alarm-via-app`, which is the candidate mitigation under consideration.

## Notes

This node names the harm so the planning team can talk about it without ambiguity. It is not a controlled hazard analysis entry; that lives in the (yet-to-be-created) risk management file.
