---
name: intake
description: Interactive Q&A capture of company knowledge into typed nodes. Sub-modes include vision (dictation-friendly), product, persona, competitor, competitor-ifu, competitor-clearance, competitor-snapshot, metric, meeting-notes, risk. Use this when adding knowledge to a vault through conversation.
---

# intake

> Placeholder skill. Implementation lands across v0.2.0 (vision, product, competitor sub-modes).

Sub-modes (medical-device profile shown):

- `vision` — six-phase dictation-friendly flow that turns rambling prose into typed nodes with full provenance.
- `product` — capture a product, product line, or sub-component.
- `persona` — build a persona node from a conversation.
- `competitor` — capture a competitor entity (legal name, canonical URL, positioning).
- `competitor-ifu` — capture or update a competitor's indication for use, versioned via `preceded_by`.
- `competitor-clearance` — capture a regulatory clearance for a competitor, including predicate chain.
- `competitor-snapshot` — capture a web-snapshot of a competitor page (manual screenshot import in v1, chrome-devtools-mcp-assisted in v1.x).
- `metric` — define a metric and seed initial fact snapshots.
- `meeting-notes` — process a meeting into atomic nodes.
- `risk` — walk through ISO 14971-vocabulary risk thinking.
- `clearance` — capture our own regulatory clearance plans or status.

See [PRD.md §10](../../PRD.md) for design detail.
