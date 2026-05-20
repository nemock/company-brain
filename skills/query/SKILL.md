---
name: query
description: Answer questions against a company-brain vault using staged retrieval, auto-injected pillars, typed edge traversal, and node-id citations. Profile-aware. Cites the graph as the source of truth; flags contradictions, staleness, and confidence.
---

# query

> Placeholder skill. Implementation lands in v0.3.0.

Implements the IB retrieval analyst pattern with profile awareness:

1. Load `_system/INDEX.md` and auto-inject relevant pillars.
2. Select candidate nodes by summary relevance, type, confidence, and recency.
3. Expand the candidate set by walking typed edges.
4. Answer with node-id citations, flagged by `source_kind`, with staleness warnings where applicable.

See [PRD.md §10 and §12](../../PRD.md) and the example queries the competitive archive unlocks.
