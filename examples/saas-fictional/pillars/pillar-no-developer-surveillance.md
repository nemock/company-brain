---
id: pillar-no-developer-surveillance
title: "Non-Goal: No Developer Surveillance"
type: pillar
namespace: ethics-and-strategy
summary: "Loftwing will never ship features that score, rank, or surveil individual contributors. The smallest unit of analysis we expose is the team."
auto_inject: true
applicable_when: "individual, IC, surveillance, scoring, ranking, developer monitoring, productivity score, performance review, leaderboard, contribution metrics, code metrics per person"
confidence: 0.95
verified_at: 2026-01-20
verified_by: nemock
staleness_signal: "This is a durable boundary. Revisit only if the founder leaves and the next leadership chooses a different ethical posture (in which case the company name should probably change)."
tags: [non-goal, ethics, strategy]
edges:
  - target: source-strategic-thesis-team-level-metrics
    type: derived_from
    weight: 0.9
    note: "The non-goal is the negative-space corollary of the team-level pillar."
  - target: pillar-team-level-signal
    type: related_to
    weight: 0.95
    note: "These two pillars must hold together."
related: []
source_url: null
controlled_document: false
---

# Non-Goal: No Developer Surveillance

## Summary

We do not score individuals. Ever.

## What This Excludes

- **No per-developer scoring views.** Not in v1, not in v2, not as an enterprise add-on.
- **No "top contributor" leaderboards.** Not in product, not in marketing, not in reports.
- **No per-developer metrics sent to managers' email digests.** Slack/email digests are team-scoped only.
- **No "anonymized" per-developer slices.** Anonymized slices are easily de-anonymized at small team sizes and we will not pretend otherwise.

## Applies when

The `applicable_when` keywords are deliberately broad. If a customer asks for any feature that involves measuring individual contributors, this pillar fires and the answer is "no, here's why."

## Edges

`derived_from` the team-level-metrics strategic thesis. `related_to` the positive pillar it pairs with.
