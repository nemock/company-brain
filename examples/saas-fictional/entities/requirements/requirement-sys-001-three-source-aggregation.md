---
id: requirement-sys-001-three-source-aggregation
title: "System Requirement: Three-Source Aggregation"
type: requirement
namespace: requirements
summary: "The system shall ingest and reconcile event streams from GitHub plus at least one of Linear or Jira, computing team-level rollups within 60 seconds of source-side changes."
auto_inject: false
applicable_when: null
confidence: 0.85
verified_at: 2026-02-04
verified_by: nemock
staleness_signal: "Revisit if a v2 integration (e.g., GitLab) materially changes the ingest architecture."
tags: [requirement, system]
requirement_class: system
edges:
  - target: decision-002-three-integrations-only-in-v1
    type: supports
    weight: 0.9
    note: "The system requirement scopes to the integrations chosen by the decision."
related: []
source_url: null
controlled_document: false
---

# System Requirement: Three-Source Aggregation

## Summary

System-level statement of what the data pipeline must do.

## Statement

The system shall:

- Ingest events from GitHub (webhook + REST poll for backfill).
- Ingest events from Linear OR Jira (customer's choice, only one connected per workspace).
- Compute per-team rollups (cycle time, deploy frequency, sprint accuracy) within 60 seconds of source-side changes.
- Persist raw event data for at least 90 days for re-derivation.

## Class = system

System requirement: spans both software and hardware (here, infrastructure). The SRD scaffold pulls these. The SRS scaffold pulls the more granular software-class requirements.
