# Schema

The company-brain schema is single-sourced in [`src/company_brain/schema/`](../src/company_brain/schema/). This document is the human-readable companion. If the two ever drift, the Python data is authoritative.

For design rationale, see [PRD.md §7](../PRD.md). For the controlled-document boundary that the medical-device profile enforces, see [controlled-document-boundary.md](controlled-document-boundary.md).

## Node types

Three categories: **epistemic** (inherited from the Infinite Brain pattern), **entity** (company-brain additions, always available), and **profile-conditional** (medical-device adds these).

### Epistemic (10)

| Name | Folder | Purpose |
|---|---|---|
| `pillar` | `pillars/` | Durable principle that should shape future agent answers. Can be written in negative form for strategic non-goals. |
| `decision` | `decisions/` | Concrete choice between alternatives. Template body includes a `## What This Rules Out` section. Anti-decisions live here. |
| `playbook` | `playbooks/` | Repeatable procedure. |
| `pattern` | `patterns/` | Observed regularity across examples. |
| `hypothesis` | `hypotheses/` | Falsifiable prediction or bet. |
| `fact` | `facts/` | Verified atomic claim. May be a metric snapshot if it carries `metric_id`. |
| `concept` | `concepts/` | Defined term or mental model. |
| `source` | `sources/` | External material with synthesis. Provenance anchor. Requires `source_kind`. |
| `question` | `questions/` | Known unknown worth preserving because answering it would change a decision, pillar, playbook, or hypothesis. |
| `note` | `notes/` | Temporary or weakly-structured material. Should graduate to a more specific type when it earns one. |

### Entity (11)

Always available regardless of profile.

| Name | Folder | Purpose |
|---|---|---|
| `product` | `entities/products/` | A shipped or in-development product. Opaque in v1; v2 introduces BOM. |
| `product-line` | `entities/product-lines/` | A family of related products. |
| `persona` | `entities/personas/` | Archetypal user. |
| `customer` | `entities/customers/` | Named real customer (anonymize as needed). |
| `stakeholder` | `entities/stakeholders/` | Internal or external party with influence. |
| `competitor` | `entities/competitors/` | Named competitor. Requires `legal_name` + `canonical_url`. |
| `vendor` | `entities/vendors/` | Supplier, contractor, or service provider. |
| `requirement` | `entities/requirements/` | Market, user, or system requirement. Requires `requirement_class`. |
| `feature` | `entities/features/` | Product capability. |
| `use-case` | `entities/use-cases/` | Scenario of use, framed around a job-to-be-done. |
| `metric` | `entities/metrics/` | The concept of a measurement. Requires `volatility_class`. Time-series facts link back via `metric_id`. |

### Profile-conditional — medical-device (9)

