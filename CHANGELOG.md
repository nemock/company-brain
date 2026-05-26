# Changelog

All notable changes to company-brain. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The schema is data; profile / node-type / edge-type additions are minor-version-breaking only if they require existing vaults to change. Additions that older vaults can ignore are non-breaking.

## [0.7.0] — 2026-05-26

Document-driven intake. The first version cycle to make the *intake → render* loop work the other way around: instead of capturing knowledge and hoping the resulting MRD reads well, start from the MRD's section structure and let the doc drive what gets captured. Two CLI helpers, one shipped question manifest (MRD), one new intake sub-mode. Built for voice-dictated sessions where the operator rambles across topics; the LLM extracts the on-topic content and silently files stray facts into other sections of the same doc.

### Added

- **`src/company_brain/intake/`** — new package housing document-driven intake helpers. Public API: `load_manifest`, `list_manifests`, `filter_for_profile`, `compute_gaps`, `manifest_to_dict`, `gaps_to_dict`, plus typed dataclasses (`Manifest`, `Section`, `FeedsFrom`, `Question`, `SlotStatus`, `SectionGap`).
- **Question-manifest format** (`src/company_brain/intake/manifests/<doc>.yaml`) — declarative YAML describing a target document as an ordered list of sections, each with intent paragraph, profile gating, `feeds_from` slots (node-type + role + minimum count), and dictation-friendly question prompts. Hand-written; not derived from render code — manifests carry interview-time concerns (prompts, intents, completeness rules) that don't exist render-side.
- **`src/company_brain/intake/manifests/mrd.yaml`** — first shipped manifest. 9 interview sections (executive summary, vision and positioning, indications for use [medical-device], market and personas, market requirements, competitive landscape, regulatory landscape [medical-device], open questions, non-goals); sections 8 (evidence-vs-vision split) and 11 (sources bibliography) are computed at render time and aren't part of the interview. Profile gating drops the two medical-device sections on non-meddev vaults.
- **`cb describe-doc-questions <doc> [--path <vault>]`** — emit a question manifest as JSON. Without `--path`, the full manifest is returned. With `--path`, sections whose `profile_required` doesn't match the vault's active profile are dropped before emission.
- **`cb gaps-for-doc <doc> [--path <vault>]`** — emit a per-section gap report. Each section classifies as `complete` (every `feeds_from` slot at or above its `min`), `partial` (some nodes present but not all slots satisfied), or `empty` (no slot has any matching node). Role discriminators handled: `pillar` `positive`/`non-goal`, `decision` `rules-out`, `requirement` by `requirement_class`, `source` by `source_kind`.
- **`intake` skill: new `for-doc` sub-mode** documented in `skills/intake/SKILL.md`. Walks the target doc's sections in order, skipping `complete` ones (announced up front), confirming `partial` ones, posing the questions on `empty` ones. After each rambling answer the LLM extracts the on-topic content into the section's `captures` node type, silently files stray facts that match another section's `feeds_from`, and re-runs `gaps-for-doc` before the next section so later-section auto-fills get caught. Resumable — nodes are written as the session proceeds, so a stopped session resumes at the first still-empty section on the next run. Ends with a captured-summary, `cb validate`, and an offer to `cb render`.

### Tests

384 passing (346 baseline + 38 new). Coverage spans manifest loading (well-formed + 8 malformed-input error paths), profile filtering, gap detection against both shipped example vaults including role-discriminator correctness (positive-vs-non-goal pillars, rules-out decisions, market requirements), serialization round-trips, the two new CLI subcommands (happy paths + error paths + idempotency), and an empty-vault sanity check that every section lands as `empty`.

### Design choices

- **CLI subcommands are read-only.** Like the existing `describe-*`, `list-nodes`, `get-node` helpers, both new subcommands emit JSON for LLM consumption. The interview itself is LLM-driven, not CLI-driven — there's no `cb intake for-doc` command.
- **Stray-fact scope is narrow.** The LLM files a stray fact only when it matches another section's `feeds_from` in the active doc. Broader filing (any active node type) stays out for v1; if the pattern proves useful we can add it behind a `--liberal-stray` flag later.
- **One manifest in v0.7.0, more on demand.** The other 20 doc types add manifests as adopters surface the need. The pattern is data-driven, so each new manifest is a YAML file, not new code.

---

## [0.6.0] — 2026-05-25

