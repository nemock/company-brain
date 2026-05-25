# Changelog

All notable changes to company-brain. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The schema is data; profile / node-type / edge-type additions are minor-version-breaking only if they require existing vaults to change. Additions that older vaults can ignore are non-breaking.

## [0.5.0] — 2026-05-25

The second-example milestone. Profile mechanism is now exercised by two profiles end to end. Onboarding documentation is complete.

### Added

- **`examples/saas-fictional/`** — second example vault using the `default` (industry-agnostic) profile. Fictional B2B SaaS engineering analytics company ("Loftwing"). ~30 hand-built nodes covering every active type in the default profile, with all 22 export formats committed under `examples/saas-fictional/exports/` as reference output.
- **`docs/adoption-guide.md`** — step-by-step walkthrough from `uv tool install` to a first generated MRD. Replaces the v0.1.0 placeholder.
- **`docs/profiles.md`** — explains the profile mechanism with worked examples of `medical-device` vs. `default`. Replaces the v0.1.0 placeholder.
- **`docs/competitive-archive.md`** — full documentation of the four-node pattern (`competitor` + `web-snapshot` source + `indication-for-use` + `regulatory-clearance`) and the queries it unlocks. Replaces the v0.1.0 placeholder.
- **CHANGELOG.md** (this file).
- `tests/test_saas_example.py` — 26 parametrized tests asserting the saas-fictional vault stays validatable, profile-correct, and renderable.

### Changed

- Version bump to `0.5.0` in `pyproject.toml` and `src/company_brain/__init__.py`. All example exports regenerated to carry the v0.5.0 footer.

### Tests

339 passing, ruff clean.

---

## [0.4.0] — 2026-05-25

Visualize, maintain, and the 19 doc scaffolds. The pipeline now goes end-to-end: scaffold → intake/atomize → query → render (21 doc types) → maintain → visualize.

### Added

- **`maintain` skill + `cb maintain` command group.** Four subcommands: `repair` (auto-fix filename-id mismatches, missing inverse edges, missing `controlled_document: false` on risk/IFU nodes), `decay` (half-life confidence decay on fact snapshots tied to volatile metrics; preserves original via `confidence_original` for idempotency), `audit` (read-only health summary), `rebuild-index` (regenerate `_system/INDEX.md`). `cb validate --fix` wires into the same repair pass; drops the v0.1.0 stub.
- **19 doc scaffolds via `cb render <doc-name>`** for: PID, project-charter, stakeholder-register, risk-register (medical-device), status-report, meeting-minutes, lessons-learned, business-plan, sales-battle-card, competitive-brief, ifu-comparison (medical-device), decision-log, press-release, investor-update, onboarding-doc, srd, srs, hrs, risk-brainstorm (medical-device). Each scaffold queries the right typed nodes, fills in what it can, and flags the output as a scaffold in the footer.
- **`visualize` skill + `cb viewer`.** Self-contained D3 HTML graph viewer. Three modes: `graph` (default, full force-directed), `ifu-chain` (medical-device only), `predicate-tree` (medical-device only). Branding palette feeds the CSS variables; template override at `_branding/templates/viewer.html.j2`.
- `sales-battle-card --competitor <id>` for per-competitor rendering; embeds competitor id in the output filename.
- `tests/test_maintain.py`, `tests/test_render_scaffolds.py`, `tests/test_viewer.py` — 104 new tests.

### Changed

- Version bump to `0.4.0`. All example exports regenerated.

### Tests

287 passing (was 171), ruff clean.

---

## [0.3.0] — 2026-05-24

Query, MRD, and one-pager. The first full round-trip from typed graph to generated planning document.

### Added

- **`query` skill + `cb list-nodes` + `cb get-node`.** Read-only JSON helpers that let the IB-style retrieval flow stay cheap (summary metadata via `list-nodes`, full node + edges-both-directions via `get-node`). Full `query/SKILL.md` describes pillar auto-injection, staged candidate selection, typed edge walks, citation discipline, and vision-vs-evidence flagging.
- **`doc-generate` MRD generator** — full implementation with profile-aware section inclusion, evidence-vs-vision split (walks `derived_from` edges to classify each claim node by source kind), IFU comparison matrix (medical-device), anti-decisions section (`## What This Rules Out` blocks from decisions + non-goal pillars), source bibliography with `source_kind` labels, controlled-document footer (medical-device only).
- **`doc-generate` one-pager generator** — short doc proving the framework is general. Picks primary product, highest-confidence positive pillar, first persona, primary feature, first customer-interview source. Degrades gracefully on sparse vaults.
- **Three output formats** — markdown (always), HTML (branded wrapper with CSS variables from `_branding/colors.yaml`, markdown→HTML via `markdown-it-py`), DOCX (small markdown-to-docx writer covering headings, paragraphs, bullets, blockquotes, tables, inline bold/code; heading colors from branding primary).
- **Branding integration** — `_branding/colors.yaml` overrides palette; `_branding/templates/<doc>.md.j2` overrides bundled template; `_branding/templates/html-wrapper.html.j2` overrides the HTML chrome.
- **Idempotency contract** — `cb render` produces byte-identical output for the same vault + pinned `--date`. Stable sort orders everywhere; generation date lives in exactly one footer line.
- `jinja2>=3.1` runtime dependency. `markdown-it-py` came in as a transitive dep through `rich`.
- Shared `vault.py` loader (extracted from `validator.py`) so render / query / maintain all share one parser.
- `tests/test_query_helpers.py`, `tests/test_render_mrd.py`, `tests/test_render_one_pager.py`, `tests/test_render_formats.py` — 49 new tests.

