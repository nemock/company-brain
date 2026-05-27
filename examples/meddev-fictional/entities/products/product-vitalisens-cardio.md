---
id: product-vitalisens-cardio
title: "Vitalisens Cardio"
type: product
namespace: products
summary: "Adult ambulatory cardiac telemetry wearable; continuous ECG capture, Bluetooth uplink to clinician app, 7-day pad cycle."
auto_inject: false
applicable_when: null
primary: true
confidence: 0.9
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Revisit when the device firmware ships v1.0 or the form factor changes."
tags: [product, wearable]
edges:
  - target: product-line-vitalisens-cardiac-monitoring
    type: part_of
    weight: 1.0
    note: "Belongs to the cardiac-monitoring product line."
  - target: product-vitalisens-pad
    type: depends_on
    weight: 1.0
    note: "Wearable cannot operate without the pad."
  - target: indication-for-use-vitalisens-cardio-2026-q1
    type: related_to
    weight: 0.9
    note: "Current IFU for this product."
  - target: regulatory-clearance-K243189-vitalisens-cardio
    type: related_to
    weight: 0.9
    note: "Planned 510(k) clearance."
related: []
source_url: null
controlled_document: false
---

# Vitalisens Cardio

## Summary

The Vitalisens wearable. It captures continuous ECG via two leads, transmits to a paired clinician application over Bluetooth, and is designed to operate continuously through a 7-day pad cycle. One wearable serves many monitoring episodes; the pad turns over each week.

## Content

In v1:

- Form factor: chest patch, lightweight, low-profile.
- Sensors: dual-channel ECG, accelerometer for motion artifact rejection.
- Connectivity: Bluetooth Low Energy to a paired smartphone or in-home gateway.
- Battery: ≥ 7 days continuous operation (validated against `requirement-sys-001-7-day-battery`).
- Charging: inductive charging cradle.
- Pad coupling: snap-fit interface; pad changes do not require recharging.

The wearable is dispensed by a prescribing clinic (Rx-only — see `decision-002-prescription-only-not-otc`).

## Edges

`depends_on` the pad is a literal product dependency, not a workflow nicety. Without a viable pad, the wearable cannot acquire signal.

## Notes

v2 candidates (not in scope for v1): additional sensors (SpO2, respiration), alternative form factors, longer-life battery for in-patient bridge use.
