---
id: requirement-mkt-001-board-legible-velocity-story
title: "Market Requirement: Board-Legible Engineering Velocity Story"
type: requirement
namespace: requirements
summary: "The product must let a VPE assemble a one-screen engineering-velocity story that a non-technical board reviewer can read in under 2 minutes."
auto_inject: false
applicable_when: null
confidence: 0.9
verified_at: 2026-02-04
verified_by: nemock
staleness_signal: "Validate after Q2 2026 customer feedback on dashboard comprehensibility."
tags: [requirement, market]
requirement_class: market
edges:
  - target: pillar-icp-vpe-scaling-saas
    type: supports
    weight: 0.85
    note: "Directly addresses the ICP's most-named pain."
  - target: use-case-quarterly-board-prep
    type: related_to
    weight: 0.95
    note: "This requirement enables the use case."
related: []
source_url: null
controlled_document: false
---

# Market Requirement: Board-Legible Engineering Velocity Story

## Summary

The product's market-class requirement.

## Statement

The product must enable a VPE to assemble, in under 5 minutes, a one-screen engineering-velocity story that a non-technical board reviewer can comprehend in under 2 minutes.

## Why class = market

This is a market requirement — it expresses what the market is willing to pay for. It is upstream of user requirements (what the user needs to do) and system requirements (what the system has to provide).

## Edges

`supports` the ICP pillar. `related_to` the use case that depends on this requirement.
