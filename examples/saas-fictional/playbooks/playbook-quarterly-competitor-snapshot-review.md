---
id: playbook-quarterly-competitor-snapshot-review
title: "Playbook: Quarterly Competitor Snapshot Review"
type: playbook
namespace: competitive
summary: "Every quarter, re-snapshot tracked competitors' product, pricing, and integration pages; capture material changes as new web-snapshot source nodes."
auto_inject: false
applicable_when: null
confidence: 0.9
verified_at: 2026-04-15
verified_by: nemock
staleness_signal: "Refine after running the playbook for two full quarters."
tags: [playbook, competitive, recurring]
edges: []
related: []
source_url: null
controlled_document: false
---

# Playbook: Quarterly Competitor Snapshot Review

## Summary

Quarterly workflow for keeping the competitive archive current.

## Cadence

Once per calendar quarter. Block 2 hours.

## Steps

1. For each `competitor` node in the vault, open the `canonical_url`.
2. Capture screenshots of the homepage, product page, and pricing page.
3. Store under `_attachments/<YYYY-MM-DD>-<competitor-slug>-<page-slug>.png`.
4. Write one `web-snapshot` `source` node per page that materially changed since the last snapshot.
5. If a snapshot reveals a major reposition, raise it as a `question` node and flag for the next product review.
6. Re-render the competitive-brief scaffold; verify the changes show up.

## Why this matters

The competitive archive is only useful if it stays fresh. Without a recurring playbook, snapshots calcify and the MRD's competitive section drifts out of sync with reality. This playbook codifies the discipline.
