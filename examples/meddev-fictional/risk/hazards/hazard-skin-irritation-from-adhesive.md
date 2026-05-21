---
id: hazard-skin-irritation-from-adhesive
title: "Hazard: Skin Irritation from Pad Adhesive"
type: hazard
namespace: risk-planning
summary: "Adhesive material on the Vitalisens Pad can cause skin irritation, allergic response, or contact dermatitis in some patients."
auto_inject: false
applicable_when: null
confidence: 0.9
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Refresh if pad chemistry changes."
tags: [hazard, pad, skin]
edges:
  - target: hazardous-situation-pad-falls-off-during-sleep
    type: related_to
    weight: 0.4
    note: "Distinct but adjacent hazard chain."
  - target: harm-missed-arrhythmia-event
    type: related_to
    weight: 0.3
    note: "Indirect link — irritation can cause patient to remove the pad, which can lead to missed events."
  - target: question-second-pad-formulation-for-sensitive-skin
    type: related_to
    weight: 0.7
    note: "Open question about a sensitive-skin formulation."
related: []
source_url: null
controlled_document: false
---

# Hazard: Skin Irritation from Pad Adhesive

## Summary

Adult patients wearing the Vitalisens Pad may experience skin irritation, allergic contact dermatitis, or other dermatologic reactions to the adhesive. Severity ranges from minor erythema to (rarely) blistering.

## Content

In ISO 14971 terms, the hazard is the chemical / mechanical interaction of the adhesive with patient skin. This node captures the planning-level identification of the hazard; the QMS-side risk management file would establish formal probability, severity, and risk control selections.

Known contributing factors (per planning thinking):

- Extended wear time (7 days is at the upper bound of typical adhesive tolerance).
- Skin sensitivity variation across the patient population.
- Pad orientation that places adhesive on areas of higher skin shear stress.

## Edges

`related_to` the question about a sensitive-skin pad formulation makes the planning loop visible.

## Notes

`controlled_document: false`. This is NOT a hazard entry from a risk management file. The risk management file is a separate, controlled record. This node informs the *thinking* that would feed that file, not the file itself.
