---
title: "company-brain — Roadmap"
status: draft
date: 2026-05-20
---

# company-brain — Roadmap

Relative milestones, not dated. Each milestone is a coherent, shippable increment. The [PRD](PRD.md) is the source of truth for scope detail; this doc is the source of truth for sequencing.

Dates can be layered on later once the project owner has a sense of velocity. Order is non-negotiable for the v0.x milestones — each one depends on the previous.

---

## v0.1.0 — Schema and architect (foundation)

**Why first:** every other workstream depends on the schema being correct and the example vault being legible.

**Included:**
- Schema definitions in `src/company_brain/schema/`: node types, edge types, frontmatter, profile mechanism.
- `vault-architect` skill — creates a valid empty vault for a given profile, including `_system/`, `entities/`, `risk/` (medical-device), `_attachments/`, `exports/`.
- `examples/meddev-fictional/` hand-built — patient monitoring wearable + replaceable sensor pad. Includes a competitor with two-version IFU history, a `regulatory-clearance` with predicate edges, a `web-snapshot` source with an attached PNG, decisions with `## What This Rules Out`, pillars-as-non-goals, and vision-source nodes.
- `cb validate` CLI — exits clean on the example vault.
- Repo created **public** at `github.com/nemock/company-brain` with `README.md` skeleton, `LICENSE` (MIT), `pyproject.toml`, `docs/controlled-document-boundary.md`. Public from day one — every v0.x commit is visible. The README's top line states this is pre-1.0 and under active development.

**Unlocks:** the schema is grounded in real-looking nodes and machine-validated. All downstream skills can target a known-good shape.

**Done when:** `cb validate examples/meddev-fictional/` exits 0 and the example reads naturally to a med-device engineer.

---

## v0.2.0 — Intake (vision, product, competitor)

**Why next:** the most differentiated parts of the project (vision capture, competitor archive) need to exist before doc generation has anything interesting to render.

**Included:**
- `intake` skill with `vision` sub-mode (six-phase flow, batched-table review, `--interactive` flag).
- `intake` skill with `product` sub-mode.
- `intake` skill with `competitor`, `competitor-ifu`, `competitor-clearance`, `competitor-snapshot` (manual screenshot import path).
- `atomize` skill — markdown, Word, PDF.
- `atomize` skill — transcripts and image screenshots (Claude vision for text extraction from images).

**Unlocks:** users can start populating real vaults. The pilot company can begin ingesting existing project initiation documents and the messy product launch outline.

**Done when:** a 5-minute messy dictated input produces a useful set of typed nodes for review, and atomizing a Word PID produces correctly-typed requirement / stakeholder / decision nodes.

---

## v0.3.0 — Query and MRD

**Why next:** completes the round trip from intake to artifact. This is the milestone where company-brain proves its core value.

**Included:**
- `query` skill — IB retrieval analyst, profile-aware, walks edges, cites node ids.
- `doc-generate` skill with the full MRD pipeline:
  - Profile-aware section inclusion (medical-device-only sections omitted entirely for other profiles).
  - Evidence-vs-vision split.
  - Anti-decisions / non-goal section.
  - IFU comparison table (medical-device profile).
  - Source bibliography with `source_kind` labels.
- MRD output to markdown, docx, html.

**Unlocks:** the public-facing value proposition becomes real. From here, every demo can include "and now generate the MRD."

**Done when:** the meddev-fictional vault produces an MRD that labels every claim by source-kind, includes the IFU comparison and anti-decision sections, and re-runs idempotently.

---

## v0.4.0 — Visualize and maintain

**Why next:** long-term vault health and the signal that doc-generate is a category, not just MRD.

**Included:**
- `visualize` skill + `cb viewer` — D3 HTML, IFU chain view, predicate tree view, community detection.
- `maintain` skill — confidence decay (fact nodes linked to medium/high volatility metrics), audit, broken-edge repair, missing-inverse-edge auto-fix, INDEX.md drift repair.
- `cb validate --fix` implemented.
- `doc-generate` scaffolds for PID, business plan, competitive brief, risk brainstorm (runnable stubs that produce flagged skeleton output).

**Unlocks:** users have a long-term answer to "is my vault healthy?" and a visible promise of where the doc-generation roadmap is heading.

**Done when:** `cb validate --fix` repairs synthetic damage to the example vault, and each scaffold generator produces something for the meddev-fictional vault that adopters can fill in.

---

## v0.5.0 — Second example + polish

