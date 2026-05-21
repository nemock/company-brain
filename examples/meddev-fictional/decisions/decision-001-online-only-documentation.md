---
id: decision-001-online-only-documentation
title: "Decision 001: Online-Only Documentation"
type: decision
namespace: operations
summary: "All Vitalisens documentation (IFU, user manual, quick-start, clinician guide) is electronic only. No printed inserts ship with any product."
auto_inject: false
applicable_when: null
confidence: 0.92
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Revisit if a notified body or FDA guidance moves against electronic-only IFU for our device class, or if a procurement-blocking customer demand emerges."
tags: [decision, documentation, operations]
edges:
  - target: pillar-no-physical-documentation
    type: supports
    weight: 0.95
    note: "Concrete operational expression of the non-goal pillar."
  - target: requirement-mkt-001-continuous-ecg-during-ambulatory
    type: related_to
    weight: 0.4
    note: "Documentation strategy must keep pace with the indicated use."
related: []
source_url: null
controlled_document: false
---

# Decision 001: Online-Only Documentation

## Summary

We will not print any of the user-facing or clinician-facing documentation that ships with Vitalisens. All documentation lives at a stable HTTPS URL, versioned in lockstep with device software, and reachable from the device packaging via a printed QR code.

## Alternatives Considered

1. **Status quo print + electronic**: ship a printed IFU and an electronic copy. Rejected because it doubles the rev-control burden and creates a version-drift risk that we cannot eliminate.
2. **Print quick-start only, electronic everything else**: rejected because even a one-page quick-start enters the controlled-documentation system and forces a print run on every change.
3. **No documentation at all on packaging**: rejected for obvious regulatory and user-experience reasons.
4. **Online-only with packaging QR code**: chosen.

## Decision

Adopt option 4. The packaging carries a single QR code linking to the canonical documentation portal. Device firmware updates publish documentation revisions to the same portal so that the live IFU and the in-field firmware are always reachable from the same URL.

## Rationale

- Eliminates print-run version drift.
- Aligns documentation change control with software change control.
- Reduces packaging waste and supports the no-physical-documentation pillar.
- Permits accessibility features (screen reader, translation, large-print mode) that printed documentation cannot offer.

## What This Rules Out

- **Printed IFU inserts.** The IFU is not printed at any point in the supply chain.
- **Printed quick-start cards.** No "getting started" cards ship in the box.
- **Printed user manuals.** No paper manuals are distributed.
- **Distributor-printed collateral.** Distributors are contractually prohibited from generating their own printed versions of the IFU or user manual.
- **PDF-by-email as the documentation distribution channel.** Documentation must live at a stable URL, not be emailed.

## Edges

The `supports` edge into `pillar-no-physical-documentation` makes this decision the operational version of the pillar.

## Notes

Open implementation items: which QR-code provider to use, what the URL pattern looks like (`vitalisens.example.com/ifu/<sku>/<rev>`), and whether the QR can survive humidity / cleaning agents in clinical environments. None of those affect the decision; they are execution details.
