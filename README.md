# company-brain

> ⚠️ **Pre-1.0, under active development.** APIs, schema, and skill interfaces will change without notice. Watch [ROADMAP.md](ROADMAP.md) for milestones.

**You're the person who knows everything about how your company works because you built it. Or you were hired into one, and you're trying to figure all of that out from the people who built it.** Either way, someone is the human cache keeping the sales deck, the investor update, the website, and the founder's head in sync with each other. `company-brain` is where those answers live so the founder stops being the lookup table — and the new hires stop interrupting them to do the job.

It's an open-source typed knowledge graph for early-stage companies. Capture your company's vision, products, customers, competitors, decisions, and the things you've explicitly ruled out as typed markdown nodes in your own git repository. Generate the 21 planning documents your company needs — MRD, PRD, business plan, sales battle card, competitive brief, investor update, decision log, onboarding doc, and more — directly from that single source of truth. Update one node, and every document that references it regenerates with a meaningful git diff.

## Why this exists

There is a phase in every early-stage company when the pitch deck quietly becomes the de facto source of truth for everything. The competitive landscape, the product roadmap, the pricing rationale, the team narrative — all of it lives in the deck because the deck is what gets updated for every investor meeting and partner pitch.

This works until it doesn't. The sales deck says one thing. The board deck says another. The investor update from last month says a third. The website says a fourth, written six months ago by someone who has since left the company. Five sources, five subtly different stories, and someone has to be the human cache reconciling them every Sunday afternoon.

`company-brain` exists for the moment when that reconciliation tax starts to be measurable in your week. It treats the company's knowledge as the source of truth and the documents as outputs, generated from typed nodes you own as markdown files in your own git repo. Capture the knowledge once. Use it everywhere.

## Who this is for

Three role-based personas span every industry the product supports:

- **The Founder** at a 1–15-person early-stage company who is currently the source of ground truth for everything, and feeling the scalability cost of being the bottleneck.
- **The Lead Product Manager** at a 15–50-person company whose job is to maintain product context across engineering, sales, marketing, and customer success, and who currently lacks a substrate shaped for synthesis.
- **The Lead Marketing Manager** at a 15–50-person company who produces MRDs, sales battle cards, and competitive briefs by hand, and watches them drift from product reality within weeks.

Industry doesn't change the personas. A founder is a founder whether the company is building a wearable medical device, a SaaS analytics platform, a hardware product, or a services firm. **Industry specialization is layered on through opt-in profiles.** The most fully developed profile today is medical device — ISO 14971 risk vocabulary, indications-for-use history chains, 510(k) predicate-device modeling, with the explicit discipline of sitting *above* design controls and producing no controlled documents. Reserved profile slots for SaaS, hardware, and services are open to community contribution.

Two earlier-stage variants the same machinery serves:

- **The pre-founder solopreneur** with the idea in hand, the company still mostly in your head, and a real possibility — Y Combinator pending, customer LOI in, day job notice ready to give — that "now I have five employees" becomes a problem next quarter. company-brain captures what's already in your head so the first hire walks into a real wiki, not a Notion graveyard.
- **The serial entrepreneur** running two or three project folders in parallel. Each company's vault is fully isolated in its own directory and git repo. No bleed between them; no shared "settings" to keep straight. `cb scaffold` and you're running.

Both also benefit from generated docs as **professional-credibility leverage** when working with outsourced contract manufacturers, fractional marketers, or 510(k) consultants — handing a partner an MRD up front compresses weeks of back-and-forth into a single review pass.

## What you get

- **Typed knowledge graph in plain markdown.** Products, personas, customers, competitors, decisions, pillars, requirements, features, metrics — each a first-class node type with structured frontmatter and typed edges. Agent-readable. Human-readable. Version-controlled like code, because it is.
- **21 planning-document generators.** From the same graph: MRD, PRD, PID, business plan, sales battle card, competitive brief, investor update, decision log, status report, SRD / SRS / HRS, press release, onboarding doc, IFU comparison (medical-device), risk register (medical-device), and others. Idempotent: same vault, same byte-identical output.
- **Anti-decisions and non-goal pillars as first-class concepts.** What the company has explicitly ruled out is captured, retrievable, and surfaced in generated documents.
- **Vision-vs-evidence provenance.** Every load-bearing claim cites a typed source node. Generated documents distinguish founder vision from market evidence, customer interviews, FDA filings, and other source kinds.
- **Vault is a git repository.** Multi-user collaboration via standard PR / merge workflow. No proprietary sync layer, no per-seat pricing, no vendor lock.