### Changed

- Version bump to `0.3.0`. Example MRD / one-pager / HTML / DOCX committed under `examples/meddev-fictional/exports/` as reference output.
- Full `query/SKILL.md` and `doc-generate/SKILL.md` replace the v0.1.0 placeholders.

### Tests

171 passing (was 122), ruff clean.

---

## [0.2.0] — 2026-05-24

Intake and atomize. Vault content can now be authored by skills rather than only by hand.

### Added

- **`intake` skill** — conversational capture into typed nodes. Sub-modes: `vision` (dictation-friendly six-phase flow), `product`, `persona`, `competitor`, `competitor-ifu`, `competitor-clearance`, `competitor-snapshot`, `metric`, `meeting-notes`, `risk` (medical-device), `clearance` (medical-device).
- **`atomize` skill** — ingest existing documents into typed nodes with provenance. Formats: markdown / plain text (direct read), Word (`python-docx`), PDF (`pdfplumber`), interview transcripts (timestamp recognition), image screenshots (Claude vision). Recognizes known skill-output structures (`competitor-profiling`, `customer-research`, `write-spec`, etc.) and routes content accordingly. Special handling for FDA 510(k) summary PDFs.
- **`cb describe-profile`** — JSON description of the active profile in a vault, or by name. Used by intake/atomize to stay aligned with the schema.
- **`cb describe-node <type>`** — JSON description of one node type's spec including extra-required-fields. Accepts `--path` for active-in-this-vault verification.
- **`cb extract <file>`** — text extraction for `.docx` and `.pdf`. Used by atomize.
- **`cb install-skills`** — symlinks the seven skills into `~/.claude/skills/` (or `--target`). Idempotent; conflict-aware.
- Schema bump: `requirement_class` accepts `software` and `hardware` alongside `market` / `user` / `system` (enables future SRS / HRS doc generators).
- `tests/test_intake_helpers.py`, `tests/test_install_skills.py`, `tests/test_cli_describe_node.py` — 20 new tests.

### Changed

- Full `intake/SKILL.md` and `atomize/SKILL.md` replace the v0.1.0 placeholders.

---

## [0.1.0] — 2026-05-21

Schema and architect — the foundation.

### Added

- **Schema package** (`src/company_brain/schema/`): node types (30 across epistemic / entity / profile-conditional categories), edge types (10), source kinds (14), industry profiles (`default`, `medical-device`, plus reserved slots for `saas` / `hardware` / `services`), frontmatter spec.
- **`vault-architect` skill + `cb scaffold`** — creates a valid empty vault for a given profile. Writes `_system/PROFILE.md`, `NODE-TYPES.md`, `EDGE-TYPES.md`, `FRONTMATTER-SCHEMA.md` (rendered from the schema package), `_branding/colors.yaml` starter, vault-level `.gitignore` and `README.md`. Runs `git init` and creates the initial commit by default (`--no-git` opts out).
- **`cb validate`** — checks every node markdown file against the schema. Reports broken edges, missing required fields, duplicate ids, unknown types, folder/type mismatches, filename/id mismatches, missing source-kinds, invalid requirement-class / volatility-class, controlled-document violations in risk/IFU folders, edge-weight-out-of-range, and more.
- **`examples/meddev-fictional/`** — hand-built medical-device example vault (fictional Vitalisens ambulatory cardiac monitor + replaceable pad). Exercises every active node type in the medical-device profile, including the IFU history chain, the 510(k) predicate chain, decisions with `## What This Rules Out`, non-goal pillars, the controlled-document boundary.
- Docs scaffolds: `docs/controlled-document-boundary.md` (complete), `docs/schema.md` (complete), `docs/profiles.md`, `docs/adoption-guide.md`, `docs/competitive-archive.md` (placeholders pending their respective milestones).
- Public repository at `github.com/nemock/company-brain` under MIT license, banner notes pre-1.0 / under-active-development.
- GitHub Actions CI: install via uv, ruff check, pytest, all three Python versions (3.10, 3.11, 3.12).
- 75 tests.

### Project conventions established

- One commit per logical sub-piece, direct to `main`.
- One commit message per sub-piece naming the milestone step.
- Tests must remain green before push; CI re-validates on the 3.10 / 3.11 / 3.12 matrix.
- Output idempotency: anything generated by `cb` is deterministic given the same inputs.

---

## Pre-v0.1.0

Scaffolding only. No tagged releases.
