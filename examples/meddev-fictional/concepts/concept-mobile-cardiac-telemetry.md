---
id: concept-mobile-cardiac-telemetry
title: "Concept: Mobile Cardiac Telemetry (MCT)"
type: concept
namespace: domain
summary: "MCT is continuous outpatient ECG monitoring with real-time or near-real-time transmission to a monitoring service that reviews and escalates clinically significant findings."
auto_inject: false
applicable_when: null
confidence: 0.95
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Update if clinical or regulatory definition shifts."
tags: [concept, domain]
edges: []
related: []
source_url: null
controlled_document: false
---

# Concept: Mobile Cardiac Telemetry (MCT)

## Summary

Mobile Cardiac Telemetry (MCT) is the regulatory and clinical category for continuous outpatient ECG monitoring with transmission to a reviewing service. Distinct from Holter monitoring (no transmission, retrospective review) and event monitoring (patient-triggered capture).

## Content

Why this concept node exists: many of our pillars, decisions, and competitor analyses use "MCT" as shorthand. Having a concept node anchors the term so an agent does not have to infer it.

Key distinctions:

- **MCT**: continuous capture + transmission + review service. Real-time or near-real-time.
- **Holter monitor**: continuous capture, no transmission, retrospective review.
- **Event monitor / loop recorder**: intermittent capture, often patient-triggered.

Vitalisens Cardio is positioned as an MCT device.

## Notes

A useful query test: "what's the difference between MCT and Holter?" should retrieve this node.
