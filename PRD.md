---
title: "company-brain — Product Requirements Document"
status: draft
version: 0.3.0
date: 2026-05-21
controlled_document: false
---

# company-brain — Product Requirements Document

> This document is itself a planning artifact. It is not a controlled document and is not part of any design history file, risk management file, or traceability matrix.

## 1. Vision

`company-brain` is a public, open-source set of Claude Code skills plus a Python CLI that lets a company build an AI-native knowledge graph of itself — products, people, decisions, vision, evidence, competitive landscape — and generate planning documents (starting with a Marketing Requirements Document) from that graph. The graph lives in Obsidian-compatible markdown so humans can browse it; the typed schema makes it cheap for agents to retrieve from.

**A company's vault is itself a git repository.** It can stay local, or be pushed to GitHub, GitLab, Bitbucket, or an on-prem git host. Team members clone the repo to their own machines, navigate the knowledge graph in Obsidian or any markdown viewer, regenerate documents, and push changes back. Multi-user collaboration uses the same merge / PR / pull-request tools teams already use for source code — company-brain stays out of git's way rather than building a separate coordination layer.

It is the layer **above** any controlled product-development records. For medical-device companies in particular, it is the place to think out loud about hazards, indications for use, requirements, competitors, and strategy without polluting design history, traceability, or risk management files.

## 2. Problem

The "second brain for me" pattern doesn't scale to "knowledge for a company." Existing patterns either:

- Optimize for one human browsing folders (PARA, Zettelkasten) — agents can't retrieve from them cheaply.
- Optimize for one agent reasoning about one person's life (the Infinite Brain pattern) — they don't model products, personas, competitors, indications for use, or regulatory clearances as first-class entities.
- Live inside heavyweight enterprise systems (Confluence, SharePoint) — they're closed, expensive, and not LLM-friendly.

Med-device companies have a sharper version of the problem: they need a place to think about hazards, requirements, and competitive predicates *before* anything is committed to a controlled document, without that thinking accidentally becoming a controlled record.

## 3. Target users

- Solo founders and small teams building software, hardware, or hybrid products.
- **Distributed teams** that want their planning knowledge to live alongside their code — same git host, same review tools, same access controls. Cloning the company vault should feel like cloning any other repo.
- Medical-device teams who want a planning layer above their design controls.
- Anyone already using the Infinite Brain or Second Brain patterns who needs to graduate to multi-product, multi-stakeholder, multi-contributor knowledge with competitive intelligence built in.

Public GitHub under github.com/nemock for the skills + CLI + examples. MIT-licensed. Friendly to fork, vendor, and extend. **Company vaults are separate, user-owned repositories** — typically private, hosted wherever the company hosts its other code.

## 4. v1 scope

A full pipeline:

- Seven Claude Code skills: `vault-architect`, `intake`, `atomize`, `query`, `doc-generate`, `maintain`, `visualize`.
- One finished document generator: **MRD**.
- Scaffolded (stubbed-but-runnable) generators for project initiation, business plan, competitive brief, risk brainstorm.
- Python CLI (`cb`) shipped via `uv tool install` / `uvx`.
- Schema with epistemic nodes + company entity nodes + opt-in medical-device profile (indications for use, regulatory clearances, hazards, etc.).
- **Vault as git repository.** `cb scaffold` runs `git init` by default, writes a vault-level `.gitignore`, and makes an initial commit. Multi-user collaboration via standard git workflows.
- **Branding folder** (`_branding/`) for logos, brand colors, fonts, and per-document templates that doc-generate consumes.
- Vision intake — a dictation-friendly conversational sub-mode that turns rambling prose into typed nodes with full provenance.
- Anti-decisions and non-goals as first-class concepts (decision template, pillars-as-non-goals).
- Competitive archive — competitor entities with IFU history, regulatory clearances, predicate chains, and manual web-snapshot import.
- D3-based vault visualizer (inspired by graphify).
- Two fictional example vaults: medical-device (patient monitoring wearable + replaceable sensor pad) and SaaS.

## 5. Out of scope

### Deferred to v1.x
- Full PID, business plan, competitive brief, and risk-brainstorm generators (v1 ships scaffolds only).
- PowerPoint atomization (Word and PDF are v1).
- SaaS / hardware / services profile *content* (v1 reserves slots; profile mechanism is exercised by `medical-device`).
- chrome-devtools-mcp-assisted automated web-snapshot capture (manual screenshot import is v1).
- openFDA API integration for automated 510(k) ingestion (manual paste-and-atomize is v1).
- Multi-page crawl + change detection.
- A polite single-page HTTP fetcher (`cb fetch`) as a no-Chrome-MCP fallback.
- A wrapper around the existing `competitor-profiling` skill that writes directly into the vault.

### Deferred to v2
- BOM / component / kit / sub-component first-class modeling, with **quantity** as edge metadata on `part_of` edges. v1 treats `product` and `product-line` as first-class but opaque.
- Cross-kit overlap analytics ("which kits break if I change component X?").
- Component dependency reasoning.
- Recurring competitor monitoring jobs ("re-scan these 8 competitors monthly, alert me on IFU drift").
- Headless-browser fetcher for JS-heavy sites without chrome-devtools-mcp.
- Optional MCP server exposing the vault as a queryable resource for other agents.

### Probably not needed
- **Confluence / Notion / Obsidian Sync export adapters** — git push to the corporate git host (GitHub, GitLab, Bitbucket, on-prem) already solves the "publish into existing tooling" use case for most teams. Revisit only if a real adopter need emerges.

### Permanently out of scope
- Controlled-document generation. company-brain never produces a signed DHF, risk management file, traceability matrix, V&V protocol, or anything intended for regulatory submission.
- Multi-tenant single-vault. One vault is one company.
- Real-time multi-user editing. Collaboration is via git, not a separate sync layer.
- Closed-source or cloud-hosted variants.

