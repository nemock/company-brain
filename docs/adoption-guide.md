# Adoption Guide

A step-by-step walkthrough from `uv tool install` to your first generated MRD. Targets a fresh user who has never seen company-brain before.

If you finish this guide and your vault validates clean, you have completed the v1 onboarding success criterion (PRD §19).

## 1. Install

You need [uv](https://docs.astral.sh/uv/) (Python package and tool manager) and `git`.

```bash
uv tool install git+https://github.com/nemock/company-brain
cb --version            # → 0.5.0 (or later)
cb install-skills       # symlinks the seven skills into ~/.claude/skills/
```

If you don't use Claude Code, you don't need `cb install-skills` — every workflow below works with `cb` alone.

## 2. Pick a profile

company-brain ships two profiles:

- **`medical-device`** — adds `indication-for-use`, `regulatory-clearance`, `risk-insight`, `hazard`, `hazardous-situation`, `harm`, `risk-control-idea`, `regulation`, `standard` node types and ISO-14971-vocabulary intake sub-modes. Generated docs carry a controlled-document-boundary footer.
- **`default`** — industry-agnostic. Just the universal types. No regulatory machinery.

If you are not a medical-device company, use `default`. You can see the differences side-by-side in [`examples/meddev-fictional/`](../examples/meddev-fictional/) (medical-device) and [`examples/saas-fictional/`](../examples/saas-fictional/) (default).

## 3. Scaffold a vault

```bash
cb scaffold --profile default --path ~/work/acme-vault
cd ~/work/acme-vault
```

This creates the folder tree, the schema reference docs in `_system/`, a `_branding/` starter, an empty `_attachments/` and `exports/`, a `.gitignore`, a `README.md`, and (by default) runs `git init` with an initial commit. Pass `--no-git` if you want to set up git yourself or live without it.

The scaffold is idempotent — running it again is safe. Pass `--force` to regenerate the `_system/*.md` reference files after a company-brain upgrade.

## 4. Capture your first knowledge

Two paths, often used together:

### Interactive intake (Claude Code)

In a Claude Code session inside your vault directory, ask:

> Let's do a vision intake. I'll dictate.

The `intake` skill runs the six-phase flow: open capture → immutable source node → nugget extraction (batched table) → review loop → write and link → anti-decision sweep. End-of-session output is a set of typed node files with `derived_from` edges pointing back to the source.

Other intake sub-modes: `product`, `persona`, `competitor`, `metric`, `meeting-notes`, `risk` (medical-device).

### Atomize an existing document

If you already have a project initiation document, an FDA 510(k) summary, an interview transcript, or a competitor screenshot:

> Atomize `~/Downloads/project-init.docx` into this vault.

The `atomize` skill reads the file (via `cb extract` for binary formats, Claude vision for images, direct read for markdown/text), writes a source node holding the verbatim content, and proposes typed derived nodes for your review.

After either path:

```bash
cb validate                            # check schema compliance
cb maintain audit                      # read-only health check
cb maintain repair                     # auto-fix what can be fixed
```

## 5. Query the graph

> What are our pricing principles?

The `query` skill loads auto-injecting pillars first, then walks typed edges to assemble a cited answer. Direct CLI access:

```bash
cb list-nodes --auto-inject-only       # all governing pillars
cb list-nodes --type decision
cb get-node decision-001-online-only   # one node + edges both directions
```

## 6. Generate your first MRD

```bash
cb render mrd                          # markdown → exports/MRD.md
cb render mrd --format html
cb render mrd --format docx
```

The MRD is profile-aware. A `default` profile MRD has nine sections (executive summary, vision and positioning, market and personas, market requirements, competitive landscape, evidence vs. vision split, open questions, what we are explicitly not doing, sources). A `medical-device` MRD adds two more: indications for use (§3) and regulatory landscape (§7).

## 7. See the graph

```bash
cb viewer                              # → vault-graph.html
open vault-graph.html                  # macOS; or use your browser
```

Force-directed D3 layout, color by node type, hover for tooltip, click for detail. For medical-device vaults, `--mode ifu-chain` and `--mode predicate-tree` give focused views.

## 8. Push to git

The vault is already a git repo (assuming you didn't pass `--no-git`). Add a remote and push:

```bash
git remote add origin <your-git-host>:your-org/acme-vault.git
git push -u origin main
```

Teammates clone the repo. Without company-brain installed they can still browse the vault in Obsidian or any markdown viewer and read the latest `exports/MRD.md`. With company-brain installed, they can `intake` and `atomize` from their own machine and push back.

## 9. Periodic maintenance

```bash
cb maintain repair                     # auto-fix missing inverse edges, etc.
cb maintain decay                      # apply confidence decay to fact snapshots
cb maintain rebuild-index              # regenerate _system/INDEX.md
```

Run after intake sessions or before publishing a refreshed MRD.

## Done

If `cb validate` exits clean and `cb render mrd` produced a document with your captured pillars cited inline, you have a working vault and the onboarding success criterion is met.

For the full document menu (21 doc types — MRD, one-pager, PID, SRD/SRS/HRS, sales battle card, etc.) see [`skills/doc-generate/SKILL.md`](../skills/doc-generate/SKILL.md). For the schema itself see [`docs/schema.md`](schema.md). For the profile mechanism in detail see [`docs/profiles.md`](profiles.md).
