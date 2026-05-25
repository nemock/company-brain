---
id: metric-weekly-active-teams
title: "Metric: Weekly Active Teams"
type: metric
namespace: product-metrics
summary: "Count of distinct paying customer workspaces that loaded a Loftwing dashboard at least once in a 7-day window."
auto_inject: false
applicable_when: null
confidence: 0.9
verified_at: 2026-04-08
verified_by: nemock
staleness_signal: "Definition is stable; volatility drives snapshot decay."
tags: [metric, product, activation]
volatility_class: high
edges: []
related: []
source_url: null
controlled_document: false
---

# Metric: Weekly Active Teams

## Summary

Distinct paying workspaces active in a 7-day window.

## Definition

Weekly active teams = count of distinct workspaces (per [`decision-003`](../../decisions/decision-003-workspace-pricing-not-seat-based.md), workspace = company) that loaded a Loftwing dashboard at least once in a rolling 7-day window. Workspaces in trial are excluded.

## Why volatility = high

Weekly numbers can shift visibly week-to-week with marketing pushes, product changes, or even calendar effects (e.g., engineering teams off in late December). A two-month-old snapshot is essentially historical; treat it as such.
