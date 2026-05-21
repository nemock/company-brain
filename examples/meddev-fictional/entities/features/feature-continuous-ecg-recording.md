---
id: feature-continuous-ecg-recording
title: "Feature: Continuous Dual-Channel ECG Recording"
type: feature
namespace: features
summary: "Vitalisens Cardio continuously records dual-channel ECG throughout the monitoring window, with motion artifact rejection via accelerometer."
auto_inject: false
applicable_when: null
confidence: 0.85
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Revisit if sensor configuration changes or if sampling rate is altered."
tags: [feature, sensor]
edges:
  - target: requirement-mkt-001-continuous-ecg-during-ambulatory
    type: supports
    weight: 0.9
    note: "Feature implements the market requirement."
  - target: product-vitalisens-cardio
    type: part_of
    weight: 1.0
    note: "Feature lives in the wearable."
related: []
source_url: null
controlled_document: false
---

# Feature: Continuous Dual-Channel ECG Recording

## Summary

Continuous dual-channel ECG capture for the full 7-day pad cycle, with on-device motion artifact rejection via accelerometer-driven filtering.

## Content

Behavioral spec:

- Dual-channel (modified lead I + modified lead II equivalent through the pad's two-electrode placement).
- Continuous from pad attach through pad removal.
- On-device motion artifact rejection; raw signal preserved alongside cleaned signal for clinician review.
- Periodic upload to the clinician app over BLE.

## Edges

`supports` the market requirement; `part_of` the wearable product.

## Notes

The clinician-app side of this — visualization, arrhythmia alarms, EHR push — is a separate feature node that has not been written yet. Flag if it becomes a referenced topic.
