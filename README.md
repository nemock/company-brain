# company-brain

> ⚠️ **Pre-1.0, under active development.** APIs, schema, and skill interfaces will change without notice. Watch [ROADMAP.md](ROADMAP.md) for milestones.

An AI-native knowledge graph for companies — products, people, decisions, vision, evidence, competitive landscape — that lives in Obsidian-compatible markdown and lets agents retrieve cheaply from typed nodes and typed edges.

Built as a set of Claude Code skills plus a Python CLI (`cb`). Industry-agnostic core with an opt-in **medical-device** profile that adds indications-for-use, regulatory clearances, and ISO-14971-vocabulary risk nodes — all explicitly **above** any design controls layer.

## Status

Current milestone: **v0.3.0 — Query, MRD, and one-pager.** The pipeline now goes end-to-end: scaffold a vault, capture knowledge via `intake`, ingest existing docs via `atomize`, query the graph via `query`, generate a real MRD or one-pager via `doc-generate`.

- [PRD.md](PRD.md) — full design spec.
- [ROADMAP.md](ROADMAP.md) — milestone sequencing.
- [docs/controlled-document-boundary.md](docs/controlled-document-boundary.md) — what company-brain is **not**.

## Install

```bash
uv tool install git+https://github.com/nemock/company-brain
cb install-skills           # symlinks the seven skills into ~/.claude/skills/
cb --version                # → 0.3.0
```

Local dev:

```bash
git clone https://github.com/nemock/company-brain && cd company-brain
uv tool install . --reinstall
cb install-skills --source .
```

## The seven skills

| Skill | What it does |
|---|---|
| [`vault-architect`](skills/vault-architect/SKILL.md) | Scaffold a new vault (`cb scaffold`). Runs once per company. |
| [`intake`](skills/intake/SKILL.md) | Conversational capture into typed nodes. Sub-modes: vision, product, persona, competitor, competitor-ifu, competitor-clearance, competitor-snapshot, metric, meeting-notes, risk, clearance. |
| [`atomize`](skills/atomize/SKILL.md) | Ingest existing docs (markdown, Word, PDF, transcripts, image screenshots) into typed nodes with provenance. |
| [`query`](skills/query/SKILL.md) | Answer questions against the graph. Auto-injects pillars, walks typed edges, cites node ids, flags vision-vs-evidence and staleness. |
| [`doc-generate`](skills/doc-generate/SKILL.md) | Render planning documents from the graph. v0.3.0 ships **MRD** (md / html / docx) and **one-pager** (md / html). |
| `maintain` | _Placeholder, lands v0.4.0._ Confidence decay, broken-edge repair, INDEX.md drift fix. |
| `visualize` | _Placeholder, lands v0.4.0._ D3 HTML viewer with IFU-chain and predicate-tree views. |

## The CLI

```
cb --help                                    # list subcommands
cb --version
cb scaffold        --profile <name>          # create a vault
cb validate                                  # check the vault against the schema
cb describe-profile                          # JSON description of the active profile
cb describe-node   <type>                    # JSON description of one node type
cb extract         <file.docx|file.pdf>      # text extraction for atomize
cb list-nodes      [filters]                 # JSON summary of nodes (for query)
cb get-node        <id>                      # JSON node + inbound/outbound edges
cb render          <doc>  [--format ...]     # generate MRD or one-pager
cb install-skills                            # symlink skills into ~/.claude/skills
```

## What you can ask the skills to do

Everything below works in any Claude Code conversation. The skill loader matches your wording against each skill's description, so plain English works — you do not need to type `/skill-name` (though you can).

If you want to bypass the skills, every example has the equivalent `cb` command shown underneath.

### Bootstrap a new vault

> Scaffold a medical-device company-brain vault in `~/work/acme-medical`.

> Create a vault for a SaaS company in this folder. Default profile.

> Validate the vault.

```bash
cb scaffold --profile medical-device --path ~/work/acme-medical
cb scaffold --profile default --path .
cb validate --path .
```

### Capture knowledge (intake)

> Let's do a vision intake. I'll dictate.

> Capture a new product called "Acme Cardiac Monitor". It's a wearable; belongs to the cardiac product line.

> Capture a competitor: PulseGuard Medical at https://pulseguard-medical.example.com.

> Capture CardioTrace's 2025 IFU. Population is adult patients, condition is post-arrhythmia surveillance...

> Capture a 510(k) for K231234, CardioTrace Pro v2, cleared 2025-08-30, predicate is K181234.

> I just finished a meeting with the cardiology team. Here are the notes: ...

> Let's brainstorm risks for the pad-adhesion failure mode.

> Add a metric: "Pad attach rate at day 1", medium volatility.

The intake skill picks the right sub-mode from what you say. Every captured node lands in the right folder with the right frontmatter and a `derived_from` edge to a source node.

### Ingest existing documents (atomize)

> Atomize this PID Word doc into the vault: `~/Downloads/project-init.docx`.

> Ingest this 510(k) summary PDF and extract the clearance, IFU, and predicates: `~/Downloads/K231234.pdf`.

> Atomize this customer interview transcript: `~/transcripts/2026-04-12-nurse-anderson.txt`.

> Read this competitor product-page screenshot and capture it as a web-snapshot source: `~/screenshots/cardiotrace-2026-05-20.png`.

> Atomize the output of the competitor-profiling skill at `~/research/cardiotrace.md`.

