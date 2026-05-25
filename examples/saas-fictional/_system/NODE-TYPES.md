# Node Types

Active profile: `default`. This file is rendered from the company-brain schema package; do not edit by hand. To refresh after a company-brain upgrade, run `cb scaffold --force`.

## Epistemic (10)

### `pillar`

- **Folder**: `pillars/`
- **Purpose**: A durable principle that should shape future agent answers. Can be written in negative form for strategic non-goals.
- **Notes**:
  - Auto-inject pillars must declare applicable_when.
  - Non-goal pillars (e.g., 'we do not enter the consumer market') belong here.

### `decision`

- **Folder**: `decisions/`
- **Purpose**: A concrete choice between alternatives. The body should include a '## What This Rules Out' section.
- **Notes**:
  - Anti-decisions (deliberate non-choices) live here, not in a separate type.

### `playbook`

- **Folder**: `playbooks/`
- **Purpose**: A repeatable procedure.

### `pattern`

- **Folder**: `patterns/`
- **Purpose**: An observed regularity across examples.

### `hypothesis`

- **Folder**: `hypotheses/`
- **Purpose**: A falsifiable prediction or bet.

### `fact`

- **Folder**: `facts/`
- **Purpose**: A verified atomic claim. May be a metric snapshot if it carries metric_id.
- **Notes**:
  - Confidence decay applies to facts linked to medium/high-volatility metrics.

### `concept`

- **Folder**: `concepts/`
- **Purpose**: A defined term or mental model.

### `source`

- **Folder**: `sources/`
- **Purpose**: External material with synthesis. Provenance anchor.
- **Additional required fields**: `source_kind`
- **Notes**:
  - source_kind: skill-output also requires producing_skill.
  - source_kind: web-snapshot also requires url, captured_at, captured_method, attachment.

### `question`

- **Folder**: `questions/`
- **Purpose**: A known unknown worth preserving because answering it would change a decision, pillar, playbook, or hypothesis.

### `note`

- **Folder**: `notes/`
- **Purpose**: Temporary capture or weakly-structured material. Should graduate to a more specific type when it earns one.

## Entity (11)

### `product`

- **Folder**: `entities/products/`
- **Purpose**: A shipped or in-development product. Opaque in v1; v2 introduces BOM and components.

### `product-line`

- **Folder**: `entities/product-lines/`
- **Purpose**: A family of related products.

### `persona`

- **Folder**: `entities/personas/`
- **Purpose**: An archetypal user, distinct from a named real customer.

### `customer`

- **Folder**: `entities/customers/`
- **Purpose**: A named real customer (anonymize as needed).

### `stakeholder`

- **Folder**: `entities/stakeholders/`
- **Purpose**: Internal or external party with influence on a product or program.

### `competitor`

- **Folder**: `entities/competitors/`
- **Purpose**: A named competitor or alternative. legal_name + canonical_url required for disambiguation.
- **Additional required fields**: `legal_name`, `canonical_url`

### `vendor`

- **Folder**: `entities/vendors/`
- **Purpose**: A supplier, contractor, or service provider.

### `requirement`

- **Folder**: `entities/requirements/`
- **Purpose**: A market, user, or system requirement. Class is mandatory so the node is never mistaken for a controlled design input.
- **Additional required fields**: `requirement_class`

### `feature`

- **Folder**: `entities/features/`
- **Purpose**: A product capability.

### `use-case`

- **Folder**: `entities/use-cases/`
- **Purpose**: A scenario of use, framed around a job-to-be-done.

### `metric`

- **Folder**: `entities/metrics/`
- **Purpose**: The concept of a measurement (MRR, churn, day-7 retention). Time-series fact nodes link back via metric_id.
- **Additional required fields**: `volatility_class`
