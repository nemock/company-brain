---
id: feature-weekly-slack-digest
title: "Feature: Weekly Slack Digest"
type: feature
namespace: product
summary: "An opt-in weekly Slack digest summarising each team's cycle time, deploy frequency, and notable changes. Posted to a configured channel."
auto_inject: false
applicable_when: null
confidence: 0.85
verified_at: 2026-03-01
verified_by: nemock
staleness_signal: "Refine based on the open/click data the digest itself generates."
tags: [feature, slack, digest]
edges:
  - target: product-loftwing-insights
    type: part_of
    weight: 1.0
    note: "Bundled into the Team and Scale tiers of Loftwing Insights."
related: []
source_url: null
controlled_document: false
---

# Feature: Weekly Slack Digest

## Summary

Opt-in weekly summary posted to Slack.

## What it does

- Posts every Monday morning to a configured channel.
- One section per team.
- Numbers only, no per-developer breakout.
- Includes a deep link back to the Loftwing dashboard.

## Why it matters

The Slack digest is the artifact most likely to be shared upward by the VPE — see the [`pattern-engaged-vpes-share-dashboard-url-early`](../../patterns/pattern-engaged-vpes-share-dashboard-url-early.md) observation. Shipping a high-quality digest accelerates the very behavior we think predicts retention.