## 6. Architecture

### Repo layout (the company-brain skills + CLI)

```
company-brain/
├── README.md
├── LICENSE                     # MIT
├── pyproject.toml              # uv-installable
├── skills/
│   ├── vault-architect/SKILL.md
│   ├── intake/SKILL.md
│   ├── atomize/SKILL.md
│   ├── query/SKILL.md
│   ├── doc-generate/SKILL.md
│   ├── maintain/SKILL.md
│   └── visualize/SKILL.md
├── src/company_brain/
│   ├── cli.py                  # exposes `cb`
│   ├── schema/                 # node/edge/profile definitions
│   ├── scaffold.py             # vault scaffolding incl. git init
│   ├── render/                 # docx, pptx, xlsx, md, html
│   ├── intake/                 # docx, pdf, transcript, image, markdown parsers
│   ├── viewer/                 # D3 HTML generator
│   └── templates/              # jinja2 MRD + scaffolds
├── examples/
│   ├── meddev-fictional/       # patient monitoring wearable + sensor pad
│   └── saas-fictional/
└── docs/
    ├── schema.md
    ├── profiles.md
    ├── controlled-document-boundary.md
    ├── vault-as-git-repository.md
    ├── competitive-archive.md
    └── adoption-guide.md
```

### Vault layout (what users have on disk per company)

A vault is a git repository. `cb scaffold` runs `git init` by default, writes a vault-level `.gitignore`, and makes an initial commit. Pass `--no-git` to opt out.

```
my-company-vault/                # the git repo root
├── .git/                        # initialized by `cb scaffold` (committed history)
├── .gitignore                   # vault-level — distinct from the company-brain repo's .gitignore
├── README.md                    # written by scaffold; identifies the vault
├── _system/
│   ├── PROFILE.md               # industry profile (e.g. medical-device)
│   ├── INDEX.md                 # GENERATED, GITIGNORED — rebuilt by `cb` on demand
│   ├── NODE-TYPES.md            # rendered from schema; committed
│   ├── EDGE-TYPES.md            # rendered from schema; committed
│   └── FRONTMATTER-SCHEMA.md    # rendered from schema; committed
├── _branding/                   # logos, brand colors, fonts, per-doc templates
│   ├── logo.png                 # consumed by doc-generate
│   ├── colors.yaml              # palette and typography choices
│   └── templates/               # optional jinja2 overrides for doc-generate
├── pillars/                     # IB epistemic node folders
├── decisions/
├── playbooks/
├── patterns/
├── hypotheses/
├── facts/
├── concepts/
├── sources/
├── questions/
├── notes/
├── entities/                    # company entity nodes (sub-folders below)
│   ├── products/
│   ├── product-lines/
│   ├── personas/
│   ├── customers/
│   ├── stakeholders/
│   ├── competitors/
│   ├── vendors/
│   ├── requirements/
│   ├── features/
│   ├── use-cases/
│   ├── metrics/
│   └── indications-for-use/     # profile-conditional (medical-device)
├── risk/                        # profile-conditional, medical-device only
│   ├── risk-insights/
│   ├── hazards/
│   ├── hazardous-situations/
│   ├── harms/
│   ├── risk-control-ideas/
│   ├── regulations/
│   ├── standards/
│   └── regulatory-clearances/
├── _attachments/                # binary captures: screenshots, PDFs, raw HTML — COMMITTED by default
└── exports/                     # generated documents (MRD, PID, etc.) — COMMITTED by default
```

**Default vault `.gitignore`:**

```gitignore
# Generated; rebuild with `cb` on demand
_system/INDEX.md

# Local-only editor state
.obsidian/workspace*.json

# OS / editor cruft
.DS_Store
*.swp
.vscode/
```

By default, `_attachments/` and `exports/` are **committed** so a team member who has cloned the repo but has not installed company-brain can still read the latest MRD or see the competitor screenshots referenced by source nodes. Users who don't want this can extend the vault `.gitignore` after scaffolding.

### Separation of concerns

- **Skills** own all node writing. LLM-driven; conversational; produce markdown.
- **CLI** owns rendering, validation, viewer generation, analytics, and git scaffolding. Deterministic; never writes node content.
- **Git** owns versioning, distribution, and conflict resolution. company-brain stays out of git's way — no custom locking, no proprietary sync, no daemon. Standard `git pull` / `git push` / PR review are the multi-user model.

This split mirrors graphify's pattern (deterministic tree-sitter parsing vs. LLM extraction for unstructured material) and keeps each layer testable independently.

## 7. Schema

### Inherited epistemic node types (from Infinite Brain)

`pillar`, `decision`, `playbook`, `pattern`, `hypothesis`, `fact`, `concept`, `source`, `question`, `note`.

Semantics, frontmatter, and edge rules follow the Infinite Brain conventions (typed edges, one-line summaries, confidence, verified_at, staleness_signal).

### New company entity node types

| Type | Folder | Purpose |
|---|---|---|
| `product` | `entities/products/` | A shipped or in-development product. Opaque in v1 (BOM in v2). |
| `product-line` | `entities/product-lines/` | A family of related products. |
| `persona` | `entities/personas/` | An archetypal user, distinct from a real customer. |
| `customer` | `entities/customers/` | A named real customer (anonymized as needed). |
| `stakeholder` | `entities/stakeholders/` | Internal or external party with influence. |
| `competitor` | `entities/competitors/` | A named competitor or alternative. Fields: `legal_name`, `canonical_url`. |
| `vendor` | `entities/vendors/` | A supplier, contractor, or service provider. |
| `requirement` | `entities/requirements/` | A market, user, or system requirement. `requirement_class` is mandatory; never claims to be a design input. |
| `feature` | `entities/features/` | A product capability. |
| `use-case` | `entities/use-cases/` | A scenario of use. |
| `metric` | `entities/metrics/` | The concept of a measurement. Time-series fact nodes link back. |