**Why next:** profile mechanism only earns trust when it's exercised by two profiles. Polish closes the gap to public release.

**Included:**
- `examples/saas-fictional/` — hand-built using a different profile (likely the `default` industry-agnostic profile to start; `saas` profile content slots stay reserved until v1.x).
- Complete documentation: `README.md`, `docs/adoption-guide.md`, `docs/competitive-archive.md`, `docs/profiles.md`, `docs/schema.md`.
- Fresh-user onboarding test: a user who has never seen the project should be able to install, scaffold, do a 30-minute intake, and generate an MRD without help.
- `CHANGELOG.md` covering v0.1.0 through v0.5.0.

**Unlocks:** public release readiness.

**Done when:** a person who has never seen the project completes the onboarding flow end-to-end and the resulting vault validates cleanly.

---

## v1.0.0 — Release tag and announcement

**Included:**
- Tag `v1.0.0` on `github.com/nemock/company-brain` (the repo has been public since v0.1.0; this is the release moment, not the publication moment).
- Public announcement (channel TBD — likely a short post on the project owner's blog or LinkedIn, possibly Show HN, possibly the AI Impact Skool community).
- Two-week listening window before starting v1.x work — early-adopter feedback shapes priorities.

**Done when:** the `v1.0.0` tag is published, the README leads with a clear value prop and a 5-minute quickstart, and at least one external user has run the full pipeline end-to-end.

---

## v1.x — Automation and depth

Order within v1.x is flexible; prioritized by user feedback after v1.0.0.

**Capture automation:**
- chrome-devtools-mcp-assisted `competitor-snapshot` — full-page screenshot via CDP, DOM text via `evaluate_script`, optional network-request manifest as a sibling source node.
- openFDA API integration: `cb intake-510k <K-number>` pulls structured fields and optionally the summary PDF.
- Multi-page crawl + change detection (snapshot diffing).
- Polite single-page HTTP fallback (`cb fetch`) — for users who haven't installed chrome-devtools-mcp. Uses `httpx` + a text-extraction library; respects robots.txt and rate limits; fails clearly on JS-heavy sites and tells the user to fall back to manual import or chrome-devtools-mcp.

**Format breadth:**
- PowerPoint atomization (`python-pptx`).

**Doc generators (full implementations to replace scaffolds):**
- PID generator.
- Competitive brief generator.
- Business plan generator.
- Risk brainstorm generator (medical-device).

**Integration:**
- Wrapper around the existing `competitor-profiling` skill that writes directly into the vault rather than emitting a standalone markdown file.

**Done when:** the chrome-devtools-mcp path is the documented happy path for competitor capture, all four scaffolded generators are fully implemented, and openFDA ingestion handles a 510(k) with no manual intervention.

---

## v2 — BOM and beyond

The features held back because v1 didn't need them and they would have widened the schema before it was stable.

**BOM and components:**
- `component`, `kit`, `bom-item` node types as first-class.
- **Quantity-bearing `part_of` edges** — the edge schema extension that v1 deliberately avoided.
- Sub-component hierarchy via recursive `part_of`.
- Cross-kit overlap analytics: `cb analyze --components` lists shared components, kits affected by a change, BOM rollup costs.
- Component dependency reasoning queries: "If we deprecate component X, which kits and products are affected, and what are their risk insights?"

**Monitoring:**
- Recurring competitor snapshot jobs ("re-scan these 8 competitors monthly").
- IFU drift alerting.
- Press-release topic clustering across the snapshot corpus.

**Capture without chrome-devtools-mcp:**
- Headless-browser fetcher for users who haven't installed chrome-devtools-mcp.

**Ecosystem:**
- Optional MCP server exposing the vault as a queryable resource for other agents (Claude Code, Cursor, etc.).
- Confluence / Notion / Obsidian Sync export adapters.

**Profile content:**
- SaaS, hardware, services profile node types and intake sub-modes fleshed out.

---

## Sequencing rules

- **Each v0.x milestone gates the next.** No parallelization until v1.0.0 ships. A small project shipping in order is easier to reason about than a large project shipping in parallel.
- **Within a milestone, build example-vault content before validating in code.** Schema mistakes are cheaper to find by writing real-looking nodes than by writing tests against a hypothetical schema.
- **The [PRD §16 build order](PRD.md) is the canonical step sequence within v1.0.0.** This roadmap aggregates those steps into shippable releases; the PRD is the authority on what each step contains.
- **v1.x and v2 reorder freely** based on user feedback after public release. The lists above are not in priority order.
