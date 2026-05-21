---
id: standard-iso-14971-risk-management
title: "Standard: ISO 14971 (Risk Management)"
type: standard
namespace: regulatory-references
summary: "International standard for risk management of medical devices. Vitalisens uses its vocabulary for planning-level risk thinking; the controlled risk management file would also conform."
auto_inject: false
applicable_when: null
confidence: 1.0
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Update when a new edition publishes."
tags: [standard, iso, risk]
edges: []
related: []
source_url: "https://www.iso.org/standard/72704.html"
controlled_document: false
---

# Standard: ISO 14971 (Risk Management)

## Summary

ISO 14971 is the international standard for applying risk management to medical devices. Vitalisens uses its vocabulary (hazard, hazardous situation, harm, risk control) throughout the `risk/` folder. The controlled risk management file (a separate artifact) would also conform to ISO 14971.

## Content

Why this node exists in the vault:

- Several risk-family nodes use ISO 14971 vocabulary; pointing at the source standard makes that explicit.
- A query like "what regulatory standards do we conform to?" should find this node.

This node is a *reference* — Vitalisens does not author the standard, only consumes it.

## Notes

`controlled_document: false` is technically redundant for a standards reference (the standard itself is a controlled document by ISO, not by Vitalisens) but the field is set defensively to signal that this node is not part of Vitalisens' QMS records.
