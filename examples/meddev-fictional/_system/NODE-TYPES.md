# Node Types

Active profile: `medical-device`. This file is rendered from the company-brain schema package; do not edit by hand. To refresh after a company-brain upgrade, run `cb scaffold --force`.

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

## Profile-conditional (9)

### `indication-for-use`

- **Folder**: `entities/indications-for-use/`
- **Purpose**: Population + condition + intervention + setting. Belongs to a product (ours or a competitor's). Versioned via preceded_by chain.
- **Additional required fields**: `population`, `condition`, `intervention`, `setting`, `belongs_to_product`
- **Notes**:
  - Always carries controlled_document: false.

### `regulatory-clearance`

- **Folder**: `risk/regulatory-clearances/`
- **Purpose**: A specific clearance event (510(k), De Novo, PMA, breakthrough designation, letter-to-file). Predicate chains use preceded_by edges.
- **Additional required fields**: `clearance_number`, `clearance_type`, `clearance_date`, `applicant`, `device_name`, `product_codes`, `summary_url`
- **Notes**:
  - Always carries controlled_document: false.

### `risk-insight`

- **Folder**: `risk/risk-insights/`
- **Purpose**: A planning-level observation about risk. Not a risk record.
- **Notes**:
  - Always carries controlled_document: false.

### `hazard`

- **Folder**: `risk/hazards/`
- **Purpose**: A potential source of harm, in ISO 14971 vocabulary, captured for thinking.
- **Notes**:
  - Always carries controlled_document: false.

### `hazardous-situation`

- **Folder**: `risk/hazardous-situations/`
- **Purpose**: A circumstance where a hazard could lead to harm.
- **Notes**:
  - Always carries controlled_document: false.

### `harm`

- **Folder**: `risk/harms/`
- **Purpose**: A potential physical injury, damage, or impact.
- **Notes**:
  - Always carries controlled_document: false.

### `risk-control-idea`

- **Folder**: `risk/risk-control-ideas/`
- **Purpose**: A candidate mitigation under consideration. Not a chosen risk control.
- **Notes**:
  - Always carries controlled_document: false.

### `regulation`

- **Folder**: `risk/regulations/`
- **Purpose**: A cited regulation (MDR, 21 CFR 820, etc.).

### `standard`

- **Folder**: `risk/standards/`
- **Purpose**: A cited standard (ISO 14971, IEC 62304, IEC 60601, etc.).
