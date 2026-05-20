---
name: maintain
description: Audit and repair a company-brain vault. Confidence decay on time-series fact nodes, broken-edge repair, missing-inverse-edge auto-fix, INDEX.md drift repair, schema-drift detection. Run periodically to keep retrieval reliable.
---

# maintain

> Placeholder skill. Implementation lands in v0.4.0.

Actions:

- **Confidence decay** — applies only to `fact` nodes linked to a `metric` of `volatility_class: medium` or `high`. Decay half-lives: high = 30 days, medium = 180 days. Pillars, decisions, and other epistemic types do not decay automatically.
- **Audit** — runs `cb validate` and reports critical / important / cleanup-opportunity findings.
- **Repair** — auto-fixes the most common issues: missing inverse edges, INDEX.md drift, missing `controlled_document: false` on profile-conditional nodes.
- **Human-review queue** — surfaces facts whose decayed confidence has dropped below threshold, weak summaries, and nodes whose staleness signals appear triggered.

See [PRD.md §12 and §13](../../PRD.md).
