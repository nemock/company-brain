---
id: decision-002-three-integrations-only-in-v1
title: "Decision 002: Three Integrations Only in v1 (GitHub, Linear, Jira)"
type: decision
namespace: product
summary: "Loftwing v1 ships with exactly three integrations: GitHub, Linear, and Jira. No GitLab, Bitbucket, Azure DevOps, or other issue trackers until v2."
auto_inject: false
applicable_when: null
confidence: 0.85
verified_at: 2026-02-04
verified_by: nemock
staleness_signal: "Revisit if more than 20% of trial-cohort signups cite a missing integration as the reason for not activating."
tags: [decision, product, integrations]
edges:
  - target: pillar-icp-vpe-scaling-saas
    type: supports
    weight: 0.7
    note: "These three integrations cover ~85% of our ICP's stack per market data."
  - target: source-market-data-dora-2025
    type: derived_from
    weight: 0.6
    note: "DORA-flavored research informed the prioritization."
related: []
source_url: null
controlled_document: false
---

# Decision 002: Three Integrations Only in v1 (GitHub, Linear, Jira)

## Summary

GitHub + Linear + Jira. Nothing else in v1.

## Alternatives Considered

1. **All five major issue trackers + all three major code hosts at launch.** Rejected — engineering time for nine high-quality integrations is more than we have.
2. **Build a generic webhook intake and let customers integrate themselves.** Rejected — defeats the self-serve-under-10-min target; nobody integrates a webhook in 10 minutes.
3. **Three integrations only (GitHub, Linear, Jira), revisit at v2.** Chosen.

## Decision

GitHub for code; Linear and Jira for issue tracking. Everything else is "not supported in v1."

## Rationale

- Per the DORA market data, GitHub + (Linear or Jira) covers ~85% of our ICP.
- Three deep integrations beat nine shallow ones for the activation experience.
- Choosing a small explicit list lets us write clear marketing copy: "Loftwing works with GitHub + Linear or Jira." Ambiguity in v1 hurts the self-serve motion more than missing integrations do.

## What This Rules Out

- **GitLab support in v1.** GitLab users see a "coming in v2" message at signup.
- **Bitbucket support in v1.** Same.
- **Azure DevOps support in v1.** Same.
- **Pivotal Tracker, Asana, Shortcut, ClickUp.** Not in v1.
- **Generic webhook intake.** Not in v1.
- **Customer-built integrations against our API.** API doesn't ship to customers in v1.

## Edges

`supports` the ICP pillar (the three integrations cover the ICP's stack). `derived_from` the market data informing prioritization.