| Name | Folder | Purpose |
|---|---|---|
| `indication-for-use` | `entities/indications-for-use/` | Population + condition + intervention + setting. Belongs to a product (ours or competitor's). Versioned via `preceded_by` chain. |
| `regulatory-clearance` | `risk/regulatory-clearances/` | One node per clearance event. Predicate relationships use `preceded_by` edges. |
| `risk-insight` | `risk/risk-insights/` | Planning-level observation about risk. Not a risk record. |
| `hazard` | `risk/hazards/` | Potential source of harm, in ISO 14971 vocabulary. |
| `hazardous-situation` | `risk/hazardous-situations/` | Circumstance where a hazard could lead to harm. |
| `harm` | `risk/harms/` | Potential physical injury, damage, or impact. |
| `risk-control-idea` | `risk/risk-control-ideas/` | Candidate mitigation under consideration. Not a chosen control. |
| `regulation` | `risk/regulations/` | Cited regulation (MDR, 21 CFR 820, etc.). |
| `standard` | `risk/standards/` | Cited standard (ISO 14971, IEC 62304, IEC 60601, etc.). |

Every node in `risk/` and `entities/indications-for-use/` carries `controlled_document: false`. The medical-device profile appends a footer disclaimer to every generated document.

## Edge types

v1 inherits the Infinite Brain edge set unchanged. No new edge types in v1; v2 introduces quantity-bearing variants for BOM modeling.

| Name | Symmetric? | Inverse | Default weight | Use when |
|---|---|---|---|---|
| `related_to` | yes | — | 0.5 | Real but non-specific relationship. Prefer a more specific edge when one fits. |
| `depends_on` | no | — | 0.7 | A cannot stand without B. Use sparingly. |
| `derived_from` | no | — | 0.8 | A claim derives from a source, note, interview, or data point. Required for provenance. |
| `contradicts` | yes | — | 0.8 | A and B cannot both be true. Preserve contradictions rather than smoothing. |
| `supports` | no | — | 0.7 | A strengthens or expresses B. Common for decision → pillar. |
| `part_of` | no | — | 0.8 | A belongs to a larger pillar, playbook, or concept. v2 extends with quantity for BOM. |
| `preceded_by` | no | `followed_by` | 0.8 | A came after B in time or sequence. **IFU history chains** and **predicate device chains** use this. |
| `followed_by` | no | `preceded_by` | 0.8 | A came before B. Inverse of `preceded_by`; the maintainer auto-fills. |
| `authored_by` | no | — | 0.6 | A was authored by B. Used when people are modeled as nodes. |
| `tagged_with` | no | — | 0.4 | A is tagged with B. Use only if tags are modeled as nodes. |

## Source kinds

The `source_kind` field on `source` nodes drives MRD claim labeling, so a reader can distinguish vision-driven claims from evidence-driven claims.

| Kind | What it is |
|---|---|
| `customer-interview` | A specific conversation with a real or prospective customer. |
| `market-data` | Third-party market research or public statistics. |
| `citation` | A book, paper, talk, or article. |
| `founder-vision` | A documented thesis from a company founder or principal. |
| `domain-expertise` | Documented expertise of a named team member. |
| `strategic-thesis` | A bet about the market that the company is making. |
| `internal-data` | Internal telemetry, user data, or observed product behavior. |
| `prior-internal-doc` | An existing internal document being ingested. |
| `skill-output` | The output of another Claude Code skill (requires `producing_skill`). |
| `press-release` | Date-stamped corporate announcement. |
| `web-snapshot` | Page captured at a moment (requires `url`, `captured_at`, `captured_method`, `attachment`). |
| `web-snapshot-network` | List of network requests from a captured page; tech-stack intel. |
| `fda-510k-summary` | The public PDF summary for a 510(k) clearance. |
| `regulatory-filing` | Broader bucket for non-510(k) regulatory documents. |

## Profiles

| Name | What it does |
|---|---|
| `default` | Industry-agnostic. Only epistemic and entity types are active. |
| `medical-device` | Activates the 9 profile-conditional node types above. Appends the controlled-document-boundary footer to every generated document. |
| `saas` | Reserved. No additional node types in v1; content lands in v2. |
| `hardware` | Reserved. No additional node types in v1; content lands in v2. |
| `services` | Reserved. No additional node types in v1; content lands in v2. |

A vault declares its profile in `_system/PROFILE.md`:

```yaml
---
profile: medical-device
profile_version: 1.0
---
```

## Frontmatter

### Base required fields (all nodes)

| Field | Type | Required? | Description |
|---|---|---|---|
| `id` | string | yes | Stable kebab-case identifier, prefix matches the node type (e.g. `pillar-pricing-philosophy`). |
| `title` | string | yes | Human-readable title. |
| `type` | string | yes | The node type. Must match a registered `NodeTypeSpec.name`. |
| `namespace` | string | yes | Visibility / category label. Free-form for v1. |
| `summary` | string | yes | One line, 100–200 chars. The first-pass retrieval signal. |
| `auto_inject` | boolean | yes | If true, the node enters agent context when `applicable_when` matches. |
| `applicable_when` | string | conditional | Required when `auto_inject: true`. |
| `confidence` | number | yes | 0.0–1.0. How trustworthy is this node? |
| `verified_at` | date | yes | ISO date the node was last verified. |
| `verified_by` | string | yes | Handle of the verifier. |
| `staleness_signal` | string | optional | Concrete description of what would make this node stale. |
| `tags` | list | yes | Free-form tags. Default `[]`. |
| `edges` | edge-list | yes | Typed outbound edges. Default `[]`. |
| `related` | list | yes | Loose related-to references (untyped). Prefer `edges`. Default `[]`. |
| `source_url` | string | optional | External URL backing this node, when one exists. |
| `controlled_document` | boolean | yes | Affirmative declaration that this is a planning artifact, not a controlled record. Default `false`. |

### Additional required fields by node type

| Node type | Additional required fields |
|---|---|
| `source` | `source_kind`. Conditional: `producing_skill` (when `source_kind: skill-output`); `url`, `captured_at`, `captured_method`, `attachment` (when `source_kind: web-snapshot`). |
| `requirement` | `requirement_class` (one of: `market`, `user`, `system`, `software`, `hardware`). Drives which requirements-doc generator picks the node up: MRD ← `market`, SRD ← `system`, SRS ← `software`, HRS ← `hardware`. |
| `metric` | `volatility_class` (one of: `low`, `medium`, `high`). |
| `competitor` | `legal_name`, `canonical_url`. |
| `indication-for-use` | `population`, `condition`, `intervention`, `setting`, `belongs_to_product`. |
| `regulatory-clearance` | `clearance_number`, `clearance_type`, `clearance_date`, `applicant`, `device_name`, `product_codes`, `summary_url`. |

### Edge frontmatter shape

Each entry in the `edges` list:

```yaml
edges:
  - target: pillar-pricing-philosophy
    type: supports
    weight: 0.9
    note: "This decision expresses the pricing pillar."
```

`target` must resolve to a real node id in the vault (validated by `cb validate`). `type` must be one of the registered edge types. `weight` is a float in `[0, 1]`. `note` is optional but encouraged.

## Programmatic access

```python
from company_brain.schema import (
    NODE_TYPES,
    EDGE_TYPES,
    SOURCE_KIND_SPECS,
    PROFILES,
    BASE_REQUIRED_FIELDS,
    get_active_node_types,
    get_profile,
)

# All node types active for a profile (epistemic + entity always; medical-device adds the 9 conditional types).
active = get_active_node_types("medical-device")

# A profile's controlled-document footer policy.
profile = get_profile("medical-device")
assert profile.appends_controlled_document_footer is True
```
