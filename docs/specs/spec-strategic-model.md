---
title: "Spec — `strategic-model` node type + generators"
status: draft
version: 0.1.0
date: 2026-05-26
target_milestone: v1.x
controlled_document: false
---

# Spec: `strategic-model` node type + generators

> **Purpose.** Lock the design for the first roadmap target out of the Aha! deep-dive analysis. This is the most asymmetric move identified — Aha! ships strategic-model templates you fill in by hand; company-brain ships them as generated artifacts that recompute when the underlying typed graph changes.
>
> **Target milestone.** v1.x (post-v1.0.0). Sequence: ship `strategic-model` after research-agent so the dogfood loop is intact at release.
>
> **Prerequisite.** This spec depends on [`spec-primary-entity-marking`](spec-primary-entity-marking.md) landing first (or alongside in the same release). Multiple strategic-model generators — SWOT subject selection, Magic Quadrant primary-plot, Lean Canvas customer-segments lead, Segment Profile target persona — need to pick a default representative entity from a set, which the `primary` boolean field resolves. Without it, generators fall back to alphabetical-by-id sort, which produces wrong results whenever entity names don't sort by priority.

---

## 1. Overview

A new typed-node concept that turns the vault's typed-graph backbone into **company intelligence**. A `strategic-model` node is a typed record that consumes other typed records — competitor IFU history, regulatory clearances, pillar nodes, risk insights, customer interviews, market shifts — and renders to a deliverable artifact (SWOT, Lean Canvas, BMC, Porter's 5, Segment Profile, Magic Quadrant).

Update one underlying node and the strategic-model regenerates with a meaningful diff.

## 2. Why this is the v1.x lead candidate

- **No competitor combines** typed-node-graph + generated-strategic-models + medical-device-aware schema. Aha! ships templates; Tana ships supertags you build yourself; Notion ships AI drafting. None ships *strategic models as typed records that recompute from underlying intelligence*.
- **It compounds existing work.** Every node type already in the schema (competitor, persona, pillar, decision, requirement, metric, indication-for-use, regulatory-clearance) becomes a potential input.
- **It is the dogfood demo.** A founder running `cb render swot --competitor-set top-5` after a `research-agent` run produces a credible SWOT in 90 seconds. That's the v1.0 launch demo.
- **It is medtech-extensible.** SWOT for a medical-device company can pull IFU drift, predicate-chain risk, and 510(k) cleared population — strategic-model machinery that no general-purpose product-management tool can match within 12 months.

## 3. The new node type

### 3.1 Definition

| Property | Value |
|---|---|
| `name` | `strategic-model` |
| `category` | `entity` (new category? `synthesis` would be more accurate but introduces a new category. Provisionally `entity`.) |
| `folder` | `entities/strategic-models/` |
| `profile` | `null` (available in all profiles) |

### 3.2 Required frontmatter (beyond base schema)

| Field | Type | Description |
|---|---|---|
| `model` | string | Discriminator. One of: `swot`, `lean-canvas`, `business-model-canvas`, `porters-5-forces`, `segment-profile`, `magic-quadrant`. |
| `subject` | string | What the model is about. Free-form for v1.x (e.g., "company-brain", "our medical device wearable", "our entry into the cardiology market"). Constrains the scope of input-node selection. |
| `as_of` | date | The "snapshot date" the model represents. Strategic models are point-in-time artifacts; the `as_of` date lets a user produce a Q1 2026 SWOT and a Q3 2026 SWOT and diff them. |

### 3.3 Model-specific frontmatter

Some models require additional parameters:

**`magic-quadrant`:**
| Field | Type | Description |
|---|---|---|
| `x_axis_label` | string | E.g., "Completeness of vision" |
| `y_axis_label` | string | E.g., "Ability to execute" |
| `x_axis_low_high` | list[string, string] | E.g., `["Niche players", "Visionaries"]` |
| `y_axis_low_high` | list[string, string] | E.g., `["Challengers", "Leaders"]` |
| `entries` | list[dict] | List of `{node_id, x_score, y_score, note}` for each entity plotted. Manually scored or partially auto-scored from competitor metrics. |

**`porters-5-forces`:**
| Field | Type | Description |
|---|---|---|
| `industry` | string | Brief description of the industry being analyzed. |

### 3.4 Edges

