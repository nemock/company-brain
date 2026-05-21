# Edge Types

v1 inherits the Infinite Brain edge set unchanged. This file is rendered from the schema package; do not edit by hand.

## Edge frontmatter shape

Each entry in a node's `edges` list:

```yaml
edges:
  - target: pillar-pricing-philosophy
    type: supports
    weight: 0.9
    note: "This decision expresses the pricing pillar."
```

- `target` must resolve to an existing node id (validated by `cb validate`).
- `type` must be one of the registered edge types below.
- `weight` is a float in `[0, 1]`.
- `note` is optional but encouraged.

## Registered edge types

| Name | Symmetric? | Inverse | Default weight | Use when |
|---|---|---|---|---|
| `related_to` | yes | — | 0.5 | Real but non-specific relationship. Prefer a more specific edge when one fits. |
| `depends_on` | no | — | 0.7 | A cannot stand without B. Use sparingly; depends_on edges suggest brittleness. |
| `derived_from` | no | — | 0.8 | A claim, decision, or pattern derives from a source, note, interview, or data point. Required for provenance. |
| `contradicts` | yes | — | 0.8 | A and B cannot both be true. Preserve contradictions rather than smoothing them. |
| `supports` | no | — | 0.7 | A strengthens or expresses B. Common for decision → pillar. |
| `part_of` | no | — | 0.8 | A belongs to a larger pillar, playbook, or concept. In v2, quantity edge metadata extends this for BOM modeling. |
| `preceded_by` | no | `followed_by` | 0.8 | A came after B in time or sequence. Used for IFU history chains (later IFU preceded_by earlier IFU) and predicate device chains (clearance preceded_by its predicate). |
| `followed_by` | no | `preceded_by` | 0.8 | A came before B in time or sequence. Inverse of preceded_by. The maintainer auto-fills this when preceded_by is set. |
| `authored_by` | no | — | 0.6 | A was authored by B. Used when people are modeled as nodes. |
| `tagged_with` | no | — | 0.4 | A is tagged with B. Use only if tags are modeled as nodes; otherwise use the tags frontmatter field. |
