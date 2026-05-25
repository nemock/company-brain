---
id: question-add-team-health-sentiment-input
title: "Question: Add a Team-Health Sentiment Input?"
type: question
namespace: product
summary: "Should Loftwing accept a weekly team-health sentiment input (e.g., a single-emoji pulse from each team's lead) and surface it alongside the velocity metrics?"
auto_inject: false
applicable_when: null
confidence: 0.6
verified_at: 2026-04-15
verified_by: nemock
staleness_signal: "Re-evaluate after the Q2 customer interviews."
tags: [question, product]
edges:
  - target: pillar-no-developer-surveillance
    type: related_to
    weight: 0.7
    note: "Any sentiment input must stay above the team level — design carefully."
related: []
source_url: null
controlled_document: false
---

# Question: Add a Team-Health Sentiment Input?

## Summary

Open question: should team-level sentiment join velocity metrics on the dashboard?

## Why it's open

Some customers (the Northgate VPE among them) have asked. The product hook is real: velocity numbers without context can be misleading, and a single weekly emoji from each team lead is cheap to collect.

The risk is feature creep and accidentally drifting toward the surveillance pattern we are explicit about avoiding. A sentiment input must stay at the team-lead level, never per-IC.

## Open considerations

- Do team leads actually fill in a weekly pulse? (Behavioral question; the friction may dominate the value.)
- Does the sentiment add to the board narrative or distract from it?
- Does it become a "we noticed sentiment dropped, what happened?" surveillance vector via the team lead?

## Decision deferred

To Q3 2026 at earliest. The Q2 customer interviews should sharpen this.
