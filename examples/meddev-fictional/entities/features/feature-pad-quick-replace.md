---
id: feature-pad-quick-replace
title: "Feature: Pad Quick-Replace"
type: feature
namespace: features
summary: "Snap-fit pad interface with orientation cues and electronic step-by-step instructions; supports self-service replacement in under 5 minutes."
auto_inject: false
applicable_when: null
confidence: 0.8
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Revisit after the first 50 patient pad changes have been observed."
tags: [feature, ux, pad]
edges:
  - target: requirement-user-001-self-service-pad-replacement
    type: supports
    weight: 0.9
    note: "Feature implements the user requirement."
  - target: product-vitalisens-pad
    type: part_of
    weight: 1.0
    note: "The snap interface lives on the pad."
  - target: product-vitalisens-cardio
    type: part_of
    weight: 1.0
    note: "The receiving interface lives on the wearable."
related: []
source_url: null
controlled_document: false
---

# Feature: Pad Quick-Replace

## Summary

Snap-fit pad interface plus electronic step-by-step instructions in the clinician/patient app. Supports unaided pad replacement in under five minutes by an adult patient.

## Content

Components:

- Color-coded snap orientation on both the wearable and the pad.
- Backing peel-tab designed for one-handed removal.
- Clinician app guides the first replacement with photo-illustrated steps. Subsequent replacements default to a brief checklist.

## Edges

Two `part_of` edges because the feature spans both physical products — the pad provides the male side of the snap and the orientation cue; the wearable provides the female side and the app interaction. Modeling both edges keeps the feature's footprint clear.

## Notes

Future enhancement candidate: a haptic confirmation on the wearable when the pad seats properly. Tracked as a v2 idea, not yet captured as a node.
