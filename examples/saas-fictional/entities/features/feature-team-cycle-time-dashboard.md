---
id: feature-team-cycle-time-dashboard
title: "Feature: Team-Level Cycle Time Dashboard"
type: feature
namespace: product
summary: "The flagship dashboard view: per-team cycle time over time, plus a 4-week trailing average and a comparison to the team's own historical baseline."
auto_inject: false
applicable_when: null
confidence: 0.9
verified_at: 2026-02-15
verified_by: nemock
staleness_signal: "Revisit after Q2 2026 customer usage patterns are in."
tags: [feature, dashboard]
edges:
  - target: product-loftwing-insights
    type: part_of
    weight: 1.0
    note: "Core feature of Loftwing Insights v1."
  - target: concept-cycle-time
    type: related_to
    weight: 0.9
    note: "The feature implements this concept."
related: []
source_url: null
controlled_document: false
---

# Feature: Team-Level Cycle Time Dashboard

## Summary

The flagship dashboard view.

## What it does

- One row per team, with cycle time as the primary number.
- Sparkline showing 12 weeks of trend.
- Comparison line: the team's own 12-week trailing baseline.
- No per-developer breakdown (see [`pillar-no-developer-surveillance`](../../pillars/pillar-no-developer-surveillance.md)).

## Why this is the flagship

If a customer evaluates Loftwing in 30 seconds, this is the screen they evaluate. The team-level rollup + baseline comparison is the "story" we promised the VPE could take to the board.
