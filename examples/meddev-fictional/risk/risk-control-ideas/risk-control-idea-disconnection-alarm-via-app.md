---
id: risk-control-idea-disconnection-alarm-via-app
title: "Risk Control Idea: Disconnection Alarm via Clinician App"
type: risk-control-idea
namespace: risk-planning
summary: "Use impedance monitoring + signal-quality assessment to detect pad detachment in real-time; surface an alert to the clinician app and a daily check-in to the patient."
auto_inject: false
applicable_when: null
confidence: 0.7
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Update once technical feasibility is validated and a controlled risk control selection is made."
tags: [risk-control, candidate, app]
edges:
  - target: harm-missed-arrhythmia-event
    type: supports
    weight: 0.85
    note: "Targets prevention of this harm."
  - target: hazardous-situation-pad-falls-off-during-sleep
    type: supports
    weight: 0.85
    note: "Directly addresses this hazardous situation."
related: []
source_url: null
controlled_document: false
---

# Risk Control Idea: Disconnection Alarm via Clinician App

## Summary

A candidate mitigation: monitor pad-to-skin impedance and ECG signal quality on-device, detect a transition into "probably detached" state, and notify both the clinician app and the patient (via app or daily check-in) so the pad can be reseated or replaced.

## Content

This is a **candidate** mitigation. It is NOT yet selected, validated, or specified as a controlled risk control. It is here because the team is actively considering it.

Components if pursued:

- On-device signal-quality scoring (continuous).
- Impedance threshold detection.
- A latency budget for alarm escalation.
- A patient-facing daily check-in (because we cannot assume the patient will see a notification within hours).

Things that are unresolved:

- Acceptable false-alarm rate (too high and we train patients/clinicians to ignore alarms; too low and we miss events).
- Power budget (alarms compete with the 7-day battery requirement).

## Edges

`supports` the harm prevention and the hazardous-situation prevention — both are valid framings.

## Notes

A v2 of this control idea might involve a wearable LED or haptic. Not in scope for v1.
