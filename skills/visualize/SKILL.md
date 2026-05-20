---
name: visualize
description: Generate a D3-based interactive HTML visualization of the company-brain vault graph. Force-directed layout, node coloring by type, edge styling by edge type, optional community detection, and special view modes for IFU history chains and predicate trees (medical-device).
---

# visualize

> Placeholder skill. Implementation lands in v0.4.0.

Wraps `cb viewer` to emit a self-contained `vault-graph.html` to `exports/`. View modes:

- **Default** — force-directed graph, colored by node type.
- **IFU history chains** — highlights `preceded_by` / `followed_by` ladders on indication-for-use nodes.
- **Predicate tree** — highlights regulatory-clearance lineage via `preceded_by` edges.

Lifted-inspiration from [graphify](https://github.com/safishamsi/graphify). See [PRD.md §14](../../PRD.md).
