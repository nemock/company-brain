---
id: pillar-no-physical-documentation
title: "Non-Goal: No Physical Documentation"
type: pillar
namespace: product-strategy
summary: "Vitalisens does not produce printed IFU, printed quick-start cards, printed user manuals, or printed in-box collateral. All documentation is online."
auto_inject: true
applicable_when: "documentation, IFU, user manual, quick start, in-box, packaging insert, printed insert, leaflet, instructions for use printing, e-IFU, electronic instructions for use, paper documentation"
confidence: 0.9
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Reconsider if (a) FDA or notified-body guidance moves against electronic-only IFU for our device class, OR (b) a large customer's procurement process refuses to onboard without printed materials."
tags: [non-goal, operations, documentation]
edges:
  - target: decision-001-online-only-documentation
    type: supports
    weight: 0.9
    note: "Specific decision that operationalizes this pillar."
  - target: source-vision-saunders-2026-cardiac-workflow-thesis
    type: derived_from
    weight: 0.7
    note: "Online-only documentation is part of the workflow-first thesis."
related: []
source_url: null
controlled_document: false
---

# Non-Goal: No Physical Documentation

## Summary

Vitalisens ships no printed documentation. The IFU, user manual, quick-start, and clinician guide are all electronic, hosted at a stable URL, and accessible from the device packaging via QR code.

## Content

The choice is deliberate. Printed documentation has known failure modes:

- It is out of date the moment it ships.
- It is hard to keep aligned with the live IFU.
- It is wasteful — most users discard it without reading.
- It is a controlled-document liability — every revision is a print run.

Electronic-only documentation lets us:

- Update the IFU and clinician guide on a single source-of-truth path.
- Version, audit, and rev-control the documentation in a way that aligns with the device-software change process.
- Reduce in-box waste.

This pillar rules out:

- Printed IFU inserts.
- Printed quick-start cards or "getting started" booklets.
- Any marketing collateral that lives only on paper.

This pillar does NOT rule out:

- A QR code on the device or packaging that links to the IFU.
- A clinician-facing one-pager that can be printed by the clinic if they choose.
- Plain-text accessible versions of all electronic documentation.

## Edges

Operationalized by `decision-001-online-only-documentation`, which captures the specific rules-out language for the team building the documentation system.

## Notes

This is the second **non-goal pillar** in the vault. It demonstrates that non-goals can be tactical (this one) as well as strategic (`pillar-no-pediatric-use`). Both ride the same auto-inject pattern.