## What this isn't

The discipline of saying no is what creates room for the things `company-brain` does well.

- **Not a project management tool.** No sprints, no Gantt charts, no OKR tracking. We feed Jira, Linear, and Asana. We don't try to be them. Test: if a proposed feature would generate more than ~5 vault changes per user per week, it's the wrong shape for markdown-in-git.
- **Not an eQMS.** For medical-device users, we sit *above* design controls and produce no controlled documents. We feed Greenlight Guru, MasterControl, Innolitics RDM, and similar systems.
- **Not a SaaS.** The vault lives on your machine, in your own git repo. No multi-tenant database, no proprietary sync.
- **Not for non-technical buyers.** The markdown / git / CLI workflow is a deliberate filter. Notion and Confluence serve WYSIWYG audiences better.

Built as a set of Claude Code skills plus a Python CLI (`cb`). MIT-licensed.

## Status

Current milestone: **v0.7.0 — Document-driven intake.** ✅ shipped. The intake-render loop now works the other way around: start from a target doc's section structure and let it drive what gets captured. Two read-only CLI helpers (`cb describe-doc-questions`, `cb gaps-for-doc`), one shipped manifest (MRD), and a new `intake for-doc` sub-mode that walks a doc's sections in order — skipping the complete ones, confirming the partial ones, asking about the empty ones — and silently files stray facts (caught from voice-dictated rambles) into other sections of the same doc. Two example vaults still exercise both shipped profiles end-to-end. See the [CHANGELOG](CHANGELOG.md) for the full delta. Next milestone is **v1.0.0** — the release tag and public announcement.

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
| [`intake`](skills/intake/SKILL.md) | Conversational capture into typed nodes. Sub-modes: vision (dictation-friendly six-phase flow), **for-doc** (document-driven interview that walks a target doc's sections), product, persona, competitor, competitor-ifu, competitor-clearance, competitor-snapshot, metric, meeting-notes, risk, clearance. |
| [`atomize`](skills/atomize/SKILL.md) | Ingest existing docs (markdown, Word, PDF, transcripts, image screenshots) into typed nodes with provenance. |
| [`query`](skills/query/SKILL.md) | Answer questions against the graph. Auto-injects pillars, walks typed edges, cites node ids, flags vision-vs-evidence and staleness. |
| [`doc-generate`](skills/doc-generate/SKILL.md) | Render planning documents from the graph. **21 generators**: full MRD (md / html / docx), full one-pager (md / html), plus 19 scaffolds (PID, project charter, stakeholder register, risk register, status report, meeting minutes, lessons learned, business plan, sales battle card, competitive brief, IFU comparison, decision log, press release, investor update, onboarding doc, SRD, SRS, HRS, risk brainstorm). |
| [`maintain`](skills/maintain/SKILL.md) | Audit and repair the vault. `cb maintain repair` (auto-fix filename-id, missing inverse edges, controlled_document flag; regen INDEX.md). `cb maintain decay` (half-life confidence decay on fact snapshots). `cb maintain audit` (read-only health summary). `cb validate --fix` wires the same repair pass. |
| [`visualize`](skills/visualize/SKILL.md) | D3 interactive HTML viewer. Single self-contained file. View modes: `graph` (force-directed, color by type), `ifu-chain` (medical-device), `predicate-tree` (medical-device). |

## The CLI

```
cb --help                                    # list subcommands
cb --version
cb scaffold        --profile <name>          # create a vault
cb validate        [--fix]                   # check the vault; --fix runs maintain repair first
cb describe-profile                          # JSON description of the active profile
cb describe-node   <type>                    # JSON description of one node type
cb extract         <file.docx|file.pdf>      # text extraction for atomize
cb list-nodes      [filters]                 # JSON summary of nodes (for query)
cb get-node        <id>                      # JSON node + inbound/outbound edges
cb render          <doc>  [--format ...]     # 21 doc types — MRD, one-pager, 19 scaffolds
cb describe-doc-questions <doc> [--path ...] # JSON question manifest for the for-doc interview
cb gaps-for-doc    <doc>  --path <vault>     # per-section gap report (complete/partial/empty)
cb maintain        <subcommand>              # repair | decay | audit | rebuild-index
cb viewer          [--mode ...]              # D3 HTML graph viewer
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

#### Document-driven intake (`for-doc`)

When you have a specific doc in mind — an MRD for the board, a PID to kick off a project — and you'd rather have the doc's section structure guide what gets captured than figure out which intake sub-mode covers each piece, run the `for-doc` interview.

> Let's do an intake for the MRD. I'll dictate.

> Walk me through what's missing from the MRD section by section.

> Document-driven intake of the MRD — go.

The interview reads the doc's question manifest, computes per-section gaps against your vault, and announces what it'll cover up front: "I have everything I need for the executive summary, market personas, and competitive landscape. Vision and positioning is partial — you have 2 pillars but the section wants 3+. The remaining 4 sections are empty. We'll walk those 5 sections. Ready?"

Then it walks the sections in order, posing questions written for voice dictation ("In one or two sentences, what does this company build, and who is it for?"). After each rambling answer, it extracts the on-topic content into the right node type and silently files stray facts that match another section's needs — so when you accidentally mention a competitor while answering a vision question, that competitor lands in §6 without breaking your flow. At the end it prints a captured-summary, runs `cb validate`, and offers to render the doc.

```bash
cb describe-doc-questions mrd --path .        # JSON: manifest, profile-filtered for this vault
cb gaps-for-doc mrd --path .                  # JSON: per-section status (complete/partial/empty)
```

v0.7.0 ships the MRD manifest. More doc types add manifests as adopters surface the need — each new manifest is a YAML file, not new code.

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

#### v0.4.0 scaffolds — 19 more doc types

> Generate a PID for this project.

> Render a stakeholder register.

> Build a sales battle card against CardioTrace.

> Generate the SRD, SRS, and HRS.

> Render the decision log so I can see every choice and its rules-out.

> Generate the onboarding doc for a new hire.

> Build a risk brainstorm doc — we have a hazards review coming up.

```bash
# Project management
cb render pid
cb render project-charter
cb render stakeholder-register
cb render risk-register                             # medical-device only
cb render status-report
cb render meeting-minutes
cb render lessons-learned

# Engineering requirements
cb render srd                                       # system-class requirements
cb render srs                                       # software-class requirements
cb render hrs                                       # hardware-class requirements

# Strategy / sales / external
cb render business-plan
cb render sales-battle-card                         # picks first competitor by id
cb render sales-battle-card --competitor competitor-pulseguard-medical
cb render competitive-brief
cb render ifu-comparison                            # medical-device only
cb render decision-log
cb render press-release
cb render investor-update
cb render onboarding-doc

# Risk planning (medical-device only)
cb render risk-brainstorm
```

Each scaffold is a runnable Jinja2 template that queries the right typed nodes, fills in what it can, and flags the output as a scaffold in the footer for adopters to complete. Sections with no inputs degrade gracefully to bracketed placeholders that name the right `intake` sub-mode. Markdown and HTML are both supported; docx / xlsx ship per-doc with the v1.x full implementations.

### Visualize the graph

> Generate a D3 HTML viewer for this vault.

> Show me an IFU-chain view of the medical-device vault.

> Show me the 510(k) predicate tree.

```bash
cb viewer                                           # → <vault>/vault-graph.html
cb viewer --mode ifu-chain                          # medical-device only
cb viewer --mode predicate-tree                     # medical-device only
cb viewer --out exports/landscape-2026-q2.html      # snapshot for committing/sharing
```

Single self-contained HTML file. D3 v7 from CDN; the vault data is embedded as a JSON island. Hover for tooltip, click a node to highlight its neighbors and see frontmatter detail in the side panel, drag to reposition, scroll to zoom.

### Maintain the vault

> Audit this vault — what needs fixing?

> Repair the vault (add missing inverse edges, fix filename-id mismatches, regenerate INDEX.md).

> Decay the confidence on volatile fact snapshots.

> Validate the vault and auto-fix what you can.

```bash
cb maintain audit                                   # read-only health summary
cb maintain repair                                  # auto-fix + INDEX.md regen
cb maintain repair --dry-run                        # preview without writing
cb maintain decay                                   # half-life decay on fact snapshots
cb maintain decay --today 2027-01-01                # pin reference date
cb maintain rebuild-index                           # regenerate _system/INDEX.md only
cb validate --fix                                   # validate after auto-repair
```

Confidence decay is per-metric: facts tied to a `low`-volatility metric have a 24-month half-life, `medium` is 6 months, `high` is 1 month. The original confidence is preserved as `confidence_original` so re-running is idempotent.

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
- `templates/<doc-name>.md.j2` — override the bundled template for any of the 21 doc types (e.g. `mrd.md.j2`, `business-plan.md.j2`, `sales-battle-card.md.j2`).
- `templates/html-wrapper.html.j2` — override the bundled HTML page chrome.

No flags needed — the render commands automatically pick up overrides when they exist.

## Example vaults

Two fully-built example vaults exercise both shipped profiles:

- **`examples/meddev-fictional/`** — `medical-device` profile. Fictional Vitalisens ambulatory cardiac monitor + replaceable Pad. Exercises every active node type including the IFU history chain, the 510(k) predicate chain, the controlled-document boundary, and the non-goal-pillar pattern.
- **`examples/saas-fictional/`** — `default` profile. Fictional Loftwing engineering analytics for VPs of Engineering. Exercises every universal node type without any medical-device-specific machinery. Distinct branding palette so the rendered HTML is visibly different.

Both vaults ship pre-generated outputs under `exports/` — MRD (markdown/html/docx), one-pager, all applicable scaffolds, sales battle cards.

```bash
cb validate          --path examples/meddev-fictional
cb render mrd        --path examples/meddev-fictional
cb render one-pager  --path examples/saas-fictional
cb viewer            --path examples/saas-fictional --out /tmp/saas.html
```

See [docs/adoption-guide.md](docs/adoption-guide.md) for an end-to-end walkthrough and [docs/profiles.md](docs/profiles.md) for the profile mechanism in detail.

## Idempotency

`cb render` produces byte-identical output for the same vault + pinned `--date`. The generation date lives only in the footer line. This makes git diffs on `<vault>/exports/` meaningful — you can read the diff to see what *content* changed, not just "the docs got regenerated."

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the full milestone list.

- **v0.1.0** ✅ schema definitions, `vault-architect`, hand-built medical-device example vault, `cb validate`.
- **v0.2.0** ✅ `intake` (vision + product + competitor sub-modes), `atomize` (markdown / Word / PDF / transcripts / image screenshots).
- **v0.3.0** ✅ `query` + MRD (profile-aware, evidence-vs-vision split, IFU comparison, anti-decisions) + one-pager + markdown / html / docx output.
- **v0.4.0** ✅ `maintain` + 19 doc scaffolds + `visualize` (D3 HTML viewer with IFU-chain and predicate-tree modes).
- **v0.5.0** ✅ saas-fictional example vault + adoption guide + profiles doc + competitive-archive doc + CHANGELOG.
- **v0.6.0** ✅ field-report polish: non-destructive `cb scaffold --force` (marker-aware README + `.gitignore` splice; branding skip-if-exists), DOCX byte-deterministic, exports-table filter, `cb maintain init-readme-markers` / `init-gitignore-markers`.
- **v1.0.0** — public release tag and announcement.

## License

MIT. See [LICENSE](LICENSE).

## Inspiration

- The Infinite Brain pattern (atomic typed nodes + typed edges + frontmatter summaries + agent-readable system index).
- [graphify](https://github.com/safishamsi/graphify) — Python CLI shape, D3.js viewer, "god nodes" analytics. (graphify analyzes source code; company-brain analyzes company knowledge.)
- [obsidian-infinite-brain](https://github.com/JotaSXBR/obsidian-infinite-brain) — five-skill decomposition.
