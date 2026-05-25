---
id: hypothesis-dashboard-url-shared-in-slack-predicts-retention
title: "Hypothesis: Dashboard URL Shared in Slack Within 7 Days Predicts 90-Day Retention"
type: hypothesis
namespace: activation
summary: "Teams whose VPE shares the Loftwing dashboard URL in their team's Slack within the first 7 days will retain at 90 days at materially higher rates."
auto_inject: false
applicable_when: null
confidence: 0.55
verified_at: 2026-04-09
verified_by: nemock
staleness_signal: "Falsified if Q1 + Q2 2026 cohorts show no statistical difference between Slack-shared and not-Slack-shared trials at the 90-day mark."
tags: [hypothesis, activation, retention]
edges:
  - target: pattern-engaged-vpes-share-dashboard-url-early
    type: related_to
    weight: 0.85
    note: "The hypothesis tries to predict an outcome from the pattern."
related: []
source_url: null
controlled_document: false
---

# Hypothesis: Dashboard URL Shared in Slack Within 7 Days Predicts 90-Day Retention

## Summary

Behavioral signal we think predicts retention; deserves a real cohort study.

## Hypothesis statement

If a VPE pastes their Loftwing dashboard URL into the team's Slack (or any team channel) within the first 7 days of signup, then that team's 90-day retention will exceed the baseline by at least 20 percentage points.

## Why we believe this

The observed pattern (see [pattern-engaged-vpes-share-dashboard-url-early](../patterns/pattern-engaged-vpes-share-dashboard-url-early.md)) is suggestive: every VPE we interviewed who ended up retaining had shared the URL early. The mechanism is plausible — sharing the URL is the act that recruits the team into the data conversation, which is the activation that retains.

## Falsification condition

If the Q1 + Q2 2026 cohorts show no statistical difference between Slack-shared and not-Slack-shared groups at 90 days, this hypothesis is falsified and the pattern is just a correlation with no causal weight.

## What this hypothesis is NOT

We are NOT measuring whether sharing the URL *causes* retention. We are testing whether the behavior is a useful early signal we can intervene on (e.g., by prompting an explicit Slack share at day 3).
