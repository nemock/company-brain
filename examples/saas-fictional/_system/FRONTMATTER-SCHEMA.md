# Frontmatter Schema

This file is rendered from the company-brain schema package; do not edit by hand.

## Base required fields (all nodes)

| Field | Type | Required? | Description |
|---|---|---|---|
| `id` | string | yes | Stable kebab-case identifier, prefix matches the node type. |
| `title` | string | yes | Human-readable title. |
| `type` | string | yes | The node type. Must match a registered NodeTypeSpec.name. |
| `namespace` | string | yes | Visibility / category label. Free-form for v1. |
| `summary` | string | yes | One line, 100–200 chars, lets an agent decide whether to load the body. |
| `auto_inject` | boolean | yes | If true, the node enters agent context when applicable_when matches. |
| `applicable_when` | string | optional | When auto_inject is true, the condition under which the node injects. |
| `confidence` | number | yes | 0.0–1.0. How trustworthy is this node? |
| `verified_at` | date | yes | ISO date the node was last verified. |
| `verified_by` | string | yes | Handle of the verifier. |
| `staleness_signal` | string | optional | Concrete description of what would make this node stale. |
| `tags` | list | yes | Free-form tags. |
| `edges` | edge-list | yes | Typed outbound edges. |
| `related` | list | yes | Loose related-to references (untyped). Prefer edges. |
| `source_url` | string | optional | External URL backing this node, when one exists. |
| `controlled_document` | boolean | yes | Affirmative declaration that this is a planning artifact, not a controlled record. |

## Additional required fields by node type

### `source`

| Field | Type | Description |
|---|---|---|
| `source_kind` | string | One of the registered SourceKind values. Drives MRD claim labeling. |

### `competitor`

| Field | Type | Description |
|---|---|---|
| `legal_name` | string | Legal company name. |
| `canonical_url` | string | The competitor's primary domain. Scopes all subsequent capture. |

### `requirement`

| Field | Type | Description |
|---|---|---|
| `requirement_class` | string | One of: market, user, system, software, hardware. Drives which requirements-doc generator picks the node up. |

### `metric`

| Field | Type | Description |
|---|---|---|
| `volatility_class` | string | One of: low, medium, high. Drives confidence decay half-life for snapshot facts. |
