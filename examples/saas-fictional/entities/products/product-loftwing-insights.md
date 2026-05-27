---
id: product-loftwing-insights
title: "Loftwing Insights"
type: product
namespace: products
summary: "The flagship product: a dashboard surface for VPEs that aggregates GitHub + Linear/Jira data into team-level cycle time, deploy frequency, and planning accuracy views."
auto_inject: false
applicable_when: null
primary: true
confidence: 0.9
verified_at: 2026-01-22
verified_by: nemock
staleness_signal: "Revisit when the v1 dashboard shape stabilises (target: end of Q2 2026)."
tags: [product, v1]
edges:
  - target: product-line-loftwing-platform
    type: part_of
    weight: 1.0
    note: "Sole product of the Loftwing Platform in v1."
related: []
source_url: null
controlled_document: false
---

# Loftwing Insights

## Summary

The v1 dashboard surface.

## What it does

- Connects to GitHub + one of {Linear, Jira} per [`decision-002`](../../decisions/decision-002-three-integrations-only-in-v1.md).
- Computes team-level cycle time, deployment frequency, sprint planning accuracy. Team is the smallest exposed unit per [`pillar-team-level-signal`](../../pillars/pillar-team-level-signal.md).
- Renders a single-screen dashboard the VPE can show to a non-technical reader.
- Pushes a weekly Slack digest at the team level (no per-person breakdown).

## What it doesn't do (in v1)

- No per-developer views (see [`pillar-no-developer-surveillance`](../../pillars/pillar-no-developer-surveillance.md)).
- No GitLab, Bitbucket, or Azure DevOps support (see [`decision-002`](../../decisions/decision-002-three-integrations-only-in-v1.md)).
- No board-export layer (that ships as Loftwing Boards in v2).

## Edges

`part_of` the Loftwing Platform product line.