A `strategic-model` node uses standard typed edges:

- `derived_from` → every source node that informed the model. Mandatory provenance.
- `consumes` (new edge type?) → every typed entity node (competitor, persona, pillar, etc.) that fed the model. Lets `cb render` walk the graph deterministically.
- `preceded_by` / `followed_by` → for chained snapshots over time (Q1 SWOT preceded_by Q3 SWOT of same subject).
- `contradicts` → if this model contradicts a prior model on the same subject.

**Decision needed:** introduce a new `consumes` edge type? Or overload `derived_from`? The semantic difference matters — `derived_from` traditionally points to sources (provenance anchors), while a SWOT also depends on entity nodes (competitor, persona). For v1.x I lean toward overloading `derived_from` to keep edge types stable; a `consumes` edge type could land in v2 if the distinction proves load-bearing.

## 4. The six model variants

For each model: purpose, inputs, output structure, formats.

### 4.1 SWOT

**Purpose.** Classical strengths / weaknesses / opportunities / threats analysis on a defined subject.

**Inputs (default profile):**
- Strengths: pillar nodes with positive framing (`auto_inject: true`); product features; metric snapshots with positive trajectory.
- Weaknesses: anti-decisions (decisions with `## What This Rules Out`); non-goal pillars (interpreted as constraints); risk-insight nodes; gaps surfaced by `cb maintain audit`.
- Opportunities: market-data source nodes; competitor IFU expansions; customer-interview themes about unmet needs; press-release sources about adjacent market shifts.
- Threats: competitor nodes (especially recent IFU expansions, clearances, raises); regulatory-clearance nodes for competitors; risk-insight nodes flagged `threat-class`.

