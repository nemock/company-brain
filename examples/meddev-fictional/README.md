# meddev-fictional example vault

A hand-built fictional company-brain vault that stress-tests the v0.1.0 schema. **Every name, product, person, customer, competitor, K-number, and metric in this vault is invented.** Nothing here represents any real company, device, or clinical event.

## The fictional company

**Vitalisens** is a fictional medical-device startup building an ambulatory cardiac telemetry product. The product line has two SKUs:

- **Vitalisens Cardio** — a continuous patient-monitoring wearable for adult patients in ambulatory settings after a cardiac event or during an arrhythmia workup.
- **Vitalisens Pad** — a replaceable adhesive sensor pad rated for 7 days of wear. The pad is the recurring-revenue engine.

Vitalisens is targeting a 510(k) clearance citing fictional predicates from two fictional competitors (CardioTrace Inc and PulseGuard Medical).

## What this vault demonstrates

This is a v0.1.0 reference. It exercises every category of the schema and the convention patterns called out in the PRD.

- **Pillars** — both positive principles (auto-injecting on ICP / pricing / disposables) and **non-goal pillars** (we will NOT enter pediatric; we will NOT produce physical documentation).
- **Decisions** — every decision body has a `## What This Rules Out` section, including explicit anti-decisions.
- **Indications for use** — our planned IFU plus a competitor's two-version IFU chain linked via `preceded_by`.
- **Regulatory clearances** — three fictional clearances with predicate edges using `preceded_by`. Demonstrates how IFU history and predicate chains both ride on the same edge type.
- **Competitor archive** — two `competitor` nodes with `legal_name` and `canonical_url`. One has an attached web-snapshot in `_attachments/` plus a 510(k) summary source plus a press release.
- **Provenance** — every claim traces via `derived_from` to a `source` node. Sources span the full range of `source_kind` values: `founder-vision`, `domain-expertise`, `strategic-thesis`, `customer-interview`, `citation`, `internal-data`, `press-release`, `web-snapshot`, `fda-510k-summary`, `market-data`.
- **Time-series facts** — one `metric` node with two snapshot facts, each carrying `metric_id`, demonstrating the confidence-decay foundation.
- **Risk vocabulary** — `risk-insight`, `hazard`, `hazardous-situation`, `harm`, `risk-control-idea`, plus a `regulation` and a `standard`. All carry `controlled_document: false`.

## What this vault is NOT

- **Not a controlled document.** Every node carries `controlled_document: false`. This entire vault is a planning artifact. It is not, and could not be, a design history file, a risk management file, or a traceability matrix. See [docs/controlled-document-boundary.md](../../docs/controlled-document-boundary.md).
- **Not a real product.** Vitalisens does not exist. The fictional company, products, K-numbers, indications, and clinical claims here would all need to be validated by real-world engineering, clinical study, and regulatory work before they could be used for anything other than learning the company-brain schema.
- **Not a how-to for FDA filing.** The predicate chain is illustrative of how company-brain models the relationships, not a model of a real submission strategy.

## Reading order

If you are exploring the schema for the first time:

1. **`_system/PROFILE.md`** — confirm the active profile is `medical-device`.
2. **`_system/INDEX.md`** — the agent's entry point. (In this example vault it remains the starter scaffold; the `maintain` skill — landing in v0.4.0 — will populate it from the node files.)
3. **`pillars/`** — start with the four pillars to see the auto-injection pattern and the non-goal convention.
4. **`decisions/`** — each decision has a `## What This Rules Out` section.
5. **`entities/competitors/competitor-cardiotrace-inc.md`** — the most-linked competitor; its IFU chain and clearance chain are next.
6. **`entities/indications-for-use/`** — three IFU nodes, two of them linked by `preceded_by`.
7. **`risk/regulatory-clearances/`** — three clearances. Read in the order: `K181234` → `K231234` (predicate edge to `K181234`). `K221567` is referenced as another predicate from our planned clearance.
8. **`sources/`** — provenance anchors. Note how `source_kind` varies.
9. **`risk/`** — the ISO-14971-vocabulary nodes.

## Re-scaffolding

To refresh the `_system/*.md` files in this vault after a company-brain upgrade:

```bash
cb scaffold --profile medical-device --path examples/meddev-fictional --force
```

This regenerates the five `_system/*.md` reference files from the current schema package without touching node content, the attached PNG, or this README.

## License

Released into the public domain as part of the company-brain project. Use this vault as a starting template, a teaching tool, or a target for `cb validate`.
