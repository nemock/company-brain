---
name: maintain
description: Audit and repair a company-brain vault. cb maintain repair auto-fixes filename-id mismatch, missing inverse edges (preceded_by ↔ followed_by), and missing controlled_document:false on risk/IFU nodes; it also regenerates _system/INDEX.md and refreshes the auto-section of the vault-level README.md (between cb:auto markers). cb maintain decay applies half-life confidence decay to fact snapshots linked to volatile metrics. cb maintain rebuild-index regenerates _system/INDEX.md only. cb maintain rebuild-readme regenerates the README auto-section only. cb maintain audit reports vault health read-only. cb validate --fix wires the repair pass into validation.
---

# maintain

This skill keeps a vault healthy as it grows. Where `validate` reports issues, `maintain` fixes the ones that can be fixed without a human call — and surfaces the rest for you to address via `intake` or hand-editing.

You do not invent edges. You do not silently rewrite confidence away from the original. You do not flip `controlled_document` from true to false. Every change has a defined repair rule.

## Before any maintenance

1. **Confirm the vault path.** Default: current working directory. Refuse if `_system/PROFILE.md` is missing.
2. **Run `cb validate --path <vault>` first.** Get a baseline. Note which errors are repair-eligible (filename-id, missing inverse, missing controlled_document) and which need human input (duplicate ids, unknown types, broken edge targets, missing required fields).
3. **Run `cb maintain audit --path <vault>`.** Read-only preview of what `repair` and `decay` would do. Use this to set expectations with the user before writing anything.

## Capabilities

### Auto-repair (`cb maintain repair`)

Fixes three classes of issue:

1. **Filename-id mismatch.** A node whose file is named `pillar-foo.md` but whose frontmatter id is `pillar-bar` gets renamed to `pillar-bar.md`. Skipped if the target name already exists (won't clobber).
2. **Missing inverse edges.** The schema declares one inverse pair: `preceded_by` ↔ `followed_by`. When A has `preceded_by: B` but B has no `followed_by: A`, the inverse is auto-added with `note: "auto-added inverse of preceded_by from <A>"`. Other edge types have no declared inverse — maintain does not invent one.
3. **Missing `controlled_document: false` on risk/IFU nodes.** Nodes under `risk/` or `entities/indications-for-use/` carry an affirmative `controlled_document: false`. When the field is *absent*, `maintain` sets it to false. When the field is present (even if true), `maintain` leaves it alone — the boundary is a safety rail and never gets silently flipped.

Always regenerates `_system/INDEX.md` at the end of the pass. Idempotent — re-running on an already-repaired vault is a no-op (modulo the INDEX.md rewrite).

```bash
cb maintain repair --path <vault>           # fix and write
cb maintain repair --path <vault> --dry-run # preview without writing
cb validate --path <vault> --fix            # equivalent: repair then validate
```

### Confidence decay (`cb maintain decay`)

Fact nodes with a `metric_id` link to a `metric` whose `volatility_class` is `low` / `medium` / `high`. As time passes since `verified_at`, the snapshot becomes less likely to still hold. Maintain applies half-life decay:

- **low** (changes annually): half-life 24 months
- **medium** (changes quarterly): half-life 6 months
- **high** (changes monthly or faster): half-life 1 month

Formula: `new_confidence = original_confidence * 0.5 ** (age_months / half_life)`. Rounded to 3 decimal places.

The **original confidence is preserved** in a new `confidence_original` field on first decay so re-runs always compute from the original. Without this, repeated decays would compound and confidence would race to zero.

```bash
cb maintain decay --path <vault>
cb maintain decay --path <vault> --today 2027-01-01   # pin reference date
cb maintain decay --path <vault> --dry-run
```

When to run: weekly or monthly cadence is typical. After a long pause in vault activity, run decay before generating any documents so the MRD's evidence-vs-vision section reflects current confidence.

### Audit (`cb maintain audit`)

Read-only health summary. Same data `repair` and `decay` would surface, plus general findings:

- `vault-size` — node count and type count.
- `no-sources` (notice) — vault has no source nodes. Claims will have no provenance; the MRD's "Uncited claims" section will be large.
- `no-pillars` (notice) — vault has no pillars. `query` has nothing to auto-inject.

```bash
cb maintain audit --path <vault>
```

Use this when checking on someone else's vault before suggesting changes — it shows what's repairable vs. what needs attention without touching anything.

### Index regeneration (`cb maintain rebuild-index`)

Just rewrites `<vault>/_system/INDEX.md`. Same logic that runs at the end of `repair`, exposed for cases where you want to refresh the index without touching anything else.

```bash
cb maintain rebuild-index --path <vault>
```

The vault's `_system/INDEX.md` is gitignored at the vault level — it's a regenerated artifact, not committed history. Always reflects the current node set.

### README auto-section regeneration (`cb maintain rebuild-readme`)

The vault-level `README.md` has an auto-section bracketed by `<!-- cb:auto START -->` and `<!-- cb:auto END -->` markers. The section shows current vault state: node count, governing pillars (auto-injected), non-goal pillars, products, competitors, and a table of files in `exports/`. Hand edits **inside** the markers are overwritten; everything **outside** is preserved.

```bash
cb maintain rebuild-readme --path <vault>
cb maintain rebuild-readme --path <vault> --dry-run
```

`cb maintain repair` calls this silently and skips cleanly if the markers aren't present (e.g. on an older vault scaffolded before this feature landed). The dedicated `rebuild-readme` command errors loudly with a suggestion to run `cb scaffold --force` if the markers are missing — useful for diagnosing why the auto-section didn't update.

`cb scaffold --force` regenerates the whole README from the current scaffold template, which **overwrites hand edits outside the markers**. Use it for a periodic refresh after a company-brain upgrade; commit first so you can recover the lost hand edits if needed.

## What this skill does NOT do

- Does not resolve **duplicate ids**, **unknown node types**, **folder-type mismatches**, **missing required fields**, **broken edge targets**, **profile mismatches**. All need a human call. Surface them via `validate`; ask the user how to proceed.
- Does not remove or comment out edges. If an edge target doesn't resolve, that's information loss waiting to happen — surface it, don't fix it.
- Does not touch frontmatter fields not in the schema (forward-compat experiments stay intact).
- Does not flip `controlled_document` from true to false. Even when it would be technically correct (e.g. a node landed under `risk/` with `controlled_document: true`), maintain leaves it for the user to address.
- Does not commit. The user decides when to commit the changes. After running `repair` or `decay`, surface the diff and ask if they want it committed.

## What to do when something goes wrong

- **`cb maintain repair` made changes you didn't expect.** Run `git diff` (the vault is a git repo). Every change has a `code` and `detail` in the output — match them up. Roll back with `git restore .` if needed.
- **`cb validate` still errors after `--fix`.** Those errors are the ones outside maintain's auto-fix scope. Read the error codes, address each via `intake` or hand-edit, then re-validate.
- **A decayed confidence looks wrong.** Check the metric's `volatility_class` — a metric tagged `high` decays fast. If the metric should be `medium` or `low`, edit the metric's frontmatter and re-run `decay`.
- **The user wants different half-life numbers.** The current values are PRD §14 defaults. If they need to be tuned per vault, that's a v0.5+ enhancement — flag it but don't hack a one-off.

## After maintenance

- Run `cb validate --path <vault>` again. Confirm error count went down.
- Tell the user what changed (count + classes of fix). Offer to commit if the vault is a git repo.
- If you just ran `decay`, regenerate any open exports (`cb render mrd`, `cb render one-pager`) so the freshly-decayed confidences show up.
