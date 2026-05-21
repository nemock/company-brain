---
id: risk-insight-pad-adhesion-failure-affects-data-quality
title: "Risk Insight: Pad Adhesion Failure Cascades into Data-Quality Failure"
type: risk-insight
namespace: risk-planning
summary: "Pad adhesion failure does not just lose signal — it tends to fail silently, producing noisy data that looks plausible. Detection matters as much as prevention."
auto_inject: false
applicable_when: null
confidence: 0.85
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Update after each major pad chemistry or sensor-firmware change."
tags: [risk, planning, pad]
edges:
  - target: hazard-skin-irritation-from-adhesive
    type: related_to
    weight: 0.5
    note: "Related but distinct concern."
  - target: pattern-pad-adhesion-failure-precedes-data-dropout
    type: derived_from
    weight: 0.85
    note: "Pattern is the evidence; this risk-insight is the planning implication."
related: []
source_url: null
controlled_document: false
---

# Risk Insight: Pad Adhesion Failure Cascades into Data-Quality Failure

## Summary

A partially-detached pad still produces signal — but the signal is degraded in ways the patient and clinician may not catch in real time. This is a planning-level observation, not a controlled risk record.

## Content

What the team should think about, but not yet operationalize as a controlled risk record:

- A pad that has lifted on one electrode but not the other produces single-channel data that the device may interpret as valid.
- Without an active disconnection alarm, neither patient nor clinician knows the data has degraded.
- The clinical impact is missed events — arrhythmias the device should have caught.
- Mitigations probably include both detection (impedance monitoring, signal-quality alarms) and prevention (pad design, application coaching).

## Edges

`derived_from` the pattern node — the risk-insight is the planning implication, the pattern is the observational base.

## Notes

This is a textbook **risk-insight** node: a planning observation, framed in ISO-14971-adjacent language but explicitly NOT a controlled record. The QMS-side risk management file would re-author this and assign formal severity / probability scores. Here, it captures the team's thinking without crossing the controlled-document boundary.
