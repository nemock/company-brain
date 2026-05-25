---
id: concept-board-prep-workflow
title: "Concept: Board-Prep Workflow"
type: concept
namespace: glossary
summary: "The recurring workflow a VPE goes through ahead of each board meeting to assemble a coherent story about engineering progress."
auto_inject: false
applicable_when: null
confidence: 0.85
verified_at: 2026-03-11
verified_by: nemock
staleness_signal: "Refine as we learn from more customer interviews; the current definition is built on four interviews."
tags: [concept, workflow]
edges:
  - target: source-customer-interview-2026-03-vpe-northgate
    type: derived_from
    weight: 0.85
    note: "The Northgate interview is the most detailed description of this workflow we have."
related: []
source_url: null
controlled_document: false
---

# Concept: Board-Prep Workflow

## Summary

The recurring quarterly workflow a VPE goes through to assemble engineering progress for a board meeting.

## Anatomy

The workflow (per customer research, with company-specific variation) looks like:

1. **Pull metrics from current tools** (cycle time, deploy frequency, change failure rate, sprint completion rate). Currently 1–2 hours of manual screenshot collection.
2. **Assemble a narrative** linking the metrics to last quarter's commitments. Currently 2–3 hours in Google Docs.
3. **Translate engineering terms into board-legible language.** "We shipped X" not "we merged Y PRs."
4. **Prep for likely board questions.** "Why did cycle time spike in March?" "Will the new product be on time?"

Total time: 4–6 hours per quarter per VPE. Loftwing's success is taking this to <1 hour.

## Why we model it as a concept

Multiple decisions, pillars, and features reference this workflow. Naming it as a concept lets later artifacts (MRD, sales battle card) point at a single id instead of restating the definition.
