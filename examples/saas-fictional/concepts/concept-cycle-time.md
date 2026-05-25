---
id: concept-cycle-time
title: "Concept: Cycle Time (DORA)"
type: concept
namespace: glossary
summary: "Cycle time = the elapsed time from a code commit to that commit running in production. One of the four DORA metrics popularized by Accelerate."
auto_inject: false
applicable_when: null
confidence: 0.95
verified_at: 2026-01-30
verified_by: nemock
staleness_signal: "Definition is stable; the canonical DORA framing has not changed since Accelerate."
tags: [concept, dora, metric-definition]
edges:
  - target: source-citation-accelerate-book
    type: derived_from
    weight: 0.9
    note: "Definition is the one from Accelerate."
related: []
source_url: null
controlled_document: false
---

# Concept: Cycle Time (DORA)

## Summary

The DORA cycle-time metric: elapsed time from commit to production.

## Definition

Cycle time = the elapsed time between a code commit landing in the main branch and that commit running in production. Measured at the team level (per the team-level-signal pillar), not at the individual-developer level.

## Why we surface it

Cycle time is the most legible engineering velocity metric for a non-technical board reviewer. It is a single number with a clear unit (days, hours), and the direction of "better" is intuitive (smaller is better, with caveats).

## What cycle time is NOT

Cycle time is not "how productive an individual developer is." See [`pillar-no-developer-surveillance`](../pillars/pillar-no-developer-surveillance.md).
