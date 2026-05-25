---
id: question-when-to-add-gitlab-support
title: "Question: When to Add GitLab Support?"
type: question
namespace: product
summary: "Under what conditions should Loftwing add GitLab support, given v1 ships GitHub-only per decision-002?"
auto_inject: false
applicable_when: null
confidence: 0.7
verified_at: 2026-04-15
verified_by: nemock
staleness_signal: "Re-evaluate quarterly when reviewing the staleness condition on decision-002."
tags: [question, integrations]
edges:
  - target: decision-002-three-integrations-only-in-v1
    type: related_to
    weight: 0.95
    note: "This question is the explicit revisit trigger for the decision."
related: []
source_url: null
controlled_document: false
---

# Question: When to Add GitLab Support?

## Summary

Open question: under what conditions do we revisit the GitLab exclusion?

## Why it's open

[`decision-002`](../../decisions/decision-002-three-integrations-only-in-v1.md) explicitly excludes GitLab in v1. The decision's staleness signal is "if more than 20% of trial-cohort signups cite a missing integration as the reason for not activating." This question is the operational form of that revisit trigger.

## What would tip the decision

- Trial cohort data showing GitLab as the most-cited missing integration two quarters in a row.
- An inbound enterprise deal in our ICP band that requires GitLab and would otherwise close.
- An open-source GitLab API client maturing enough to halve the integration build cost.

## Status

Open. No revisit triggered yet by Q1 cohort data.
