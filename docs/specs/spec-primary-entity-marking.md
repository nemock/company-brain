---
title: "Spec — `primary` frontmatter field for entity nodes"
status: draft
version: 0.1.0
date: 2026-05-26
target_milestone: "v1.x (prerequisite for spec-strategic-model)"
controlled_document: false
---

# Spec: `primary` frontmatter field for entity nodes

> **Purpose.** Resolve the generator-side ambiguity where multiple entities of the same type (persona, product, competitor, etc.) exist in a vault and a generator must pick one as representative. Currently generators sort alphabetically by node id, which produces wrong results when names don't disambiguate by priority.
>
> **Target milestone.** v1.x — **must land before or alongside `spec-strategic-model`** because multiple strategic-model generators depend on this mechanism (SWOT subject selection, Magic Quadrant primary-plot, Lean Canvas customer segments).
>
> **Origin.** Surfaced 2026-05-26 during meta-vault dogfooding. The one-pager generator picked `persona-fractional-exec` instead of `persona-medtech-founder` due to alphabetical sort. After the personas were updated to Founder / Lead PM / Lead Marketing Manager, the bug became permanently visible: the auto-rendered MRD lists personas as Founder → Lead Marketing Manager → Lead Product Manager because `lead-m` < `lead-p` alphabetically.

---

## 1. The problem

Several `doc-generate` generators need to pick a single representative entity from a set:

| Generator | Selection it must make | Current behavior |
|---|---|---|
| `one-pager` | "Who it's for" persona | Alphabetical by id |
| `mrd` | §3 personas ordering | Alphabetical by id |
| `sales-battle-card` | Default competitor (when `--competitor` not passed) | First by id |
| `press-release` | Product / persona to lead with | Alphabetical by id |
| `onboarding-doc` | Primary persona, product, pillars to lead with | Alphabetical by id |
| `investor-update` | Top-line metrics to surface | Mixed |
| **(future) `swot`** | Subject if not passed via `--subject` | n/a — spec-strategic-model |
| **(future) `magic-quadrant`** | Default product to plot for "us" | n/a — spec-strategic-model |
| **(future) `lean-canvas`** | Primary persona for Customer Segments | n/a — spec-strategic-model |

The alphabetical fallback works when entities are named in priority order (e.g., `persona-01-…`, `persona-02-…`). It fails silently — with no warning, no error, no detection by `cb validate` — when entities are named semantically (`persona-founder`, `persona-lead-product-manager`, `persona-lead-marketing-manager`).

---

## 2. The proposed change

### 2.1 Schema

Add an optional `primary` boolean to the **base frontmatter schema**, available on every node type:

| Field | Type | Required? | Default | Description |
|---|---|---|---|---|
| `primary` | boolean | optional | `false` (or absent) | When `true`, generators prefer this node when selecting a representative from a set of nodes of the same type within the same namespace scope. |

Adding `primary` to base frontmatter (rather than per-type) means *any* entity type can use it: a primary `product`, a primary `persona`, a primary `competitor`, a primary `pillar` — and someday a primary `strategic-model`.

### 2.2 Generator behavior

For each generator that picks a representative entity from a set of N candidates:

1. **Filter by `primary: true`.** If exactly one match, use it.
2. **If multiple match,** use alphabetical-by-id among the primaries and emit a footer note: *"Multiple `<type>` nodes marked primary; selected `<id>` alphabetically."*
3. **If zero match,** fall back to alphabetical-by-id among all candidates and emit a footer note: *"No primary `<type>` marked; selected `<id>` by id sort."*

The fallback preserves backward compatibility with existing vaults that have no `primary` fields set.

### 2.3 Validator behavior

`cb validate` does **not** error or warn on missing primaries — backward-compatible by default.

`cb validate --strict` (new optional flag) emits a warning when:
- More than one node of the same `(type, namespace)` has `primary: true`.
- A generator with primary-entity selection has been rendered into `exports/` but no entity of the relevant type is marked primary in the vault.

### 2.4 Intake / scaffold behavior

- `vault-architect` doesn't auto-set `primary` (the scaffolded vault has no entities yet).
- `intake` sets `primary: true` on the first entity of a given type captured in a session (the user can override).
- Subsequent entities of the same type default to `primary: false` and require explicit `--make-primary` to be promoted.