**Inputs (medical-device profile, additions):**
- Threats: competitor regulatory-clearance with predicate edges pointing at *our* planned filings; hazard nodes promoted to threats.
- Opportunities: IFU gaps (we cover an indication competitors don't); predicate-chain orphans (clearances with no follow-on).

**Output structure (markdown):**
- §1 Subject + as-of date
- §2 Strengths (cited node ids)
- §3 Weaknesses (cited node ids)
- §4 Opportunities (cited node ids)
- §5 Threats (cited node ids)
- §6 Implications (auto-generated short narrative: top 1 strength × top 1 opportunity = bet to pursue; top 1 weakness × top 1 threat = risk to mitigate)
- §7 Sources

**Output formats:** markdown, html, docx. Optional: 2x2 grid as SVG (deferred to v2 unless trivial).

### 4.2 Lean Canvas (Ash Maurya)

**Purpose.** One-page business model for startups; 9 blocks.

**Inputs:**
- Problem (top 3): pillar nodes about target-customer pains; customer-interview source themes.
- Customer Segments: persona nodes (primary first).
- Unique Value Proposition: positioning pillar; auto-inject pillars about what we sell.
- Solution (top 3): product nodes + their top features.
- Channels: pillar nodes about distribution; if absent, scaffold from a placeholder.
- Revenue Streams: pricing decisions; metric nodes with `volatility_class: low` related to revenue.
- Cost Structure: scaffold placeholder unless captured.
- Key Metrics: metric nodes flagged `top_line: true` (cf. update-brief design).
- Unfair Advantage: pillar nodes that articulate moat (open source, local-first, medtech profile in our case).

**Output structure (markdown):**
- A 9-cell block layout (markdown can use tables or sections).
- Each cell: 2-4 bullets with cited node ids.

**Output formats:** markdown, html. docx and a graphical layout deferred.

### 4.3 Business Model Canvas (Osterwalder)

**Purpose.** 9-block business model canvas.

**Inputs:** Largely overlapping with Lean Canvas. The differences are framing-only (BMC has Key Partnerships, Key Activities, Key Resources, Customer Relationships in place of Lean Canvas's Problem, Solution, Unfair Advantage).

- Customer Segments: persona nodes.
- Value Propositions: positioning pillars + product nodes.
- Channels: pillar nodes about distribution.
- Customer Relationships: scaffold placeholder unless captured.
- Revenue Streams: pricing decisions, revenue metrics.
- Key Resources: scaffold placeholder unless captured.
- Key Activities: scaffold placeholder unless captured.
- Key Partnerships: vendor nodes (existing entity type).
- Cost Structure: scaffold placeholder.

**Output structure (markdown):** 9-cell layout.

**Output formats:** markdown, html.

### 4.4 Porter's Five Forces

**Purpose.** Industry-level competitive analysis.

**Inputs:**
- Competitive Rivalry: competitor nodes (existing rivalry).
- Threat of New Entrants: any competitor nodes flagged with `tags: [emerging]`; market-data sources about funding events in the space.
- Threat of Substitutes: competitor nodes with `tags: [substitute]` or competitor nodes in adjacent categories (cross-category comparison).
- Bargaining Power of Buyers: persona + customer nodes (especially customer-interview source nodes about price sensitivity).
- Bargaining Power of Suppliers: vendor nodes (existing entity type).

**Output structure (markdown):**
- §1 Industry context
- §2-6 Each of the five forces with cited evidence
- §7 Implications (which force is currently most active; where the company is exposed)

**Output formats:** markdown, html.

### 4.5 Segment Profile

**Purpose.** Deep profile of a single defined customer segment.

**Inputs:**
- The persona node being profiled (single, required).
- Customer nodes that exemplify the persona.
- Customer-interview source nodes linked to the persona.
- Pillar nodes that govern how we serve this segment.
- Metric nodes flagged as segment-specific.

**Output structure (markdown):**
- §1 Segment summary (from persona)
- §2 Demographics + firmographics
- §3 Jobs-to-be-done (extracted from customer-interview themes)
- §4 Pains (from interview themes)
- §5 Gains (from interview themes)
- §6 How we serve them (from pillars + product features)
- §7 What we deliberately don't try to be for this segment (from non-goal pillars)
- §8 Sources

**Output formats:** markdown, html, docx.

### 4.6 Magic Quadrant

**Purpose.** 2x2 grid plotting multiple competitors (including us) on two user-chosen axes.

**Inputs:**
- A set of competitor nodes (passed via `--competitor-set` or `--include-competitors`).
- Optionally our product node (we plot ourselves too).
- The two axes (from frontmatter — see §3.3 above).
- Scoring: manual per-entry in frontmatter for v1.x. v2 may auto-score from competitor frontmatter fields (e.g., funding stage, IFU breadth, regulatory posture).

**Output structure:**
- §1 Quadrant overview + axis definitions
- §2 SVG quadrant visualization (this is the differentiator — the chart itself, not just text)
- §3 Per-entry commentary (each plotted entity with 2-3 bullets of rationale)
- §4 Sources

**Output formats:** html (SVG inline), markdown (text-only fallback with axis-position descriptions), docx (SVG-as-image).

The SVG rendering reuses `visualize` skill machinery — same D3 v7 dependency, similar self-contained-HTML pattern.

## 5. CLI surface

```
cb render swot                  --subject <subject>  [--as-of <date>]  [-o path]  [-f markdown|html|docx]
cb render lean-canvas           --subject <subject>  [--as-of <date>]  [-o path]  [-f markdown|html]
cb render business-model-canvas --subject <subject>  [--as-of <date>]  [-o path]  [-f markdown|html]
cb render porters-5-forces      --industry <name>    [--as-of <date>]  [-o path]  [-f markdown|html]
cb render segment-profile       --persona <id>       [--as-of <date>]  [-o path]  [-f markdown|html|docx]
cb render magic-quadrant        --model-node <id>                      [-o path]  [-f html|markdown|docx]
```

`--model-node <id>` for magic-quadrant references a hand-curated `strategic-model` node (because the axes and scoring must be specified somewhere); for other models, the node is auto-created in-place from the inputs at render time and persisted in `entities/strategic-models/` so future regenerations diff cleanly.

## 6. Intake flow

A new `intake` sub-mode: `strategic-model`. Conversational flow:

1. Skill asks: "Which model are you building? (swot / lean-canvas / bmc / porters-5 / segment-profile / magic-quadrant)"
2. Skill asks: "What is the subject? (product, market, segment, competitive landscape)"
3. Skill walks the relevant input node types and proposes a draft, presenting the cited inputs as a batched table.
4. User accepts / edits / rejects each input.
5. Skill writes the `strategic-model` node and offers to render.

For magic-quadrant specifically, the intake flow includes interactive axis-definition and scoring (the conversational equivalent of filling in `x_axis_label`, `y_axis_label`, `entries[]`).

## 7. Profile awareness

The `default` profile generates all six models using only universal entity types.

The `medical-device` profile extends three of the six:

- **SWOT** — Threats and Opportunities pull from `indication-for-use`, `regulatory-clearance`, `hazard` nodes when present.
- **Magic Quadrant** — competitor scoring can include axes like "IFU breadth" or "predicate-chain depth" that only make sense for medical device.
- **Lean Canvas / BMC** — Channels can include "FDA cleared submission pathway" as a regulated channel.

Non-medical-device profiles see no medtech vocabulary in their generated models (consistent with §8 of the PRD on profile-awareness).

## 8. Idempotency

Same vault state + same `--as-of` date = byte-identical output, modulo the timestamp footer. This makes `git diff exports/` meaningful — a SWOT diff shows what *changed* in the underlying intelligence, not "the doc got regenerated."

The `strategic-model` node itself is mutable — re-running `cb render swot --subject X` with new inputs updates the persisted node. To snapshot at a moment, use `--as-of 2026-Q2-snapshot` which creates a new node `strategic-model-swot-X-2026-Q2-snapshot.md` distinct from the rolling one.

## 9. Implementation milestones

Suggested sequence within v1.x:

1. **Schema extension.** Add `strategic-model` node type + folder + required fields + edge semantics. Update `FRONTMATTER-SCHEMA.md` rendering. ~1 day.
2. **SWOT generator.** Markdown template + input-walking logic + tests. ~3 days.
3. **Lean Canvas + BMC.** Adjacent in input shape; share a 9-cell-layout template. ~3 days.
4. **Porter's 5 Forces + Segment Profile.** Each ~2 days. ~4 days total.
5. **Magic Quadrant including SVG renderer.** ~4 days. Most complex.
6. **`intake strategic-model` sub-mode.** ~3 days.
7. **Profile-conditional extensions (medical-device).** ~2 days.
8. **Integration tests on meddev-fictional + saas-fictional + company-brain-itself vaults.** ~2 days.

**Total estimate:** ~22 working days. Land as v1.1.0 if research-agent ships in v1.0 (so the demo is intact at release), or as v1.0 if released earlier.

## 10. Test cases

Each example vault should produce at minimum:

- **meddev-fictional/exports/SWOT-vitalisens.md** — SWOT for the fictional ambulatory cardiac monitor. Threats include the competitor IFU expansion captured in that vault.
- **saas-fictional/exports/lean-canvas-loftwing.md** — Lean Canvas for the fictional engineering analytics product.
- **company-brain-vault/exports/SWOT-company-brain.md** — SWOT of company-brain itself, generated by us, used in our own launch.
- **company-brain-vault/exports/magic-quadrant-knowledge-tools.md** — Magic quadrant plotting company-brain, GBrain, Tana, Decision Graph, Aha! on user-chosen axes.

The last one is the launch-day demo.

## 11. Open questions

1. **`consumes` edge type or overloaded `derived_from`?** (See §3.4.)
2. **Should `strategic-model` be a new node category (`synthesis`) or live under `entity`?** Conceptually it's a synthesis artifact, not a stand-alone entity. Decision needed before schema PR.
3. **Magic quadrant scoring — manual only in v1.x, or attempt partial auto-scoring from competitor frontmatter fields (funding stage, IFU breadth, etc.)?**
4. **Idempotency on `--as-of`.** When a user runs `cb render swot --subject X` without `--as-of`, does the output overwrite the previous SWOT, or append-with-timestamp? Recommendation: overwrite (mutable rolling), and require `--as-of` for snapshots.
5. **Primary entity selection** — **scoped and resolved** by [`spec-primary-entity-marking`](spec-primary-entity-marking.md), which proposes a `primary: bool` field on base frontmatter. Strategic-model generators inherit this mechanism and must not ship until it lands.
6. **The materiality field (from update-brief design)** — should strategic-model nodes carry it? Probably yes; lets `update-brief` surface strategic-model changes at the right audience tier.

## 12. Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 0.1.0 | 2026-05-26 | nemock + Claude | Initial spec. Locks the design for the v1.x lead candidate identified in the Aha! deep-dive. Six model variants specified with inputs, outputs, formats. Implementation milestones sketched. Six open questions to resolve before code lands. |
