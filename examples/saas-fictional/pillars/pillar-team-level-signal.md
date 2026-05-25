---
id: pillar-team-level-signal
title: "Team-Level Signal Over Individual-Contributor Metrics"
type: pillar
namespace: product-strategy
summary: "Every Loftwing metric and dashboard view is scoped to the team or higher; we do not surface or score individual contributors."
auto_inject: true
applicable_when: "metrics, dashboards, surveillance, IC, individual, developer, ranking, scoring, performance, productivity, monitoring, observability of people"
confidence: 0.9
verified_at: 2026-01-20
verified_by: nemock
staleness_signal: "Revisit if a strategic partnership or major enterprise deal hinges on IC-level features and we discover the trade-off has shifted."
tags: [strategy, positioning]
edges:
  - target: source-strategic-thesis-team-level-metrics
    type: derived_from
    weight: 0.95
    note: "This pillar is the formalization of the strategic thesis."
  - target: source-domain-expertise-12-years-eng-management
    type: supports
    weight: 0.7
    note: "Founder has watched IC-level tools fail at three companies."
related: []
source_url: null
controlled_document: false
---

# Team-Level Signal Over Individual-Contributor Metrics

## Summary

Engineering productivity at Loftwing is a team-level conversation, not an individual one.

## Content

Every metric, every dashboard view, every export rolls up to the team or higher. The smallest unit of analysis we expose is "the team." We never display PR counts per developer, lines-of-code per developer, or any scored ranking of individuals.

This is a positive pillar (we will measure teams) tightly paired with the non-goal pillar [`pillar-no-developer-surveillance`](pillar-no-developer-surveillance.md) (we will not measure individuals). Both must hold; relaxing either breaks the trust we trade on.

## Edges

`derived_from` the strategic thesis on team-level metrics. `supports` 12 years of domain expertise watching IC-level tools poison eng-management trust.
