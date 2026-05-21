---
id: fact-stripe-fee-2-9-percent-plus-30c
title: "Fact: Stripe US Card Processing Fee"
type: fact
namespace: operations
summary: "Stripe's standard US card processing fee is 2.9% of the transaction amount plus a fixed $0.30 per successful charge. Domestic only."
auto_inject: false
applicable_when: null
confidence: 0.95
verified_at: 2026-05-21
verified_by: nemock
staleness_signal: "Refresh annually or after any Stripe pricing announcement."
tags: [fact, vendor]
edges: []
related: []
source_url: "https://stripe.com/pricing"
controlled_document: false
---

# Fact: Stripe US Card Processing Fee

## Summary

Stripe charges 2.9% + $0.30 per successful US-domestic card transaction. International cards add 1% to the percentage component.

## Content

Why this fact is here: pad-subscription pricing math (per `pillar-disposable-pad-business-model`) requires knowing the payment-processing overhead. This fact anchors that math.

## Notes

Generic operational fact — no metric_id, no decay. Confidence is high because the source URL points at Stripe's own pricing page.
