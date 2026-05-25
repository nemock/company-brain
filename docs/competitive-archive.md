# Competitive Archive

A company-brain vault becomes a competitive archive when you treat competitors as first-class entities, capture snapshots over time, and let the typed edges connect the dots. This document describes the workflow and the queries it unlocks.

For the schema details, see [`docs/schema.md`](schema.md). For the design rationale, see [PRD §13](../PRD.md).

## The four-node pattern

A competitive archive is built from four node types working together:

1. **`competitor`** (universal) — the entity. Requires `legal_name` and `canonical_url` for disambiguation. One node per competitor company.
2. **`source` with `source_kind: web-snapshot`** (universal) — a page captured at a moment. Each snapshot is its own immutable source node. Attachment lives in `_attachments/`; extracted text in the body.
3. **`indication-for-use`** (medical-device profile only) — what a competitor's product is cleared to do, with `population`, `condition`, `intervention`, `setting`. Versioned via `preceded_by` / `followed_by` chains.
4. **`regulatory-clearance`** (medical-device profile only) — a specific clearance event (510(k), De Novo, PMA, etc.) with structured metadata. Predicate device citations are first-class `preceded_by` edges.

For the `default` profile, the first two cover the archive — typed competitor entities + dated snapshot sources are enough to reason about positioning, pricing, and trajectory.

## Capture workflows

### Add a new competitor

```
Capture a competitor: FlightPath Engineering at https://flightpath-eng.example.com.
```

The [`intake competitor`](../skills/intake/SKILL.md) sub-mode prompts for `legal_name`, `canonical_url`, positioning, and known strengths/weaknesses. The canonical_url is the disambiguation anchor — all subsequent snapshots and atomized content scope to that domain.

### Snapshot a competitor page

v0.5.0 ships manual screenshot import:

```
Read this competitor product-page screenshot and capture it as a web-snapshot source:
  ~/screenshots/flightpath-pricing-2026-05-25.png
```

The [`intake competitor-snapshot`](../skills/intake/SKILL.md) sub-mode (or [`atomize`](../skills/atomize/SKILL.md) on an image) moves the file into `_attachments/`, uses Claude's vision to extract visible text, and writes a `source` node with `source_kind: web-snapshot` and the structured fields (`url`, `captured_at`, `captured_method: manual-screenshot`, `attachment`).

The competitor node gets a `related_to` edge to the new source so downstream queries find it.

v1.x adds [`chrome-devtools-mcp`](https://github.com/upstash/chrome-devtools-mcp) integration for automated full-page captures plus DOM text extraction. The manual path stays as the fallback.

### Atomize a 510(k) summary PDF (medical-device)

```
Atomize this 510(k) summary PDF and extract the clearance, IFU, and predicates:
  ~/Downloads/K231234.pdf
```

`cb extract` pulls page-by-page text and tables. The [`atomize`](../skills/atomize/SKILL.md) skill recognizes the structure and creates:

- One `source` node with `source_kind: fda-510k-summary`.
- One `regulatory-clearance` node with the structured fields (`clearance_number`, `clearance_type`, `clearance_date`, `applicant`, `device_name`, `product_codes`, `summary_url`).
- One `indication-for-use` node with `population` / `condition` / `intervention` / `setting` parsed from the IFU statement.
- For each cited predicate clearance, a `preceded_by` edge on the new clearance node.

v1.x adds `cb intake-510k <K-number>` for one-command openFDA pulls.

### Capture an IFU evolution

When a competitor's IFU changes between clearances, capture the new version as a fresh `indication-for-use` node and add a `preceded_by` edge from the new node to the previous one. The chain becomes a one-hop walk:

```
indication-for-use-cardiotrace-pro-2025-q3 → preceded_by → indication-for-use-cardiotrace-pro-2023-q1
```

The MRD's IFU comparison table, the IFU comparison report scaffold, and the `cb viewer --mode ifu-chain` viewer all read this chain.

## Maintenance

Run the quarterly snapshot review playbook to keep the archive fresh. Both example vaults ship a `playbook-quarterly-competitor-snapshot-review.md` (see [`examples/meddev-fictional/playbooks/`](../examples/meddev-fictional/playbooks/playbook-competitor-510k-monitoring.md) and [`examples/saas-fictional/playbooks/`](../examples/saas-fictional/playbooks/playbook-quarterly-competitor-snapshot-review.md)). Codify the discipline; the archive only matters if it stays current.

`cb maintain decay` does not apply to web-snapshot sources — they are point-in-time captures and stay at their original confidence. What does get stale is the competitor `summary` and our `weakness` reads on competitors; revisit those each quarter against the latest snapshot.

## Queries the archive unlocks

Once the archive has data, the [`query`](../skills/query/SKILL.md) skill can answer:

- "How has CardioTrace's IFU evolved across their 510(k)s?" — one-hop walk of the `preceded_by` chain on their IFU nodes.
- "Which competitor clearances does our planned K243189 cite as predicates?" — `preceded_by` edges out of our planned clearance node.
- "Which competitor changed pricing this quarter?" — diff the most recent two `web-snapshot` source nodes for each competitor's pricing page.
- "Which competitors have a Slack-digest feature?" — full-text query across their web-snapshot extracted text + atomized product pages.
- "What's the chronology of CardioTrace's product roadmap based on their press releases?" — list all sources with `source_kind: press-release` for their competitor node, sort by `verified_at`.

## Documents the archive feeds

| Document | What it consumes |
|---|---|
| MRD §6 Competitive landscape | All `competitor` nodes + edges. Medical-device adds clearances and IFU history per competitor. |
| MRD §3 IFU comparison (medical-device) | `indication-for-use` nodes grouped by `belongs_to_product`. |
| Sales battle card (scaffold) | One competitor + its IFUs + clearances + our pillars + our non-goal pillars. |
| Competitive brief (scaffold) | All competitors + their IFUs/clearances + market-data + press-release sources. |
| IFU comparison report (scaffold, medical-device) | All IFU nodes + their `preceded_by` chains + parent products + corresponding clearances. |
| `cb viewer --mode predicate-tree` | All `regulatory-clearance` nodes + their `preceded_by` predicate links. |

## What this archive is NOT

- Not real-time monitoring. Snapshots are point-in-time. For change detection, use the quarterly review playbook or wait for v1.x recurring-snapshot automation.
- Not a license to scrape. Web snapshots are for your company's internal competitive intelligence; respect robots.txt and any applicable terms of service.
- Not a controlled regulatory record. The IFU and clearance nodes are planning artifacts — even in a medical-device vault, they carry `controlled_document: false` and live above the design history file.