Field-report polish. The first version cycle driven by operating a real medical-device vault (`AiM_Wiki`, ~61 nodes) and surfacing the rough edges that hadn't shown up in the example vaults. Every change here originated as a friction point flagged in production.

### Added

- **`cb maintain init-readme-markers`** — non-destructive marker injection for vaults whose README was scaffolded before the `<!-- cb:auto -->` convention landed. Inserts the marker pair at a sensible default location (between the first and second `##` heading, configurable via `--position`). All hand-curated content is preserved; the next `cb maintain rebuild-readme` populates the auto-block. The upgrade path that lets adopters move to the marker-based world without losing their README content.
- **`cb maintain init-gitignore-markers`** — symmetric command for the vault `.gitignore`. Prepends the `# cb:gitignore-managed` marker block to a legacy file; user-added rules (`node_modules/`, `*.mp4`, build artifacts, etc.) are preserved below the managed block. Future `cb scaffold --force` runs splice the managed block in place.
- **`cb scaffold --reset-branding`** — opt-in flag (used in combination with `--force`) that overwrites `_branding/colors.yaml` and `_branding/README.md` back to scaffold defaults. Without it, `--force` now skips the branding starters by design.

### Changed

- **`cb scaffold --force` is now safe to re-run on every upgrade.** Three behavioral shifts working together:
  - **README.** When the existing README has `<!-- cb:auto -->` markers, `--force` performs an in-place splice — the auto-block is refreshed from current vault state and everything outside the markers stays byte-identical to the user's hand-curated content. Legacy READMEs without markers still get the v0.5.0 full-overwrite (no content to preserve); the migration path is `cb maintain init-readme-markers` once.
  - **`.gitignore`.** Marker-aware splice on `--force`: only the block between `# cb:gitignore-managed START` and `END` is rewritten. User-added rules outside the markers survive. Legacy `.gitignore` without markers is preserved as-is (skipped, not clobbered).
  - **`_branding/`.** `colors.yaml` and `README.md` are no longer overwritten by `--force` alone — these are user-customized brand assets. Pass `--reset-branding` for explicit reset.
- **DOCX render is now byte-deterministic.** Two sources of churn normalized: docx core properties (`<dcterms:created>`, `<dcterms:modified>`, author, last_modified_by) are stamped to `generation_date` at midnight UTC / a stable string instead of wall-clock + OS user; and the underlying zip is re-packed with name-sorted entry order and a fixed (1980-01-01) per-entry timestamp. `cb render mrd --format docx --date <pinned>` now produces byte-identical bytes on every run, matching the idempotency contract for markdown and HTML.
- **README auto-section exports table is now filtered.** Skips files starting with `_` or `.`, skips `vault-graph*` (viewer convention; doesn't belong in `exports/`), and restricts to known doc extensions (`.md`, `.html`, `.docx`, `.pdf`, `.xlsx`, `.csv`). No more `_build_vault_graph.py` or other helpers crowding the table.
- **`cb scaffold --force` on a populated vault now refreshes the README auto-block from current vault state** instead of resetting it to the "0 nodes" empty-vault stub.

### Fixed

- `cb scaffold --force` was clobbering hand-curated README content outside the cb:auto markers (the entire point of the marker convention). Recovery was previously a `git restore`. Fixed via the in-place splice path above.
- `cb scaffold --force` was reverting `.gitignore` to the bare scaffold default, silently dropping user-added patterns (`node_modules/`, `*.app`, `*.mp4`, language artifacts). Fixed via marker-aware splice.
- "Latest exports" table in the README auto-section was listing helper scripts and the viewer output alongside real documents. Fixed via the filter rules above.
- DOCX bytes drifted between renders even when the visible content was unchanged (zip metadata + wall-clock core properties). Fixed via the determinism work above.

### Tests

346 passing, ruff clean. Net delta from v0.5.0: +33 tests, primarily covering marker preservation across all the new `--force` paths and the byte-equality assertion on DOCX output.

### Field-report status

All five friction points from the production AiM_Wiki vault session are resolved:

| # | Friction | Commit |
|---|---|---|
| 1 | `--force` clobbered README outside markers | `3bff716` |
| 2 | `--force` reset `.gitignore` to bare default | `e4619fd` |
| 3 | `--force` reset auto-section to "0 nodes" | `3bff716` |
| 4 | Exports table listed helpers / viewer output | `3bff716` |
| 5 | DOCX non-deterministic | `a84aef3` |

---

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
