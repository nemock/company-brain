---
id: metric-trial-to-paid-conversion
title: "Metric: Trial-to-Paid Conversion"
type: metric
namespace: gtm-metrics
summary: "Percentage of trial signups that become paying customers by end of trial. Quarterly measurement window."
auto_inject: false
applicable_when: null
confidence: 0.9
verified_at: 2026-04-08
verified_by: nemock
staleness_signal: "Definition is stable; the volatility class drives snapshot decay."
tags: [metric, gtm]
volatility_class: medium
edges:
  - target: hypothesis-self-serve-under-10-min-converts-25pct
    type: related_to
    weight: 0.9
    note: "The hypothesis targets this metric."
related: []
source_url: null
controlled_document: false
---

# Metric: Trial-to-Paid Conversion

## Summary

% of trial signups that pay by end of trial.

## Definition

Trial-to-paid conversion = (number of trials in cohort that became paying customers by end of trial) / (number of trials in cohort that started in that quarter). Measured quarterly. Calendar quarters.

## Why volatility = medium

The metric changes quarter-to-quarter as we ship activation improvements, but slow enough that a one-month-old snapshot is still mostly trustworthy. Annual half-life on snapshot confidence (per maintain skill) is about right.

## Edges

`related_to` the hypothesis that targets this metric.
