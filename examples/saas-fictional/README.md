# Loftwing (fictional) — saas-fictional example vault

A hand-built example vault for [company-brain](https://github.com/nemock/company-brain) using the **`default`** industry-agnostic profile.

The fictional company is **Loftwing** — engineering productivity analytics for VPs of Engineering at scaling B2B SaaS companies. The company, its product, customers, competitors, and metrics are all invented; nothing here is real, and nothing here is endorsed by any real engineering analytics vendor.

This vault is one of two examples shipped with company-brain. The other, [`meddev-fictional`](../meddev-fictional/), exercises the `medical-device` profile (additional IFU / regulatory-clearance / risk-* node types). Together they demonstrate that the same schema engine works for very different industries.

## Why two examples

The profile mechanism only earns trust when it is exercised by two profiles. If the meddev-fictional vault and the saas-fictional vault both render usable docs and pass `cb validate` cleanly, the profile mechanism is doing what it claims.

## Scope of this vault

- ~40 nodes covering every active node type in the `default` profile.
- All universal epistemic types (pillar, decision, hypothesis, pattern, fact, concept, source, question, playbook, note).
- All universal entity types (product, product-line, persona, customer, stakeholder, competitor, feature, use-case, requirement, metric, vendor).
- A source from each common `source_kind` so the MRD's evidence-vs-vision split has real data.
- Decisions with `## What This Rules Out` sections; non-goal pillars tagged `non-goal`.
- Requirements split across `market`, `user`, `system`, and `software` classes (no `hardware` — Loftwing is software-only).
- Metrics of both `medium` and `high` volatility so the maintain skill's decay path has something to chew on.

## What's NOT here (and why)

The `default` profile does not activate `indication-for-use`, `regulatory-clearance`, `risk-insight`, `hazard`, `hazardous-situation`, `harm`, `risk-control-idea`, `regulation`, or `standard`. Those are medical-device-only; see `examples/meddev-fictional` for vaults that include them.

## Try it

```bash
cb validate --path examples/saas-fictional
cb render mrd --path examples/saas-fictional
cb render one-pager --path examples/saas-fictional
cb viewer --path examples/saas-fictional
```

Pre-generated outputs live under `exports/`.

## Maintenance

- `cb validate` — schema check.
- `cb maintain audit` — read-only health summary.
- `cb maintain rebuild-index` — regenerate `_system/INDEX.md`.
