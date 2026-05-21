---
id: concept-predicate-device
title: "Concept: Predicate Device (510(k) Substantial Equivalence)"
type: concept
namespace: regulatory
summary: "A predicate device is a legally marketed device cited in a 510(k) submission to establish substantial equivalence. The predicate's IFU and technical characteristics anchor the submission's scope."
auto_inject: false
applicable_when: null
confidence: 1.0
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Update if FDA changes the 510(k) framework substantively."
tags: [concept, regulatory, 510k]
edges: []
related: []
source_url: "https://www.fda.gov/medical-devices/premarket-notification-510k/510k-submission-process"
controlled_document: false
---

# Concept: Predicate Device (510(k) Substantial Equivalence)

## Summary

In FDA 510(k) submissions, a *predicate device* is a legally marketed device the submitter cites to establish substantial equivalence. The new device's IFU, technical characteristics, and risk profile are compared against the predicate's; a successful 510(k) clears the new device for the predicate-comparable indications.

## Content

Why this concept matters in this vault:

- The competitive archive models predicate relationships as first-class `preceded_by` edges between `regulatory-clearance` nodes.
- Choosing predicates for our own filing (K243189, planned) is a strategic decision that affects clearance scope.

Predicate strategy is a real planning topic, not just a paperwork exercise. The IFU of our chosen predicates effectively bounds what we can claim.

## Notes

`controlled_document: false` even though this concept *describes* a controlled-documentation framework. The distinction: company-brain has a node about predicates; it does not contain predicate citations for any actual filing.
