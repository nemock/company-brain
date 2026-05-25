---
id: pillar-icp-vpe-scaling-saas
title: "ICP: VPE at Scaling B2B SaaS (50–250 Engineers)"
type: pillar
namespace: product-strategy
summary: "Loftwing serves VPs of Engineering and CTOs at B2B SaaS companies between Series A and Series C (roughly 50–250 engineers)."
auto_inject: true
applicable_when: "ICP, target market, audience, who we serve, segment, persona, vertical, customer profile, deal size, sales motion"
confidence: 0.9
verified_at: 2026-01-15
verified_by: nemock
staleness_signal: "Revisit if we sustain 30%+ of paying customers outside this band for two consecutive quarters."
tags: [icp, strategy]
edges:
  - target: source-vision-loftwing-2026
    type: derived_from
    weight: 0.9
    note: "Founder vision identifies this segment as underserved by incumbents."
  - target: source-customer-interview-2026-03-vpe-northgate
    type: supports
    weight: 0.7
    note: "Northgate is exactly the persona this pillar describes."
related: []
source_url: null
controlled_document: false
---

# ICP: VPE at Scaling B2B SaaS (50–250 Engineers)

## Summary

The customer we serve.

## Content

Loftwing serves **VPs of Engineering and CTOs at B2B SaaS companies, Series A through Series C, roughly 50–250 engineers**. This band is the sweet spot for three reasons:

1. **Below ~50 engineers**, the VPE already knows what the team is working on; analytics is a nice-to-have, not a workflow.
2. **Above ~250 engineers**, the company has bespoke internal tooling and an analytics team; we cannot compete with the in-house solution.
3. **The 50–250 band has the board-prep problem**: the team is too big to track by intuition, the board wants metrics, and the existing tools are aimed at the IC level (LinearB, Code Climate Velocity) or the consultant level (Jellyfish at the enterprise end).

This pillar governs every product decision. When in doubt: would the VPE at a 120-engineer Series B company find this useful? If yes, build it. If no, skip it.

## Edges

`derived_from` the founder vision; `supports` the Northgate customer interview as a concrete instance of the persona.