Atomize handles binary formats via `cb extract`, images via Claude's native vision, and recognizes the structure of known skill outputs (competitor-profiling, customer-research, write-spec, etc.).

```bash
cb extract ~/Downloads/project-init.docx        # text only, for inspection
cb extract ~/Downloads/K231234.pdf
```

### Query the graph

> What are our pricing principles?

> Who are our competitors and which ones have the most recent clearances?

> How has CardioTrace's IFU evolved between their two 510(k)s?

> Why did we decide to be Rx-only?

> What are we explicitly NOT doing?

> What's the predicate chain for our planned K243189 filing?

> Which customer interviews informed the pad-attach-rate hypothesis?

> Which claims in the vault are vision-driven vs. evidence-driven?

The query skill loads the auto-injecting pillars first (so its answers are governed by the company's principles), then walks typed edges to find evidence. Every load-bearing claim cites a node id.

```bash
cb list-nodes --auto-inject-only                    # all governing pillars
cb list-nodes --type competitor
cb list-nodes --type decision --namespace regulatory
cb list-nodes --type source --source-kind fda-510k-summary
cb get-node pillar-no-pediatric-use                 # full node + edges both ways
cb get-node regulatory-clearance-K231234-cardiotrace-pro-v2
```

### Generate documents (doc-generate)

> Generate an MRD for this vault.

> Generate the MRD as a docx.

> Generate the MRD as HTML.

> Generate the MRD and write it to `~/board-docs/2026-Q2-MRD.md`.

> Generate the one-pager.

> Generate the one-pager as HTML for the sales team.

> Regenerate every doc-generate output.

```bash
cb render mrd                                       # → <vault>/exports/MRD.md
cb render mrd --format html                         # → <vault>/exports/MRD.html
cb render mrd --format docx                         # → <vault>/exports/MRD.docx
cb render mrd --out ~/board-docs/2026-Q2-MRD.md
cb render one-pager                                 # → <vault>/exports/one-pager.md
cb render one-pager --format html
cb render mrd --date 2026-05-24                     # pin date (idempotency tests)
```

The MRD is profile-aware: a medical-device vault gets §3 Indications-for-use and §7 Regulatory landscape; a default-profile vault doesn't, and the section numbers shift to fill the gap. The controlled-document footer is appended only under the medical-device profile.

### Inspection and schema

> What node types exist in the medical-device profile?

> Describe the `regulatory-clearance` node type.

> Show me the active profile of this vault.

```bash
cb describe-profile --name medical-device           # describe by name
cb describe-profile --path .                        # describe the active profile
cb describe-node regulatory-clearance               # node-type spec
cb describe-node regulatory-clearance --path .      # warn if not active in this vault
```

### Branding the output

Drop files under `<vault>/_branding/`:

- `colors.yaml` — overrides primary, secondary, accent, text, background, muted, font_family_headings, font_family_body. CSS variables in the generated HTML pick them up.
- `logo.png` / `logo.jpg` / `logo.svg` — picked up if present (full embed in HTML/docx lands in a later milestone).
- `templates/mrd.md.j2` — override the bundled MRD template entirely.
- `templates/one-pager.md.j2` — override the bundled one-pager template entirely.
- `templates/html-wrapper.html.j2` — override the bundled HTML page chrome.

No flags needed — the render commands automatically pick up overrides when they exist.

## Example vault

`examples/meddev-fictional/` is a hand-built medical-device vault (fictional Vitalisens pulmonary patch + replaceable Pad) that exercises every active node type, every source kind, the IFU-history chain, the 510(k) predicate chain, the controlled-document boundary, and the non-goal-pillar pattern. Generated MRD / one-pager / HTML / docx live under `examples/meddev-fictional/exports/` as reference output.

```bash
cb validate          --path examples/meddev-fictional
cb render mrd        --path examples/meddev-fictional
cb render one-pager  --path examples/meddev-fictional
```

## Idempotency

`cb render` produces byte-identical output for the same vault + pinned `--date`. The generation date lives only in the footer line. This makes git diffs on `<vault>/exports/` meaningful — you can read the diff to see what *content* changed, not just "the docs got regenerated."

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the full milestone list.

- **v0.1.0** ✅ schema definitions, `vault-architect`, hand-built medical-device example vault, `cb validate`.
- **v0.2.0** ✅ `intake` (vision + product + competitor sub-modes), `atomize` (markdown / Word / PDF / transcripts / image screenshots).
- **v0.3.0** ✅ `query` + MRD (profile-aware, evidence-vs-vision split, IFU comparison, anti-decisions) + one-pager + markdown / html / docx output.
- **v0.4.0** — `visualize` + `maintain` + scaffold generators for PID, business plan, competitive brief, risk brainstorm (19 doc types).
- **v0.5.0** — second example vault (SaaS) + onboarding docs + CHANGELOG.
- **v1.0.0** — public release tag and announcement.

## License

MIT. See [LICENSE](LICENSE).

## Inspiration

- The Infinite Brain pattern (atomic typed nodes + typed edges + frontmatter summaries + agent-readable system index).
- [graphify](https://github.com/safishamsi/graphify) — Python CLI shape, D3.js viewer, "god nodes" analytics. (graphify analyzes source code; company-brain analyzes company knowledge.)
- [obsidian-infinite-brain](https://github.com/JotaSXBR/obsidian-infinite-brain) — five-skill decomposition.
