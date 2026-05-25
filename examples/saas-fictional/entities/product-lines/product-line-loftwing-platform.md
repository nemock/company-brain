---
id: product-line-loftwing-platform
title: "Loftwing Platform"
type: product-line
namespace: products
summary: "The Loftwing product line: engineering productivity analytics for VPs of Engineering, with a shared data layer across all products."
auto_inject: false
applicable_when: null
confidence: 0.9
verified_at: 2026-01-22
verified_by: nemock
staleness_signal: "Revisit when we add a second standalone product (currently planned for v2)."
tags: [product-line]
edges: []
related: []
source_url: null
controlled_document: false
---

# Loftwing Platform

## Summary

The shared platform that all Loftwing products run on.

## What's in it

In v1, the platform hosts a single user-facing product (Loftwing Insights). The shared layers are:

- Integration adapters (GitHub, Linear, Jira)
- Event warehouse (PostgreSQL + Materialize)
- Auth + workspace management
- Dashboard rendering engine

When Loftwing Boards ships in v2, it will sit on top of the same shared layers.
