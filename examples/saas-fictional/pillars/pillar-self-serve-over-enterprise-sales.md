---
id: pillar-self-serve-over-enterprise-sales
title: "Self-Serve Setup Over Enterprise Sales Motion"
type: pillar
namespace: gtm-strategy
summary: "A new user must be able to connect Loftwing to their stack and see the first dashboard in under 10 minutes, without talking to sales."
auto_inject: true
applicable_when: "pricing, sales motion, onboarding, signup, setup, time-to-value, GTM, PLG, self-serve, enterprise, demo, contact-sales"
confidence: 0.85
verified_at: 2026-01-22
verified_by: nemock
staleness_signal: "Revisit if a credible enterprise deal pipeline emerges and the unit economics of self-serve don't support the team's runway."
tags: [strategy, gtm, plg]
edges:
  - target: source-customer-interview-2026-03-vpe-northgate
    type: derived_from
    weight: 0.8
    note: "The Northgate VPE was explicit that self-serve is the only motion that fits their decision-making."
  - target: source-vision-loftwing-2026
    type: supports
    weight: 0.6
    note: "Founder vision implies a fast iteration loop that PLG enables and enterprise sales doesn't."
related: []
source_url: null
controlled_document: false
---

# Self-Serve Setup Over Enterprise Sales Motion

## Summary

PLG, not enterprise sales, as the GTM motion.

## Content

A new user must be able to:

1. Sign up with Google or email in under 30 seconds.
2. Connect at least one integration (GitHub, Linear, Jira) in under 5 minutes.
3. See a populated dashboard in under 10 minutes from signup.

Anything that violates this — required calls, forced demos, contact-sales gates on basic functionality — works against this pillar. We are NOT trying to compete with Jellyfish for enterprise procurement. We are trying to be the tool the VPE adopts before procurement is involved.

## Edges

`derived_from` the Northgate customer interview's explicit statement; `supports` the founder vision's implied iteration loop.
