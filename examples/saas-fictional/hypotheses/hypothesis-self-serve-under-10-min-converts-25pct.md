---
id: hypothesis-self-serve-under-10-min-converts-25pct
title: "Hypothesis: Self-Serve Under 10 Minutes Converts at 25%+"
type: hypothesis
namespace: gtm
summary: "If a new user can sign up, connect an integration, and see a dashboard in under 10 minutes, trial-to-paid conversion will sustain at 25% or higher."
auto_inject: false
applicable_when: null
confidence: 0.6
verified_at: 2026-02-04
verified_by: nemock
staleness_signal: "Falsified if median-setup-time stays under 10 minutes for a full quarter and trial-to-paid does not reach 25%."
tags: [hypothesis, gtm, activation]
edges:
  - target: pillar-self-serve-over-enterprise-sales
    type: related_to
    weight: 0.8
    note: "The self-serve pillar implicitly assumes this hypothesis is true."
  - target: source-internal-data-q1-2026-trial-cohort
    type: related_to
    weight: 0.75
    note: "Q1 2026 cohort is the first data point on this hypothesis."
related: []
source_url: null
controlled_document: false
---

# Hypothesis: Self-Serve Under 10 Minutes Converts at 25%+

## Summary

A falsifiable bet that drives our activation work.

## Hypothesis statement

If a new user can sign up, connect at least one integration, and see a populated dashboard within 10 minutes of starting, then trial-to-paid conversion will sustain at 25% or higher across two consecutive quarters.

## Falsification condition

The Q1 2026 cohort had:

- Median setup time: 14 minutes overall, 8 minutes among activated trials.
- Trial-to-paid (cleanly defined): 18%.

Both signals are encouraging but neither meets the bar. We will re-test in Q2 2026 after the integration-setup UX work that is in flight.

## What this hypothesis is NOT

It is **not** the claim that fast setup is the only thing that drives conversion. It is the claim that fast setup is a *necessary* condition. Conversion may also depend on whether the first dashboard tells a story the VPE wants to share upward.

## Edges

`related_to` the self-serve pillar (the pillar implicitly assumes the hypothesis). `related_to` the Q1 cohort data (the first data point).