### 2.5 Multiple-primaries-per-namespace policy

Within a single `(type, namespace)` pair, only one node should be `primary: true`. The validator warns on violations in `--strict` mode but does not error — there are legitimate reasons to temporarily have two (e.g., during a transitional refresh of the primary persona). The render emits a footer note so the situation is visible in output.

---

## 3. Implementation milestones

| # | Task | Estimate |
|---|---|---|
| 1 | **Schema extension.** Add `primary` to base frontmatter in `src/company_brain/schema/frontmatter.py`. Update `FRONTMATTER-SCHEMA.md` rendering. | ~½ day |
| 2 | **Validator pass.** Add `--strict` flag and the two new warnings. | ~½ day |
| 3 | **Generator updates.** one-pager, MRD persona section, sales-battle-card, press-release, onboarding-doc. | ~1 day |
| 4 | **`intake` skill update.** Default first-entity-of-type to `primary: true`; expose `--make-primary` flag. | ~½ day |
| 5 | **Tests.** Update example vault renders (meddev-fictional, saas-fictional, company-brain-itself) to set `primary: true` on intended primaries; verify outputs change accordingly. | ~½ day |

**Total estimate:** ~3 working days. Land as a hygiene release (target `v0.8.0`) before implementation of `spec-strategic-model` begins.

---

## 4. Test cases

1. **`meddev-fictional` vault** — mark `persona-cardiac-monitor-clinician` (or equivalent) as `primary: true`. Re-render one-pager and MRD; confirm correct persona surfaces in §3 lead position.
2. **`saas-fictional` vault** — same pattern.
3. **`company-brain-itself` vault** — set `primary: true` on `persona-founder`, `product-company-brain`, `competitor-gbrain` (top threat). Re-render MRD; confirm Founder leads the personas, GBrain is the default sales-battle-card competitor.
4. **Multiple primaries** — mark two competitors as `primary: true` in the same namespace. `cb validate --strict` emits a warning; render still produces a deterministic output (alphabetical among primaries) with a footer note.
5. **Backward compatibility** — existing vault with no `primary` fields produces byte-identical output to the pre-change render, modulo the new footer note about no-primary-marked.
6. **Override at render time** — `cb render sales-battle-card --competitor competitor-x` ignores `primary` field and uses the passed argument. (Explicit CLI flag wins over frontmatter.)

---

## 5. Open questions

1. **Should `primary` be scoped by namespace, or globally?** Recommendation: scoped by `(type, namespace)`. A vault can have `primary: true` for one persona in the `market` namespace and one persona in the `partners` namespace without conflict.
2. **Multi-tier priority (e.g., `priority: 1 / 2 / 3`) instead of a boolean?** Out of scope for v1.x. Revisit if the boolean proves insufficient. The materiality field from `spec-update-brief` might absorb this responsibility instead.
3. **What about edge ordering, not just node selection?** Out of scope. Edges already have a `weight` field that plays a similar role for ordering linked nodes.
4. **Should the validator block a render that produces a "no primary marked" warning?** Recommendation: no — the soft fallback (alphabetical) preserves backward compatibility. Failing the render would break every pre-change vault on first re-render.

---

## 6. Relationship to other specs

- **[`spec-strategic-model`](spec-strategic-model.md)** — depends on this; SWOT, Magic Quadrant, and Lean Canvas generators all need primary-entity selection.
- **[`spec-research-agent`](spec-research-agent.md)** — does not directly depend on this, but research-agent's competitor-disambiguation logic could leverage `primary: true` for "the competitor we currently care most about" when refreshing a known landscape.
- **`update-brief-design`** (lives in the project's planning folder alongside the MRD and competitive brief, not in this repo) — the `materiality` field proposed there is conceptually orthogonal but adjacent. Both fields can coexist on the same node (one for "is this the representative one?", one for "how prominent is it in audience-filtered briefs?").

---

## 7. Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 0.1.0 | 2026-05-26 | nemock + Claude | Initial spec. Documents the primary-entity-marking gap surfaced during meta-vault dogfooding, proposes the `primary` boolean field, defines generator and validator behavior, sketches ~3-day implementation. Prerequisite for spec-strategic-model. |
