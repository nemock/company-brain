---
id: use-case-quarterly-board-prep
title: "Use Case: Quarterly Board Prep"
type: use-case
namespace: product
summary: "VPE assembles engineering velocity story for the board with Loftwing as the data source; target time under 1 hour, down from the typical 4–6."
auto_inject: false
applicable_when: null
confidence: 0.85
verified_at: 2026-03-11
verified_by: nemock
staleness_signal: "Validate with customer-reported time savings in Q2 2026."
tags: [use-case, board-prep]
edges:
  - target: concept-board-prep-workflow
    type: related_to
    weight: 0.95
    note: "This use case operationalises the board-prep workflow concept."
  - target: feature-team-cycle-time-dashboard
    type: depends_on
    weight: 0.85
    note: "The flagship dashboard is the primary surface for this use case."
related: []
source_url: null
controlled_document: false
---

# Use Case: Quarterly Board Prep

## Summary

The use case that drove the product's existence.

## Flow

1. **Day before board** — VPE opens Loftwing dashboard. Reads team-level cycle time, deploy frequency, planning accuracy for the trailing quarter.
2. **Annotates** — adds a one-line context note per team for anything anomalous.
3. **Exports a screenshot** of the dashboard with annotations.
4. **Drops the screenshot into the board deck** as a single page titled "Engineering velocity, Qx 2026."

In v1 the export is a manual screenshot. v2 ships a board-pack export as the Loftwing Boards product.

## Success criterion

Under 1 hour, end to end, by end of Q2 2026 for any team on the Team or Scale tier.
