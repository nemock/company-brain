---
name: doc-generate
description: Generate planning documents from a company-brain vault. v0.3.0 ships the full MRD (markdown / html / docx) and one-pager (markdown / html) generators. Profile-aware - medical-device sections (IFU, regulatory landscape) are included only when the active profile is medical-device. The 19 scaffolded generators (PID, business plan, competitive brief, risk brainstorm, sales battle card, decision log, SRD/SRS/HRS, etc.) ship in v0.4.0.
---

# doc-generate

This skill turns the typed vault into planning documents. The vault is the source of truth; the documents are derived artifacts you can regenerate any time and that get committed under `<vault>/exports/`.

You do not write document content by hand. The generators read the schema, pull the right typed nodes, and emit consistent, profile-aware output. Your job is to invoke the right `cb render` command and surface any issues to the user.

## Before any render

1. **Confirm the vault path.** Default: current working directory. Refuse politely if there is no `_system/PROFILE.md` — that's the marker of a vault.
2. **Run `cb validate --path <vault>` first.** A vault with errors will still render, but uncited claims and broken edges will surface in the output. If validate reports errors, tell the user and offer to fix them via `intake` or `atomize` before generating.
3. **Confirm the active profile.** Run `cb describe-profile --path <vault>` to know whether medical-device-only sections will appear. The profile decides which sections render.

## What ships in v0.3.0

| Document | Markdown | HTML | DOCX | Status |
|---|:-:|:-:|:-:|---|
| Marketing Requirements Document (MRD) | ✅ | ✅ | ✅ | Full |
| One-pager | ✅ | ✅ | — | Full |
| PID (Project Initiation Document) | | | | Scaffold in v0.4.0 |
| Business Plan | | | | Scaffold in v0.4.0 |
| Sales battle card (per competitor) | | | | Scaffold in v0.4.0 |
| Competitive brief | | | | Scaffold in v0.4.0 |
| IFU comparison report (med-device) | | | | Scaffold in v0.4.0 |
| Decision log / ADR roll-up | | | | Scaffold in v0.4.0 |
| Risk brainstorm (med-device) | | | | Scaffold in v0.4.0 |
| 11 more PMBOK / engineering doc types | | | | Scaffold in v0.4.0 |

The one-pager does **not** ship a docx writer (PRD §11 — a one-page leave-behind is better as markdown or html). All other v0.4.0 scaffolds will support markdown at minimum.

## Rendering

```
cb render <doc> [--path <vault>] [--out <file>] [--format markdown|html|docx]
```

### MRD

```
cb render mrd                                     # markdown → <vault>/exports/MRD.md
cb render mrd --format html                       # HTML     → <vault>/exports/MRD.html
cb render mrd --format docx                       # DOCX     → <vault>/exports/MRD.docx
cb render mrd --out /tmp/board-mrd.md             # custom path
```

The MRD has the section structure documented in PRD §11. Profile-conditional sections (IFU, Regulatory landscape) are omitted entirely when the active profile isn't medical-device — not rendered empty, not stubbed out.

### One-pager

```
cb render one-pager                                # markdown → <vault>/exports/one-pager.md
cb render one-pager --format html                  # HTML     → <vault>/exports/one-pager.html
```

The one-pager picks: the first product by id, the highest-confidence positive pillar (non-goal-excluded), the first persona, the feature most related to the primary product, and the first customer-interview source. When any of those is missing, the section degrades to a hint like "Run `intake persona` to define one."

## What this skill does NOT do

- Does not modify vault nodes. For knowledge capture, use the `intake` skill. For document ingestion, use `atomize`.
- Does not push to git. The user (or their team) decides when to commit `exports/`. If they want a commit, ask first and propose a structured message naming what got regenerated.
- Does not bypass the controlled-document boundary. The MRD and one-pager are planning artifacts. When the active profile is `medical-device`, every generated document carries the footer:

  > This is a planning artifact. It is not a controlled document and is not part of any design history file, risk management file, or traceability matrix per ISO 14971, IEC 62304, or 21 CFR 820.

  Do not strip that footer. If the user asks for a controlled document, refuse and explain — company-brain is for the layer above the QMS.
- Does not invent content. If a section reads sparsely (e.g. "No personas captured yet"), the right answer is to run `intake persona` and re-render, not to hand-edit the output.

## Branding integration

The generators read from `<vault>/_branding/`:

- `colors.yaml` — palette (primary, secondary, accent, text, background, muted) + typography (`font_family_headings`, `font_family_body`). Defaults are used for any field not set.
- `logo.png` / `logo.jpg` / `logo.svg` — picked up if present. The HTML wrapper does not currently embed it; the docx writer does not currently embed it. Both are intentional v0.3.0 simplifications and can be lifted later.
- `templates/<doc>.md.j2` — overrides the bundled template by name. A vault that drops a custom `mrd.md.j2` here gets full control over MRD content shape without changing the codebase.
- `templates/html-wrapper.html.j2` — overrides the bundled HTML shell. A vault can wrap its docs in its own page chrome (header, nav, custom CSS) without touching company-brain.

## Idempotency

Re-running a generator on an unchanged vault produces **byte-identical output modulo the single generation-date line in the footer**. This is the contract:

- The same vault + the same `--date` flag → identical markdown bytes, identical HTML bytes.
- DOCX files have inherent zip-metadata variability, but the visible paragraph and table content is identical (the round-trip test asserts this).
- This is what makes git diffs on `exports/` meaningful — you can tell what *content* changed by reading the diff, not just "the docs regenerated."

If you generate a doc, the user makes some vault changes via `intake`, and you regenerate, the diff in `exports/MRD.md` shows exactly which sections the new nodes affected. That's the whole point.

## After rendering

- Report the output path and size to the user.
- If `cb validate` had errors before render, remind the user to fix them.
- If the user wants the docs committed, ask first, then `git add exports/ && git commit -m "Regenerate MRD and one-pager"`. Don't push.

## What to do when something goes wrong

- **`cb render` fails with `VaultNotFoundError`.** The path isn't a vault. Confirm `_system/PROFILE.md` exists.
- **`cb render` fails with `template not found`.** A vault override at `_branding/templates/` may have a syntax error; check the file. If no override exists, the bundled template is missing — reinstall company-brain.
- **Output reads sparsely.** The vault is sparse for the doc's input set. Don't paper over it — surface the gaps. For the MRD, the "Uncited claims" subsection in §8 is the authoritative list of nodes lacking sources.
- **A non-goal pillar shows in the wrong section.** Non-goal classification is by `tag: non-goal` (primary) or title prefix `"Non-Goal"` (fallback). If a pillar should be classified as non-goal but isn't, add the tag and re-render.
- **The docx is missing formatting you expected.** The docx writer covers headings, paragraphs, bullets, blockquotes, tables, and inline bold/code. Ordered lists, nested lists, fenced code, and links pass through as plain text. If you need more, raise an issue rather than hand-editing the docx.
