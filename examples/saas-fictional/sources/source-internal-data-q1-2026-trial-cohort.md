---
id: source-internal-data-q1-2026-trial-cohort
title: "Internal Data: Q1 2026 Trial Cohort"
type: source
namespace: analytics
summary: "Internal cohort data covering the Q1 2026 trial signups: setup time, activation milestones, conversion to paid."
auto_inject: false
applicable_when: null
confidence: 0.95
verified_at: 2026-04-08
verified_by: nemock
staleness_signal: "Each quarter's cohort is its own snapshot; do not edit."
tags: [internal, analytics, cohort]
source_kind: internal-data
edges: []
related: []
source_url: null
controlled_document: false
---

# Internal Data: Q1 2026 Trial Cohort

## Summary

The Q1 2026 trial-cohort dataset.

## Content

- 213 trials started.
- 47 trials activated (defined as: at least one integration connected + at least one dashboard view in week 1).
- 47/213 = 22% trial-to-paid conversion (close, but the conversion definition is "activated and paid by end of trial," not "activated").
- Of activated, 38 became paying customers by end-of-trial (so true trial-to-paid is 38/213 = 18%, not 22% — see note).
- Median setup time across all trials: 14 minutes. Among activated trials: 8 minutes.

## Notes

The headline 22% number conflates activation and paid conversion. The MRD should cite the cleaner 18% figure. The hypothesis [`hypothesis-self-serve-under-10-min-converts-25pct`](../hypotheses/hypothesis-self-serve-under-10-min-converts-25pct.md) targets 25%; we are not there yet, but the activated-cohort path is encouraging.
