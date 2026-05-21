---
id: pillar-no-pediatric-use
title: "Non-Goal: We Do Not Pursue Pediatric Use"
type: pillar
namespace: product-strategy
summary: "Vitalisens will not pursue indications, labeling, marketing, or clinical claims for pediatric patients (under 18) in v1 or v2 of the product."
auto_inject: true
applicable_when: "pediatric, child, children, adolescent, under-18, school-age, infant, neonatal, age-restricted indication, IFU expansion to younger populations"
confidence: 0.9
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Reconsider if (a) a strategic partnership with a pediatric cardiology center makes pediatric clinical data tractable, OR (b) reimbursement for pediatric ambulatory monitoring becomes materially more favorable than adult."
tags: [non-goal, strategy, scope]
edges:
  - target: pillar-icp-ambulatory-cardiac-patients
    type: supports
    weight: 0.9
    note: "Negative framing that sharpens the ICP boundary."
  - target: question-when-to-pursue-pediatric-clearance
    type: related_to
    weight: 0.7
    note: "The open question about *when* this non-goal might flip."
related: []
source_url: null
controlled_document: false
---

# Non-Goal: We Do Not Pursue Pediatric Use

## Summary

Pediatric ambulatory cardiac monitoring is a real clinical need served by other devices. Vitalisens does not pursue it. This is a deliberate boundary, not an oversight.

## Content

A pediatric indication would require:

- A separate clinical study cohort.
- Pad chemistry validation against pediatric skin (more sensitive, smaller surface area).
- Adjusted ECG-channel configuration to account for smaller anatomy.
- A separate regulatory pathway (510(k) with pediatric labeling, or a De Novo for novel pediatric claims).
- A separate sales and reimbursement motion.

Pursuing this in v1 or v2 would dilute focus and delay clearance. Pediatric is not "harder" than adult; it is a different product with its own clinical, regulatory, and commercial work.

This pillar rules out:

- IFU language referencing pediatric populations.
- Marketing claims directed at children, parents, or pediatric clinicians.
- Pad variants intended for pediatric skin.
- Clinical studies enrolling under-18 patients to evaluate Vitalisens.

This pillar does NOT rule out:

- A future v3+ pediatric program if the open question (see `question-when-to-pursue-pediatric-clearance`) resolves in favor.
- Off-label use observation; we simply do not pursue it, label for it, or market it.

## Edges

The `supports` edge into the ICP pillar makes the negative framing legible to any agent reasoning about scope.

The `related_to` edge into the open question is intentional — this pillar should not feel like a final answer. It is a current operating commitment that might flip on specific evidence.

## Notes

This is a textbook **non-goal pillar**: a pillar written in negative form, with an `auto_inject: true` that fires when pediatric topics come up. Any agent answering a pediatric-related question should retrieve this pillar early in Phase 1 and surface the boundary.