### Profile-conditional node types (medical-device)

| Type | Folder | Purpose |
|---|---|---|
| `indication-for-use` | `entities/indications-for-use/` | Population + condition + intervention + setting. Belongs to any product, ours **or competitor's**. Versioned via `preceded_by` / `followed_by` chain. |
| `regulatory-clearance` | `risk/regulatory-clearances/` | A specific clearance event (510(k), De Novo, PMA, breakthrough designation, letter-to-file). Carries clearance number, applicant, date, predicate clearances, product codes. |
| `risk-insight` | `risk/risk-insights/` | A planning-level observation about risk. Not a risk record. |
| `hazard` | `risk/hazards/` | A potential source of harm, in 14971 vocabulary, captured for thinking. |
| `hazardous-situation` | `risk/hazardous-situations/` | A circumstance where a hazard could lead to harm. |
| `harm` | `risk/harms/` | A potential physical injury, damage, or impact. |
| `risk-control-idea` | `risk/risk-control-ideas/` | A candidate mitigation under consideration. Not a chosen control. |
| `regulation` | `risk/regulations/` | A cited regulation (MDR, 21 CFR 820, etc.). |
| `standard` | `risk/standards/` | A cited standard (ISO 14971, IEC 62304, IEC 60601, etc.). |

Every node in the `risk/` tree and the `indications-for-use/` folder carries `controlled_document: false` in frontmatter. The `medical-device` profile inserts a footer disclaimer on every generated document.

### Edges

v1 inherits the IB edge set: `related_to`, `depends_on`, `derived_from`, `contradicts`, `supports`, `part_of`, `preceded_by`, `followed_by`, `authored_by`, `tagged_with`.

**Predicate relationships are first-class edges**, not just frontmatter lists. A `regulatory-clearance` node uses `preceded_by` to link to its declared predicate clearance(s).

**IFU history is an edge chain.** Each new IFU snapshot for a given product is a separate immutable node — `indication-for-use-acme-monitor-2024-q1`, `indication-for-use-acme-monitor-2026-q3` — linked via `preceded_by` / `followed_by`. "How did Acme's IFU evolve?" is a one-hop chain walk.

v2 will introduce **quantity-bearing edges** on `part_of` for BOM modeling.

### Frontmatter

Required fields per Infinite Brain schema: `id`, `title`, `type`, `namespace`, `summary`, `auto_inject`, `applicable_when`, `confidence`, `verified_at`, `verified_by`, `staleness_signal`, `tags`, `edges`, `related`, `source_url`.

**Additional company-brain fields:**

