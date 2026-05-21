---
id: requirement-sys-001-7-day-battery
title: "System Requirement: 7-Day Continuous Battery Life"
type: requirement
namespace: requirements
summary: "Vitalisens Cardio must operate for at least 7 days of continuous use between recharges under nominal conditions."
auto_inject: false
applicable_when: null
confidence: 0.92
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Revisit if pad wear time changes or if sensor sampling rate is altered."
tags: [requirement, system]
requirement_class: system
edges:
  - target: decision-003-7-day-wear-not-14-day
    type: derived_from
    weight: 0.9
    note: "Battery life requirement is set by the pad wear-time decision."
  - target: product-vitalisens-cardio
    type: related_to
    weight: 0.9
    note: "Requirement applies to this product."
related: []
source_url: null
controlled_document: false
---

# System Requirement: 7-Day Continuous Battery Life

## Summary

The Vitalisens Cardio wearable must operate for at least seven days of continuous ECG capture and Bluetooth uplink under nominal use, between recharges. The number is set by the pad wear-time decision, not chosen independently.

## Content

Specific system parameters:

- Continuous dual-channel ECG sampling at the labeled rate.
- Periodic Bluetooth uplink at the labeled cadence.
- Accelerometer sampling for motion artifact rejection.
- Ambient temperature range per typical clinical / home use.

Below 7 days, patient experience suffers (recharge becomes another point of failure). Above 7 days, the battery is over-spec'd for the pad-bounded use case.

## Edges

`derived_from` the wear-time decision is the actual dependency direction — battery life is downstream of the pad-change cadence we committed to.

## Notes

`requirement_class: system` is mandatory. This requirement is *not* a controlled design input — if it ever entered a DHF, it would be re-authored under controlled change management. It is captured here for planning legibility.
