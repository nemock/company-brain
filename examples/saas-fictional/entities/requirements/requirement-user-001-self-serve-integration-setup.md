---
id: requirement-user-001-self-serve-integration-setup
title: "User Requirement: Self-Serve Integration Setup"
type: requirement
namespace: requirements
summary: "A new user must be able to connect their issue tracker (Linear or Jira) and code host (GitHub) without engineering help and without contacting support."
auto_inject: false
applicable_when: null
confidence: 0.9
verified_at: 2026-02-04
verified_by: nemock
staleness_signal: "Falsified if Q2 2026 trial-cohort data shows >10% of trials abandoning during integration setup."
tags: [requirement, user, activation]
requirement_class: user
edges:
  - target: pillar-self-serve-over-enterprise-sales
    type: supports
    weight: 0.95
    note: "Self-serve setup is what the pillar names."
related: []
source_url: null
controlled_document: false
---

# User Requirement: Self-Serve Integration Setup

## Summary

The user must integrate Loftwing without help.

## Statement

A new user, starting from scratch, must be able to:

1. Authenticate with GitHub.
2. Authenticate with either Linear or Jira (their choice).
3. Select which projects/repos to track.
4. Reach a first dashboard view.

…all without:

- Contacting support.
- Reading documentation longer than three paragraphs.
- Asking an engineer for help (the user IS the engineering leader).

## Class = user

User requirement: what the user must be able to accomplish, independent of how the system delivers it.