| Field | Applies to | Purpose |
|---|---|---|
| `controlled_document` | all nodes (default `false`) | Affirmative declaration that this is a planning artifact. |
| `profile` | `_system/PROFILE.md` only | Active industry profile. |
| `source_kind` | `source` nodes | Distinguishes origin (see §9). Drives MRD claim-flagging. |
| `producing_skill` | `source` nodes when `source_kind: skill-output` | Names the upstream skill. |
| `requirement_class` | `requirement` nodes | `market` \| `user` \| `system`. Required. |
| `metric_id` | time-series fact nodes | Foreign key into the `metric` node this snapshot belongs to. |
| `volatility_class` | `metric` nodes | `low` / `medium` / `high`. Drives confidence decay half-life. |
| `legal_name`, `canonical_url` | `competitor` nodes | Disambiguation. All subsequent fetches scope to `canonical_url`'s domain. |
| `population`, `condition`, `intervention`, `setting` | `indication-for-use` nodes | The structured IFU components. |
| `belongs_to_product` | `indication-for-use` nodes | Edge target: a `product` node (ours or a competitor's). |
| `clearance_number`, `clearance_type`, `clearance_date`, `applicant`, `device_name`, `product_codes`, `summary_url` | `regulatory-clearance` nodes | Structured clearance metadata. |
| `url`, `captured_at`, `captured_method`, `attachment` | `source` nodes with `source_kind: web-snapshot` | Web archive metadata. |

### Anti-decisions and non-goals

What a company is choosing **not** to do is as important as what it is choosing to do. Three patterns codify this:

1. **Decision template gets a `## What This Rules Out` section** alongside "Alternatives Considered." Many decisions have a negative frame that is more memorable than the positive one ("no physical documentation" is what people remember; "online-only documentation" is the technically correct framing). Both belong in the node.
2. **Pillars are the home for strategic non-goals.** A statement like "We will never enter the consumer market" is a durable principle that should govern future answers — that's a pillar with negative framing and an `applicable_when` like `"consumer market, B2C, retail channel, mass-market"`. If anyone later asks "should we explore consumer?", the pillar auto-injects and the agent answers correctly without re-litigating.
3. **The vision-intake nugget extractor has a non-goal classifier**, surfacing rejected directions as candidate decisions or non-goal pillars.

## 8. Profile mechanism

`_system/PROFILE.md` declares the active industry profile:

```yaml
---
profile: medical-device
profile_version: 1.0
---
```

The profile controls:

- Which entity / risk folders the architect creates.
- Which intake sub-modes the `intake` skill exposes.
- Which scaffolds the `doc-generate` skill makes available.
- **Which sections appear in generated documents.** Profile-conditional sections are omitted entirely when the active profile doesn't enable them — not rendered empty, not rendered with a placeholder. A SaaS profile MRD has no "Indications for use" section at all; a medical-device profile MRD has no section it doesn't earn.
- Whether the controlled-document footer is appended to generated documents.

v1 ships `medical-device`. Profile slots reserved (empty implementations): `saas`, `hardware`, `services`. A `default` industry-agnostic profile exists for users who want only the IB epistemic types plus the universal company entity types.

## 9. Provenance model

Every meaningful claim in a generated document must trace via `derived_from` to a `source` node. The source can be of any `source_kind`:

| `source_kind` | What it is | Example |
|---|---|---|
| `customer-interview` | A specific conversation with a real or prospective customer. | "Interview 2026-04-12 with neurosurgeon Dr. X" |
| `market-data` | Third-party market research, public stats. | "IMV Medical Information Division MRI report 2025" |
| `citation` | A book, paper, talk, article. | "Norman, *The Design of Everyday Things*" |
| `founder-vision` | A documented thesis from a company founder or principal. | "Founder vision 2026: workflow-time is the surgical bottleneck" |
| `domain-expertise` | Documented expertise of a named team member. | "20 years operating-room exposure, neurosurgical procedures, author: D. Saunders" |
| `strategic-thesis` | A bet about the market that the company is making. | "We believe surgeons adopt robotics if procedure time drops 30%" |
| `internal-data` | Internal telemetry, user data, observed product behavior. | "Q1 2026 user activity log, 14-day cohort" |
| `prior-internal-doc` | An existing internal document being ingested. | "Project Initiation Doc, drafted 2025-Q3" |
| `skill-output` | The output of another Claude Code skill, ingested via atomize. | competitor-profiling output for Competitor X |
| `press-release` | Date-stamped corporate announcement. | "Acme Medical press release 2026-02-14" |
| `web-snapshot` | Page captured at a moment (HTML, screenshot, or both). | "acme-medical.com/products/cardiac-monitor on 2026-05-20" |
| `web-snapshot-network` | List of network requests from a captured page. | Tech-stack intel: analytics, CMS, embedded services |
| `fda-510k-summary` | The public PDF for a clearance. | "K223456 summary PDF" |
| `regulatory-filing` | Broader bucket for non-510(k) docs. | "CE Technical File summary, MDR public report" |

**Vision is a first-class source.** The MRD generator labels every claim in its output by `source_kind`, so a reader can see at a glance which parts are vision-driven and which are evidence-driven. Both are legitimate; conflating them silently is the failure mode this prevents.

The generator does refuse to ship a claim with **no** traceable source at all. Vision counts; uncited prose does not.

## 10. Intake

### `intake` skill sub-modes (medical-device profile shown)

- `product` — capture a product, product line, or sub-component.
- `vision` — see "Vision sub-mode" below. Dictation-friendly conversational capture.
- `persona` — build a persona node from a conversation.
- `competitor` — capture a competitor entity (legal name, canonical URL, positioning).
- `competitor-ifu` — capture or update a competitor's indication for use (versioned via `preceded_by`).
- `competitor-clearance` — capture a `regulatory-clearance` for a competitor, including predicate chain.
- `competitor-snapshot` — capture a web-snapshot of a competitor page (manual screenshot import in v1; chrome-devtools-mcp-assisted in v1.x).
- `metric` — define a metric and seed initial fact snapshots.
- `meeting-notes` — process a freshly-finished meeting into atomic nodes.
- `risk` — walk through ISO 14971-vocabulary risk thinking with the controlled-document boundary reminder.
- `clearance` — capture our own regulatory clearance plans or status.

### Vision sub-mode (the six-phase flow)

Designed to absorb messy dictated or typed prose without imposing structure up front:

1. **Open capture.** Skill says "Talk freely. End with 'done' or 'process'." User dictates or types for as long as wanted, in any order. No structure imposed.
2. **Source node creation, immutable.** Skill writes one `source` node — `source-vision-session-2026-05-20`, `source_kind: founder-vision`, body = the complete raw transcript preserved verbatim. This is the audit trail. It never gets edited later.
3. **Nugget extraction.** Skill scans the transcript and proposes typed nodes: pillars, decisions (positive and anti-decision), hypotheses, requirements, risk-insights, indications-for-use, non-goal pillars. Output is a batched table with one row per proposal: excerpt, proposed type, proposed id, one-line rationale.
4. **Review loop.** User reviews the batched table and accepts / edits / rejects / splits / merges each row. (CLI flag `--interactive` switches to one-at-a-time prompts for users who prefer that.) Rejected rows get logged in the source node so reasoning is preserved.
5. **Write and link.** Accepted nodes get written with `derived_from` → the source node. INDEX.md updated.
6. **Anti-decision sweep.** Skill explicitly asks once more: "Were there any 'we are NOT doing X' statements I missed?" because dictation tends to bury non-goals inside positive prose.

Design principles:

- **Conservative extraction.** Not every sentence becomes a node. The bar: "would an agent retrieve this six months from now?" If no, it stays in the source body, not as its own node.
- **Multiple sessions are normal.** Each session is its own immutable `source-vision-session-<date>` node. The graph grows by accretion.
- **Dictation noise is fine.** The skill tolerates homonym errors and asks for clarification only on high-stakes items (specific product names, numbers, indications-for-use language).

### Competitor disambiguation

When the user invokes `competitor` intake, the skill prompts for both `legal_name` ("Acme Medical Inc") and `canonical_url`. All subsequent snapshot capture, web-fetch, and atomize operations scope to that canonical_url's domain to prevent accidentally archiving the wrong "Acme Medical."

### `atomize` skill (file ingestion)

v1 input formats:

- **Markdown / plain text** — always.
- **Word (`.docx`)** — promoted from v1.x to v1 because pilot users have existing project initiation documents to ingest. Uses `python-docx`.
- **PDF** — text + simple tables, via `pdfplumber` or `pypdf`. Recognizes pasted-in FDA 510(k) summary PDFs and extracts IFU, predicates, product codes automatically.
- **Interview transcripts** — txt with timestamps. Claim extraction, quote attribution, persona signal extraction.
- **Image screenshots** — PNG/JPG of web captures, etc. Uses Claude's built-in vision to extract visible text. Image stored in `_attachments/`; extracted text in the source-node body.

v1.x adds: PowerPoint (`python-pptx`).

### Ingest-from convention

When the user runs an existing Claude Code skill (`competitor-profiling`, `customer-research`, `product-marketing-context`, `write-spec`, `competitive-brief`) and saves its output to a known location, `atomize` recognizes the section structure and routes content to typed nodes. The original document lands as a `source` node with `source_kind: skill-output` and `producing_skill: <name>`. Unknown skill outputs fall back to generic atomization.

## 11. Document generation

### v1 finished: MRD

The MRD generator pulls from:

- `pillar` (positioning, principles) — frames the doc; includes non-goal pillars.
- `persona`, `customer`, `competitor` — audience and landscape.
- `indication-for-use` — when present, including a competitor IFU comparison table.
- `requirement` with `requirement_class: market` — the actual market requirements.
- `metric` and recent `fact` snapshots — traction or absence-of-traction.
- `source` (all kinds) — claim labeling.
- `_branding/` — logos, colors, optional template overrides.

Output structure (jinja2 template, profile-aware):

| # | Section | Profile |
|---|---|---|
| 1 | Executive summary | all |
| 2 | Vision and positioning (cites pillars and founder-vision sources) | all |
| 3 | **Indications for use** (our IFU plus competitor IFU comparison table when present) | **medical-device only** |
| 4 | Market and personas (cites persona, customer, competitor nodes) | all |
| 5 | Market requirements (cites requirement nodes with class=market) | all |
| 6 | Competitive landscape (cites competitor nodes; medical-device profile adds regulatory clearances and IFU history) | all (medical-device extends) |
| 7 | **Regulatory landscape** (cites regulation, standard, regulatory-clearance nodes) | **medical-device only** |
| 8 | Evidence vs. vision split (auto-generated breakdown of which claims are vision-driven and which are evidence-driven) | all |
| 9 | Open questions (cites question nodes) | all |
| 10 | What we are explicitly not doing (cites anti-decisions and non-goal pillars) | all |
| 11 | Sources (full source-node bibliography with `source_kind` labels) | all |

Profile-conditional sections are omitted entirely when the active profile doesn't enable them. A `default` or `saas` profile MRD has no Indications for Use or Regulatory Landscape sections at all, and its Competitive Landscape section excludes the clearance/IFU sub-paragraphs.

Output formats: markdown (primary), docx, html. Outputs land in `exports/`, which is committed by default so team members without skills can still read them.

### v1 scaffolded (stubs that run but produce skeleton output)

- Project initiation document
- Business plan
- Competitive brief
- Risk brainstorm (medical-device profile only)

These ship as runnable Jinja2 templates that consume typed-node queries but produce intentionally incomplete output flagged as scaffold. They exist so adopters can fill them in, and so the v1 contract for "doc-generate produces something for each" holds.

### Idempotence

Re-running a generator on an unchanged vault produces byte-identical output modulo timestamps. This makes git diffs on `exports/` meaningful and prevents the "every regen looks different" anti-pattern.

### Controlled-document footer

When `profile: medical-device`, every generated document gets:

> This is a planning artifact. It is not a controlled document and is not part of any design history file, risk management file, or traceability matrix per ISO 14971, IEC 62304, or 21 CFR 820.

## 12. Vault as a git repository

A first-class feature of the v1 delivery model.

### Why it matters

A company's planning knowledge is more valuable when it can be shared, reviewed, and contributed to by multiple people on the team — without building a real-time collaboration layer. Git already solves this for source code. company-brain treats a vault as exactly the same kind of artifact.

### What this means in practice

- `cb scaffold` runs `git init` by default, writes a vault-level `.gitignore` matched to the company-brain schema, and creates an initial commit containing the scaffolded skeleton.
- The vault repo can stay local indefinitely, or be pushed to any git host (GitHub, GitLab, Bitbucket, on-prem Gitea, etc.). company-brain does not care which.
- Team members clone the vault repo to their own machines. With **just git + a markdown viewer**, they can read all node content, browse with Obsidian, and see the latest generated `exports/`. With the company-brain skills installed, they can also contribute — `intake`, `atomize`, `doc-generate`, etc.
- Skills emit structured commit messages so the git history doubles as a knowledge-graph audit trail ("added founder-vision source `source-vision-saunders-2026`", "regenerated MRD", "updated competitor `competitor-cardiotrace-inc` IFU history").
- Multi-user editing is via standard PR / merge-request workflows on the chosen host. Two people editing the same pillar produces a merge conflict; resolution is the same as for any other markdown conflict.

### What we deliberately do not build

- No real-time multi-user editing.
- No proprietary sync daemon or special service.
- No build-time database. The vault on disk is always the source of truth.
- No fancy locking on top of git. If two people edit the same node, git's normal conflict-resolution applies.

### Skills-aware vs. skills-unaware team members

- **Skills installed**: can intake, atomize, regenerate documents, run `cb validate`, push their own changes.
- **No skills installed**: can clone, read every markdown file, view exports (since exports are committed), view attachments, browse with Obsidian. Cannot contribute new nodes via the skills, but they can still hand-edit a markdown file if they understand the schema.

This asymmetry is intentional. The skills are the productivity layer; the markdown vault is the open data layer.

### Generated-file policy

To keep merges clean, files that change on every contribution are gitignored at the vault level. The `cb` CLI rebuilds them on demand.

| File | Policy | Why |
|---|---|---|
| `_system/INDEX.md` | Generated, gitignored | Touched by every intake/atomize; merge-conflict hotspot. |
| `_system/NODE-TYPES.md`, `EDGE-TYPES.md`, `FRONTMATTER-SCHEMA.md` | Rendered from schema, committed | Stable across normal use; regenerated by `cb scaffold --force` on company-brain upgrades. |
| `exports/*.md`, `exports/*.docx`, `exports/*.html` | Committed | Team members without skills still need to read them. Idempotent regeneration keeps diffs meaningful. |
| `_attachments/**` | Committed | Part of the knowledge graph. Heavy on size but essential. Users who want lighter repos override in `.gitignore`. |
| `_branding/**` | Committed | Brand assets are shared across the team. |

### Recommended workflow for collaborative vaults

1. One person scaffolds the vault and creates a remote (GitHub / Bitbucket / on-prem git).
2. Team members clone.
3. Routine intake / atomize work happens on `main` for small teams, on branches + PRs for larger teams that want review.
4. Doc regeneration (`cb render-mrd` etc.) is typically run by whoever is publishing the document; the regenerated `exports/` are committed in the same PR.
5. Heavyweight changes (new pillars, IFU updates) flow through PR review.

### Hosting considerations

| Host | Notes |
|---|---|
| GitHub (public or private) | Standard. Works out of the box. |
| GitLab | Standard. Works out of the box. |
| Bitbucket | Standard. Common in regulated industries already on Atlassian. Works out of the box. |
| On-prem (Gitea, Forgejo, etc.) | Standard. Works out of the box. |
| Local-only (no remote) | Fully supported. Single-user vaults can live indefinitely without a remote. |

## 13. Competitive archive

A first-class feature, not a side-channel. Justifies the schema additions in §7 and the intake sub-modes in §10.

### Why this matters
For medical-device companies pursuing a 510(k), the **predicate device's indications for use are a controlling input** to clearance success. Having a typed, queryable library of competitor IFUs, their historical versions, their clearance chains, and the public artifacts that surround them turns a one-week analysis into a one-day analysis. The same library generalizes outside med-device to any market where competitor positioning, regulatory posture, or feature claims matter.

### What gets archived
- **Competitor entities**, disambiguated by `legal_name` + `canonical_url`.
- **Indications for use** — current and historical, chained via `preceded_by`.
- **Regulatory clearances** — one node per clearance event, with predicate edges to other clearances (ours or theirs).
- **Web snapshots** — page captures at a moment in time, stored as `source` nodes with the image/HTML in `_attachments/` and extracted text in the body. Committed alongside everything else.
- **Press releases** — date-stamped, as `source` nodes with `source_kind: press-release`.
- **FDA 510(k) summary PDFs** — paste-and-atomize in v1; openFDA API in v1.x.
- **Network-request manifests** — optional companion source nodes capturing the API endpoints and embedded services a competitor's page calls (`source_kind: web-snapshot-network`). Useful tech-stack intel.

### Capture progression

**v1 (manual + deterministic):**
- All schema additions above. Hand-entry works.
- `competitor`, `competitor-ifu`, `competitor-clearance`, `competitor-snapshot` intake sub-modes.
- Image-screenshot import via `atomize`: user supplies path, image lands in `_attachments/`, Claude vision extracts visible text, source node created.
- Paste-FDA-510k-summary atomization: user drops the PDF, skill extracts IFU + predicates + product codes automatically.

**v1.x (chrome-devtools-mcp assisted):**
- The skill detects whether **chrome-devtools-mcp** tools are loaded (the user installs it themselves: `npx chrome-devtools-mcp@latest`).
- When available, `competitor-snapshot` automates capture:
  1. `navigate` loads the URL into the user's live Chrome.
  2. `take_screenshot` (full-page via CDP's `captureBeyondViewport`) captures the visual.
  3. `evaluate_script` or `take_snapshot` captures DOM-rendered text — no OCR needed.
  4. Optionally `list_network_requests` captures the network manifest into a sibling source node.
- robots.txt is irrelevant because this is the user's own browser session.
- openFDA API integration: `cb intake-510k <K-number>` calls openFDA, pulls structured fields, optionally downloads the summary PDF. Creates `regulatory-clearance` + `indication-for-use` + predicate edges without manual entry.

**v2 (recurring monitoring):**
- Scheduled re-capture jobs.
- Snapshot diffing across captures: only new content creates new source nodes; IFU drift triggers alerts.
- Headless-browser fetcher for users without chrome-devtools-mcp.

### Practical considerations
- **Storage growth.** Even text-stripped, 200 snapshots across 8 competitors over a year is a few hundred MB. The README documents this; users can override the default-committed `_attachments/` policy if they want lighter clones. CLI provides `cb prune-snapshots --older-than 18mo --keep-changes` for housekeeping.
- **JS-heavy sites.** v1's manual import bypasses this entirely. v1.x's chrome-devtools-mcp path bypasses it because Chrome renders the page.
- **JS-heavy sites without chrome-devtools-mcp.** v1.x has no good story for these except manual import. v2 adds a headless-browser fetcher.
- **Disambiguation.** All competitor fetches scope to the competitor's `canonical_url` domain to prevent name collisions.
- **Legal posture.** Captures are of publicly accessible content for personal/internal analysis, stored locally, not redistributed beyond the team that has access to the vault repo. The README is explicit about this.

### The queries this unlocks

- "How has Acme's IFU evolved across their last three 510(k)s?"
- "Which competitors share a predicate device with our planned filing?"
- "Show me competitor press releases from the last 18 months that mention pediatric use, indexed by competitor."
- "Which competitor product codes overlap with ours, and how do their cleared IFUs differ on patient population?"
- "Of the 12 competitors I track, who has expanded their IFU in the past 24 months, and what got added?"

All of these reduce to typed-edge traversals against the schema. No special-case code; the same `query` skill handles them.

## 14. Validation and maintenance

### `cb validate`

CLI command that exits non-zero on:

- Broken edges (target id does not resolve).
- Missing required frontmatter fields.
- Duplicate ids.
- Schema drift (unknown node type for active profile).
- Time-series facts with no `metric_id`.
- Sources without `source_kind`.
- Nodes in `risk/` or `indications-for-use/` without `controlled_document: false`.
- `regulatory-clearance` nodes whose declared predicates do not resolve to existing clearance nodes (warning, not error — the predicate may not have been ingested yet).

`cb validate --fix` auto-repairs:

- Missing inverse edges (the most common manual burden in IB-style vaults).
- `_system/INDEX.md` rebuild (regenerated from the live node set; INDEX.md is gitignored, so the rebuild stays local).

### Confidence decay

Applies **only** to `fact` nodes that link to a `metric` of `volatility_class: medium` or `high`.

Decay half-lives (defaults):
- `high` volatility: 30 days.
- `medium` volatility: 180 days.
- `low` volatility (and all non-metric facts): no decay.

`maintain` skill surfaces facts whose effective confidence has dropped below a configurable threshold and asks the user to re-verify, supersede, or accept.

Pillars, decisions, concepts, playbooks, patterns, hypotheses do **not** decay automatically.

## 15. Visualization

`cb viewer` emits a self-contained `vault-graph.html` to `exports/` (committed) with:

- Force-directed D3 layout.
- Node coloring by type.
- Edge styling by edge type.
- Community detection (Leiden, optional dependency) for highlighting "god nodes" — high-connectivity concepts that warrant special attention.
- Filter UI by type, namespace, profile, confidence range.
- Special view modes: "IFU history chains" highlights `preceded_by` / `followed_by` ladders on indications-for-use nodes; "predicate tree" highlights clearance lineage.

Lifted-inspiration from graphify; not lifted code. graphify's strength is source-code analysis via tree-sitter, which doesn't apply here. The viewer's UX patterns (the three-pane interactive HTML, the report file, the JSON export) are what we adopt.

Because the HTML is committed, team members without skills can still open `exports/vault-graph.html` in any browser and explore the graph visually.

## 16. External dependencies

### Required of the host system

- **git** ≥ 2.20. Universal in developer environments. Used for the scaffold init, commits, and as the basis for the distribution model. `cb scaffold --no-git` is the opt-out for users without git installed.
- **Python** ≥ 3.10.

### Python (installed automatically with `uv tool install company-brain`)

| Dependency | Purpose | License |
|---|---|---|
| `typer` or `click` | CLI framework | MIT/BSD |
| `jinja2` | Document templating | BSD |
| `pyyaml` | Frontmatter parsing | MIT |
| `python-docx` | Word output and atomization | MIT |
| `pdfplumber` | PDF intake (text + tables) | MIT |
| `markdown-it-py` | Markdown parsing | MIT |
| `rich` | CLI output formatting | MIT |
| `networkx` | Graph analytics (community detection) | BSD |
| `pillow` | Image handling for screenshot intake | HPND |

v1.x adds: `python-pptx` (PowerPoint), `openpyxl` (Excel output), optional `leidenalg` for higher-quality community detection, `httpx` + `selectolax` for the `cb fetch` HTTP fallback.

### Recommended MCP servers (optional)

| MCP | Used for | Required? |
|---|---|---|
| `chrome-devtools-mcp` | v1.x automated web-snapshot capture (full-page screenshot, DOM text, network requests). Install: `npx chrome-devtools-mcp@latest`. | Optional — manual screenshot import always works. |

### Recommended Claude Code skill companions

company-brain functions standalone but ingests from these skills' outputs when present:

- `competitor-profiling` — competitor research → `competitor` nodes + supporting `source` nodes.
- `customer-research` — research synthesis → `persona`, `customer`, `requirement` nodes.
- `product-marketing-context` — foundational context → `pillar` and `source` nodes.
- `write-spec` (PM plugin) — drafted specs → `requirement` and `feature` nodes.
- `competitive-brief` (PM plugin) — competitor analysis → `competitor` and `source` nodes.

None of these are install-time dependencies.

### Claude Code itself

Minimum version: whatever supports `skills/` directory format with frontmatter-defined skills as of 2026-05.

## 17. Build order

1. **Schema** — write `docs/schema.md`, define node + edge + profile + frontmatter in `src/company_brain/schema/`. Data classes and validators only.
2. **`vault-architect` skill + `cb scaffold`** — produces a valid empty vault for a given profile, including `_attachments/`, `_branding/`, `entities/indications-for-use/`, `risk/regulatory-clearances/`, and the rest of the medical-device folders. Runs `git init` and creates the initial commit by default.
3. **Hand-built example vault** — `examples/meddev-fictional/` populated by hand to stress-test the schema. Patient monitoring wearable + replaceable sensor pad. Includes: a competitor with two-version IFU history; a `regulatory-clearance` with predicate edges; a `web-snapshot` source with an attached PNG; decisions with `## What This Rules Out`; pillars-as-non-goals; vision-source nodes.
4. **`cb validate`** — exits clean on the example vault. Tests written against it.
5. **`intake` skill — `vision` and `product` sub-modes** — vision implements the six-phase flow. Skills emit structured git commit messages for the changes they introduce.
6. **`intake` skill — competitor sub-modes** — `competitor`, `competitor-ifu`, `competitor-clearance`, `competitor-snapshot` (manual screenshot import path).
7. **`atomize` skill — markdown, Word, PDF**.
8. **`atomize` skill — transcripts and image screenshots** (uses Claude vision for image text extraction).
9. **`query` skill** — IB retrieval analyst, profile-aware.
10. **`doc-generate` skill — MRD pipeline** — Jinja2 template, claim labeling, IFU comparison, source bibliography, anti-decision section, docx output. Consumes `_branding/` for assets and templates.
11. **`visualize` skill + `cb viewer`** — D3 HTML generator with IFU-chain and predicate-tree view modes.
12. **`maintain` skill** — decay + audit + repair, including `cb validate --fix` and INDEX.md regeneration.
13. **`doc-generate` scaffolds** — PID, business plan, competitive brief, risk brainstorm stubs.
14. **Second example vault** — `examples/saas-fictional/` to prove profile mechanism.
15. **Public release** — README, LICENSE, onboarding guide, controlled-document-boundary doc, vault-as-git-repository doc, competitive-archive doc, CHANGELOG, v0.1.0 on github.com/nemock.

## 18. v2 (deferred features)

Documented here so v1 doesn't paint into corners that block v2.

- **BOM / component / kit / sub-component** as first-class entities. `component` nodes referenced by multiple `kit` and `product` nodes via `part_of` edges. Edge metadata carries **quantity**. Sub-component hierarchy supported via recursive `part_of`.
- **Cross-kit overlap analytics.** `cb analyze --components` lists shared components, kits affected by a change, and BOM rollup costs.
- **Component dependency reasoning.** Query: "If we deprecate component X, which kits and products are affected, and what are their risk insights?"
- **Full PID, business plan, competitive brief, risk-brainstorm generators.**
- **PowerPoint atomization.**
- **SaaS, hardware, services profile content.**
- **Recurring competitor monitoring with diff alerts.**
- **Headless-browser fetcher** for JS-heavy sites without chrome-devtools-mcp.
- **Optional MCP server** that exposes the vault as a queryable resource for other agents (Claude Code, Cursor, etc.).

## 19. Success criteria for v1

- A new user can `uv tool install company-brain`, invoke `vault-architect` with `--profile medical-device`, complete a 30-minute vision intake session, atomize one project initiation Word doc and one transcript, import one competitor screenshot, paste one FDA 510(k) summary PDF, and generate an MRD that labels every claim by `source_kind` and includes a competitor IFU comparison table.
- The scaffolded vault is a git repo from the moment it lands, with a meaningful initial commit. The user can `git remote add origin <bitbucket-url> && git push` and a teammate can clone, install skills, and continue contributing.
- A teammate who has cloned the vault but has **not** installed company-brain can still open Obsidian, read every node, and view the latest `exports/MRD.md` and `exports/vault-graph.html`.
- `examples/meddev-fictional/` and `examples/saas-fictional/` both pass `cb validate` with zero errors.
- The MRD generator demonstrably distinguishes vision-driven claims from evidence-driven claims, and includes a "What we are explicitly not doing" section sourced from anti-decisions and non-goal pillars.
- The vision intake sub-mode survives a 5-minute messy dictated input and produces a useful set of typed nodes for review.
- Repo is published on github.com/nemock under MIT license, with a working README, onboarding guide, vault-as-git-repository doc, competitive-archive doc, and the controlled-document-boundary disclaimer.

## 20. Open items

All resolved.

Resolved:
- License: **MIT**.
- GitHub owner: **github.com/nemock**.
- Vision intake as its own sub-mode: **yes**, dedicated, six-phase flow.
- Vision review-loop UX: **batched table by default**, `--interactive` flag for one-at-a-time.
- Word atomization: **v1** (promoted from v1.x because pilot users have existing Word PIDs).
- Manual screenshot import: **v1**. chrome-devtools-mcp-assisted capture: **v1.x**.
- `cb fetch` polite HTTP fallback: **v1.x**, for users who haven't installed chrome-devtools-mcp.
- Pilot vault: **entirely private**. No pilot content, structure, or patterns enter the public repo. The fictional `meddev-fictional` example is the only medical-device reference in the project.
- Repo visibility: **public from day one**. v1.0.0 is the release tag and announcement, not the publication moment. README leads with a pre-1.0 under-active-development banner until v1.0.0 ships.
- Vault is a git repository by default: **yes**, `cb scaffold` runs `git init` and commits the skeleton; opt-out via `--no-git`.
- Branding folder: **`_branding/` at vault root**, holds logos, brand colors, fonts, optional doc-generate templates.
- `exports/` and `_attachments/` committed by default in production vaults.
- `_system/INDEX.md` generated and gitignored to avoid merge-conflict hotspots.

## 21. Glossary

- **Anti-decision**: a decision whose primary value is in what it rules out (e.g., "no physical documentation"). Captured as a `decision` node with a strong `## What This Rules Out` section.
- **Atomic node**: a single markdown file holding one concept, with typed frontmatter.
- **Attachments folder**: `_attachments/` inside the vault. Holds binary captures: screenshots, PDFs, raw HTML. Committed by default. Source nodes reference files here by relative path.
- **Branding folder**: `_branding/` inside the vault. Holds logos, brand colors, fonts, and optional jinja2 template overrides consumed by doc-generate. Committed.
- **Controlled document**: a document under formal change-control as part of a quality system. company-brain produces **none** of these.
- **Edge**: a typed, directional relationship between two nodes, declared in frontmatter.
- **Exports folder**: `exports/` inside the vault. Holds generated documents (MRD, PID, etc.) and the visualizer HTML. Committed by default so team members without skills can still read the latest output.
- **IFU (indication for use)**: the formal statement of what a medical device does, for whom, under what conditions, in what setting. In company-brain it is a node type with `population`, `condition`, `intervention`, `setting` fields. Versioned via a `preceded_by` chain.
- **Industry profile**: a configuration that determines which node types and intake modes are active in a vault.
- **Namespace**: a visibility scope on a node (workspace, brand, restricted, catalog).
- **Non-goal pillar**: a `pillar` written in negative form (e.g., "we will never enter the consumer market"), with an `applicable_when` that fires when an agent might propose entering that direction.
- **Predicate device**: in 510(k) clearance, the legally marketed device used to establish substantial equivalence. In company-brain, predicate relationships are first-class `preceded_by` edges between `regulatory-clearance` nodes.
- **Provenance**: the chain from a claim to its origin via `derived_from` edges to `source` nodes.
- **Regulatory clearance**: a specific clearance event (510(k), De Novo, PMA, etc.). One node per event.
- **Vault**: the markdown folder that holds a single company's knowledge graph. **A vault is also a git repository** — `cb scaffold` initializes it as one by default.
- **Vault repository**: synonym for vault — emphasizes that the vault is a git-tracked, push/pull-able artifact, distinct from the company-brain skills repo.
- **Web-snapshot**: a page captured at a moment in time, stored as a `source` node with the image/HTML in `_attachments/` and extracted text in the body.
