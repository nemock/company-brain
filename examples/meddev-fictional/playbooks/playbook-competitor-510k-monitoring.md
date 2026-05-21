---
id: playbook-competitor-510k-monitoring
title: "Playbook: Quarterly Competitor 510(k) Monitoring"
type: playbook
namespace: competitive
summary: "Every quarter, scan FDA 510(k) clearances in the relevant product codes for new filings by tracked competitors; capture as regulatory-clearance + source nodes."
auto_inject: false
applicable_when: null
confidence: 0.8
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Refresh after any tooling or process change."
tags: [playbook, competitive, regulatory]
edges:
  - target: competitor-cardiotrace-inc
    type: related_to
    weight: 0.7
    note: "One of the tracked competitors."
  - target: competitor-pulseguard-medical
    type: related_to
    weight: 0.7
    note: "One of the tracked competitors."
related: []
source_url: null
controlled_document: false
---

# Playbook: Quarterly Competitor 510(k) Monitoring

## Summary

A repeatable quarterly cadence for scanning FDA 510(k) clearances for new filings by tracked competitors and any new entrants in the MCT product codes.

## When to Run

Once per quarter. Trigger: first business day of the calendar quarter.

## Steps

1. **Search openFDA for new clearances** in product code DRT (and any adjacent codes) filed in the previous quarter.
2. **Filter to competitors of interest** (current list: CardioTrace, PulseGuard, plus any new entrants).
3. **For each new clearance**:
   - Create a `regulatory-clearance` node with the standard fields.
   - Create a `source` node of `source_kind: fda-510k-summary` for the PDF.
   - If the filer is a known competitor, link to the existing `competitor` node.
   - If the filer is new, create a `competitor` node and add to the tracking list.
4. **For each affected competitor**, check the product page for IFU changes:
   - Capture a `web-snapshot` source.
   - If the IFU changed, create a new `indication-for-use` node and chain it `preceded_by` the prior IFU.
5. **Surface in the next leadership review**: flag any clearance that meaningfully changes the competitive landscape (new entrant in DRT, IFU expansion that pressures our positioning, new predicate that we should consider citing).

## Owner

Regulatory lead (in v1.x, the openFDA integration may automate steps 1-3).

## Edges

Links to the currently tracked competitors so it is discoverable when reviewing the competitive archive.

## Notes

v1.x will introduce `cb intake-510k <K-number>` which automates the structured-data ingestion side of step 3.
