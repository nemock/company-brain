---
id: vendor-stripe
title: "Stripe (payments)"
type: vendor
namespace: vendors
summary: "Payment processor. Handles billing for all paid workspaces; charges 2.9% + 30c for US card transactions."
auto_inject: false
applicable_when: null
confidence: 0.95
verified_at: 2026-02-01
verified_by: nemock
staleness_signal: "Verify if Stripe fee structure changes or we evaluate alternatives."
tags: [vendor, payments, infrastructure]
edges: []
related: []
source_url: "https://stripe.com/pricing"
controlled_document: false
---

# Stripe (payments)

## Summary

Stripe handles all Loftwing billing.

## Why Stripe

Self-serve PLG motion (per [`pillar-self-serve-over-enterprise-sales`](../../pillars/pillar-self-serve-over-enterprise-sales.md)) requires a credit-card-friendly payment processor with good developer ergonomics. Stripe is the default.

## Costs

- US card transactions: 2.9% + 30c.
- International cards: 3.9% + 30c.
- ACH (where relevant for larger workspaces): 0.8%, capped at $5.

On our pricing ($99 / $299 / $899), Stripe fees are the largest variable cost on a per-customer basis.

## Risks

Single-vendor dependency for revenue. Mitigation deferred until ARR justifies a second processor.
