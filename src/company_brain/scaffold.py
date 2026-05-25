"""Vault scaffolding.

Creates the on-disk structure for a new company-brain vault, including:

* All node-type folders active for the chosen profile
* ``_attachments/`` (binary captures — committed by default)
* ``_branding/`` (logos, colors, optional doc templates — committed)
* ``exports/`` (generated documents — committed)
* ``_system/PROFILE.md`` declaring the active profile
* ``_system/INDEX.md`` (starter; gitignored at the vault level)
* ``_system/NODE-TYPES.md``, ``EDGE-TYPES.md``, ``FRONTMATTER-SCHEMA.md``
  rendered from :mod:`company_brain.schema` data filtered by profile
* A vault-level ``.gitignore`` matched to the schema
* A vault-level ``README.md`` identifying the vault

By default, ``scaffold()`` also runs ``git init``, writes the initial
commit, and leaves the vault as a ready-to-push git repository. Pass
``init_git=False`` to skip the git steps (useful for example vaults that
live inside another git repo, or for users without git installed).

Folder creation is idempotent. ``_system/*.md``, ``_branding/*``, and the
vault ``.gitignore`` / ``README.md`` refuse to overwrite by default; pass
``force=True`` to regenerate them.

This module never writes node content. That is the job of the ``intake`` and
``atomize`` skills.
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from . import __version__
from .schema import (
    BASE_REQUIRED_FIELDS,
    EDGE_TYPE_SPECS,
    NodeCategory,
    NodeTypeSpec,
    Profile,
    get_active_node_types,
    get_profile,
)


# Marker pair the `cb maintain rebuild-readme` pass regenerates between.
# Anything outside these markers in the vault-level README.md is preserved
# across maintain runs; anything between them gets rewritten.
AUTO_README_START = "<!-- cb:auto START -->"
AUTO_README_END = "<!-- cb:auto END -->"


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------


@dataclass
class VaultScaffoldResult:
    """Summary of what scaffold() did."""

    vault_path: Path
    profile_name: str
    folders_created: list[Path] = field(default_factory=list)
    files_written: list[Path] = field(default_factory=list)
    files_skipped: list[Path] = field(default_factory=list)
    git_initialized: bool = False
    git_initial_commit: str | None = None
    git_skipped_reason: str | None = None

    @property
    def folder_count(self) -> int:
        return len(self.folders_created)

    @property
    def file_count(self) -> int:
        return len(self.files_written)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


class ProfileNotFoundError(ValueError):
    """Raised when an unknown profile name is passed to scaffold()."""


def scaffold(
    vault_path: Path,
    profile_name: str,
    *,
    force: bool = False,
    init_git: bool = True,
    today: date | None = None,
    verified_by: str | None = None,
) -> VaultScaffoldResult:
    """Scaffold a vault at ``vault_path`` for the given profile.

    Args:
      vault_path: target directory. Created if missing.
      profile_name: must resolve to a registered profile.
      force: if True, regenerate ``_system/*.md``, ``_branding/`` starters,
        ``.gitignore``, and ``README.md`` even when they already exist.
      init_git: if True (default), run ``git init`` and create an initial
        commit. No-op if the directory is already inside a git repo's
        working tree or if git is not installed.
      today: override the scaffold date (for deterministic tests).
      verified_by: handle to use for ``verified_by`` in any seeded frontmatter.
        Not used in v0.1.0 since no nodes are written, but reserved.

    Returns:
      :class:`VaultScaffoldResult` describing what was created / skipped.

    Raises:
      ProfileNotFoundError: if ``profile_name`` is unknown.
      NotADirectoryError: if ``vault_path`` exists but is not a directory.
    """

    profile = get_profile(profile_name)
    if profile is None:
        raise ProfileNotFoundError(
            f"unknown profile '{profile_name}'. Run `cb scaffold --help` to see options."
        )

    if vault_path.exists() and not vault_path.is_dir():
        raise NotADirectoryError(f"{vault_path} exists and is not a directory")

    today = today or date.today()
    result = VaultScaffoldResult(vault_path=vault_path, profile_name=profile_name)
    active_types = get_active_node_types(profile_name)

    # --- folders ------------------------------------------------------------
    folder_paths = _enumerate_folders(vault_path, active_types)
    for folder in folder_paths:
        existed = folder.exists()
        folder.mkdir(parents=True, exist_ok=True)
        if not existed:
            result.folders_created.append(folder)

    # --- _system files ------------------------------------------------------
    system_files: dict[str, str] = {
        "PROFILE.md": _render_profile_md(profile, today),
        "INDEX.md": _render_index_md(profile),
        "NODE-TYPES.md": _render_node_types_md(profile, active_types),
        "EDGE-TYPES.md": _render_edge_types_md(),
        "FRONTMATTER-SCHEMA.md": _render_frontmatter_schema_md(active_types),
    }

    system_dir = vault_path / "_system"
    for filename, content in system_files.items():
        _write_or_skip(system_dir / filename, content, force=force, result=result)

    # --- _branding starter files -------------------------------------------
    branding_dir = vault_path / "_branding"
    _write_or_skip(branding_dir / "colors.yaml", _render_branding_colors_yaml(), force=force, result=result)
    _write_or_skip(branding_dir / "README.md", _render_branding_readme(), force=force, result=result)

    # --- vault-level .gitignore and README ---------------------------------
    _write_or_skip(vault_path / ".gitignore", _render_gitignore(), force=force, result=result)
    _write_or_skip(
        vault_path / "README.md",
        _render_vault_readme(profile, today),
        force=force,
        result=result,
    )

    # --- git init + initial commit -----------------------------------------
    if init_git:
        _init_git_and_commit(vault_path, profile, result)

    return result


# ---------------------------------------------------------------------------
# Folder enumeration
# ---------------------------------------------------------------------------


def _enumerate_folders(vault_path: Path, active_types: tuple[NodeTypeSpec, ...]) -> list[Path]:
    """Compute the full set of folders to create.

    Returns a stable, deduplicated list rooted at ``vault_path``.
    """

    folder_set: set[Path] = {
        vault_path,
        vault_path / "_system",
        vault_path / "_attachments",
        vault_path / "_branding",
        vault_path / "exports",
    }
    for spec in active_types:
        folder_set.add(vault_path / spec.folder)

    # Sort so test assertions are stable. mkdir(parents=True) handles the
    # implied parent chain.
    return sorted(folder_set)


# ---------------------------------------------------------------------------
# File writer helper
# ---------------------------------------------------------------------------


def _write_or_skip(
    path: Path, content: str, *, force: bool, result: VaultScaffoldResult
) -> None:
    """Write ``content`` to ``path`` unless it exists and ``force`` is False."""

    if path.exists() and not force:
        result.files_skipped.append(path)
        return
    path.write_text(content, encoding="utf-8")
    result.files_written.append(path)


# ---------------------------------------------------------------------------
# Renderers (private; tests exercise them via the public scaffold() entry)
# ---------------------------------------------------------------------------


def _render_profile_md(profile: Profile, today: date) -> str:
    activated = profile.activated_node_type_names
    activated_section = (
        "\n".join(f"- `{name}`" for name in activated)
        if activated
        else "_(none — this profile activates no additional node types in v1.)_"
    )

    footer_note = (
        "Every document generated for this vault carries the controlled-document-boundary footer."
        if profile.appends_controlled_document_footer
        else "This profile does not append the controlled-document-boundary footer."
    )

    profile_notes = (
        "\n".join(f"- {note}" for note in profile.notes) if profile.notes else "_(no extra notes)_"
    )

    return f"""---
profile: {profile.name}
profile_version: 1.0
scaffolded_at: {today.isoformat()}
scaffolded_by_company_brain_version: {__version__}
controlled_document: false
---

# Vault Profile

This vault uses the **{profile.name}** profile.

{profile.description}

## Activated profile-conditional node types

{activated_section}

## Profile notes

{profile_notes}

## Document generation

{footer_note}

## Lifecycle

The profile is set at vault creation and not designed to be flipped in place. Re-scaffolding into the same directory with a different profile will leave orphan folders from the previous profile.

## Schema source of truth

This file is human-readable; the authoritative schema lives in the [company-brain Python package](https://github.com/nemock/company-brain) under `src/company_brain/schema/`. The companion docs `_system/NODE-TYPES.md`, `_system/EDGE-TYPES.md`, and `_system/FRONTMATTER-SCHEMA.md` are rendered from that source.
"""


def _render_index_md(profile: Profile) -> str:
    return f"""# Master Node Index

This file is the agent's primary entry point. The `maintain` skill keeps it in sync as nodes are added; for now it is a starter scaffold.

**Active profile**: `{profile.name}`.

> `_system/INDEX.md` is gitignored at the vault level. It is regenerated by `cb` on demand and is not part of the committed history. The committed authority is the per-folder node files.

## Retrieval protocol

1. **Phase 1**: read summaries here and any pillar with `auto_inject: true` whose `applicable_when` matches the question.
2. **Phase 2**: load full bodies for surviving candidates and walk their `edges` frontmatter one hop. Most answers live within one or two hops.

## Node tables

Total nodes: 0.

_(No nodes yet. Use the `intake` or `atomize` skill to add some, then run `cb validate --fix` to populate this index.)_
"""


def _render_node_types_md(profile: Profile, active_types: tuple[NodeTypeSpec, ...]) -> str:
    by_category: dict[NodeCategory, list[NodeTypeSpec]] = {c: [] for c in NodeCategory}
    for spec in active_types:
        by_category[spec.category].append(spec)

    sections: list[str] = [
        "# Node Types",
        "",
        f"Active profile: `{profile.name}`. This file is rendered from the company-brain schema package; do not edit by hand. To refresh after a company-brain upgrade, run `cb scaffold --force`.",
        "",
    ]

    category_titles = {
        NodeCategory.EPISTEMIC: "Epistemic",
        NodeCategory.ENTITY: "Entity",
        NodeCategory.PROFILE_CONDITIONAL: "Profile-conditional",
    }

    for category, types in by_category.items():
        if not types:
            continue
        sections.append(f"## {category_titles[category]} ({len(types)})")
        sections.append("")
        for spec in types:
            sections.append(f"### `{spec.name}`")
            sections.append("")
            sections.append(f"- **Folder**: `{spec.folder}/`")
            sections.append(f"- **Purpose**: {spec.description}")
            if spec.extra_required_fields:
                fields = ", ".join(f"`{f.name}`" for f in spec.extra_required_fields)
                sections.append(f"- **Additional required fields**: {fields}")
            if spec.notes:
                sections.append("- **Notes**:")
                for note in spec.notes:
                    sections.append(f"  - {note}")
            sections.append("")

    return "\n".join(sections).rstrip() + "\n"


def _render_edge_types_md() -> str:
    lines: list[str] = [
        "# Edge Types",
        "",
        "v1 inherits the Infinite Brain edge set unchanged. This file is rendered from the schema package; do not edit by hand.",
        "",
        "## Edge frontmatter shape",
        "",
        "Each entry in a node's `edges` list:",
        "",
        "```yaml",
        "edges:",
        "  - target: pillar-pricing-philosophy",
        "    type: supports",
        "    weight: 0.9",
        '    note: "This decision expresses the pricing pillar."',
        "```",
        "",
        "- `target` must resolve to an existing node id (validated by `cb validate`).",
        "- `type` must be one of the registered edge types below.",
        "- `weight` is a float in `[0, 1]`.",
        "- `note` is optional but encouraged.",
        "",
        "## Registered edge types",
        "",
        "| Name | Symmetric? | Inverse | Default weight | Use when |",
        "|---|---|---|---|---|",
    ]
    for spec in EDGE_TYPE_SPECS:
        sym = "yes" if spec.symmetric else "no"
        inv = f"`{spec.inverse}`" if spec.inverse else "—"
        lines.append(
            f"| `{spec.name}` | {sym} | {inv} | {spec.default_weight} | {spec.description} |"
        )
    lines.append("")
    return "\n".join(lines)


def _render_frontmatter_schema_md(active_types: tuple[NodeTypeSpec, ...]) -> str:
    lines: list[str] = [
        "# Frontmatter Schema",
        "",
        "This file is rendered from the company-brain schema package; do not edit by hand.",
        "",
        "## Base required fields (all nodes)",
        "",
        "| Field | Type | Required? | Description |",
        "|---|---|---|---|",
    ]
    for spec in BASE_REQUIRED_FIELDS:
        required = "yes" if spec.required else "optional"
        lines.append(
            f"| `{spec.name}` | {spec.type.value} | {required} | {spec.description} |"
        )

    types_with_extras = [t for t in active_types if t.extra_required_fields]
    if types_with_extras:
        lines.extend(
            [
                "",
                "## Additional required fields by node type",
                "",
            ]
        )
        for spec in types_with_extras:
            lines.append(f"### `{spec.name}`")
            lines.append("")
            lines.append("| Field | Type | Description |")
            lines.append("|---|---|---|")
            for field_spec in spec.extra_required_fields:
                lines.append(
                    f"| `{field_spec.name}` | {field_spec.type.value} | {field_spec.description} |"
                )
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _render_gitignore() -> str:
    return """# company-brain vault-level .gitignore
# See https://github.com/nemock/company-brain — docs/vault-as-git-repository.md

# Generated; rebuild with `cb` on demand
_system/INDEX.md

# Obsidian per-machine workspace state
.obsidian/workspace*.json

# OS / editor cruft
.DS_Store
Thumbs.db
*.swp
*.swo
.vscode/
.idea/
"""


def _render_branding_colors_yaml() -> str:
    return """# Brand colors and typography for company-brain doc-generate.
# Edit to match your company's brand. Consumed by jinja2 templates in
# src/company_brain/templates/ (overridable from _branding/templates/).

primary: "#1f2a44"
secondary: "#4f6cb6"
accent: "#f59e0b"
text: "#374151"
background: "#ffffff"
muted: "#9ca3af"

# Typography
font_family_headings: "Helvetica Neue, Arial, sans-serif"
font_family_body: "Georgia, serif"
"""


def _render_branding_readme() -> str:
    return """# _branding/

Holds the company's brand assets for use by the `doc-generate` skill. Committed to git so all team members see the same brand on regenerated documents.

## Files

- `colors.yaml` — palette and typography. Edit to match your company's brand.
- `logo.png` (optional) — primary logo used in document headers. Drop in if you have one.
- `templates/` (optional) — jinja2 template overrides for specific documents. company-brain ships defaults; this folder lets you override.

## Used by

`doc-generate` reads from this folder when rendering MRD, PID, business plan, etc., to produce documents that match the company's brand.

## Convention

Anything in `_branding/` is committed by default. The folder is intentionally small — a logo, a colors file, optional templates. Heavier shared assets belong in `_attachments/`.
"""


def _render_vault_readme(profile: Profile, today: date) -> str:
    """Render the comprehensive vault-level README.

    The block between ``AUTO_README_START`` and ``AUTO_README_END`` is
    refreshed in place by ``cb maintain repair`` / ``cb maintain
    rebuild-readme``. Everything outside the markers is the user's to
    edit and survives across regenerations.
    """

    is_meddev = profile.name == "medical-device"

    layout_rows = [
        "| `_system/` | Schema reference docs (rendered from the schema package). `INDEX.md` is gitignored and rebuilt on demand. |",
        "| `_branding/` | Logos, brand colors, fonts, optional doc templates. |",
        "| `_attachments/` | Binary captures: screenshots, PDFs, raw HTML. Referenced by source nodes. |",
        "| `exports/` | Generated documents (MRD, PID, etc.) and the visualizer HTML. |",
    ]
    if is_meddev:
        layout_rows.append(
            "| `pillars/`, `decisions/`, `entities/`, `risk/`, ... | Node folders, one per node type. |"
        )
    else:
        layout_rows.append(
            "| `pillars/`, `decisions/`, `entities/`, ... | Node folders, one per node type. |"
        )
    layout_table = "\n".join(layout_rows)

    # Profile-conditional row inside the "Kinds of data" table.
    kinds_risk_row = (
        "| `risk/` | Medical-device risk and regulatory nodes (see below). | Planning-level safety and regulatory thinking, present because this vault uses the **medical-device** profile. Every risk node is explicitly **not** a controlled document. |\n"
        if is_meddev
        else ""
    )

    # Profile-conditional "Inside risk/" subsection.
    inside_risk_section = (
        """
### Inside `risk/`

Medical-device planning nodes, all carrying `controlled_document: false`: `risk-insights/` (planning-level observations, not risk records), `hazards/`, `hazardous-situations/`, `harms/`, `risk-control-ideas/` (candidate mitigations under consideration, not chosen controls), `regulatory-clearances/` (510(k) / De Novo / PMA events, chained by predicate), `regulations/` (e.g. 21 CFR 820, MDR), and `standards/` (e.g. ISO 14971, IEC 62304).
"""
        if is_meddev
        else ""
    )

    # Profile-conditional bit inside "Inside entities/".
    inside_entities_ifu_clause = (
        " and — under the medical-device profile — `indications-for-use/` (population + condition + intervention + setting for a product)"
        if is_meddev
        else ""
    )

    # Profile-conditional intake-skill sub-modes blurb.
    intake_sub_modes = (
        "vision, product, persona, competitor, competitor-ifu, competitor-clearance, competitor-snapshot, metric, meeting-notes, risk, clearance"
        if is_meddev
        else "vision, product, persona, competitor, competitor-snapshot, metric, meeting-notes"
    )

    # Profile-conditional MRD line.
    mrd_profile_note = (
        "The MRD is profile-aware: this medical-device vault gets §3 Indications-for-use and §7 Regulatory landscape, and the controlled-document footer is appended. A default-profile vault omits those sections and the numbers shift to fill the gap."
        if is_meddev
        else "The MRD is profile-aware: this default-profile vault has nine sections. A medical-device profile vault adds §3 Indications-for-use and §7 Regulatory landscape, and appends a controlled-document footer."
    )

    return f"""# Company Brain Vault

A [company-brain](https://github.com/nemock/company-brain) knowledge vault, scaffolded {today.isoformat()} for the **{profile.name}** profile.

## What this is

An AI-native knowledge graph of a company — products, people, decisions, vision, evidence, competitive landscape. The graph lives in Obsidian-compatible markdown so humans can browse it; the typed schema makes it cheap for agents to retrieve from.

**This vault is a git repository.** Clone it, browse with any markdown viewer (Obsidian recommended), and read the latest generated documents from `exports/`. With the [company-brain](https://github.com/nemock/company-brain) skills installed, you can also contribute new nodes via the `intake` and `atomize` skills.

{AUTO_README_START}
## What's in this vault right now

_This section is regenerated by `cb maintain repair` and `cb maintain rebuild-readme`. Edits inside the markers are overwritten — change vault content via `intake` / `atomize` and re-run maintain. Edits **outside** the markers are preserved._

**Vault state:** newly scaffolded — 0 nodes. Run `intake` or `atomize` to start populating, then re-run `cb maintain repair`.
{AUTO_README_END}

## Layout

| Path | What's there |
|---|---|
{layout_table}

## Kinds of data in the graph

The graph is built from **typed nodes** — each node is one markdown file, in a folder named for its type. The folders differ by what kind of thing or claim they hold, and (just as important) by how much they are allowed to shape future answers. Nodes carry frontmatter and connect through typed edges; most non-source nodes cite a `source` via a `derived_from` edge.

| Folder | What it holds | How it differs from the others |
|---|---|---|
| `pillars/` | Durable governing principles, including strategic non-goals ("we do *not* …"). | The constitution. These are auto-injected into agent answers, so every response is shaped by them. A pillar is meant to endure, where a decision records a single choice. |
| `decisions/` | Concrete choices between alternatives, each with a "What this rules out" section. | Point-in-time commitments. A decision records *this* choice and the options it closes off, rather than stating an enduring principle. |
| `facts/` | Verified atomic claims, including metric snapshots. | Evidence — something believed true and citable. Facts tied to volatile metrics lose confidence over time (decay). A hypothesis, by contrast, is not yet verified. |
| `hypotheses/` | Falsifiable predictions or bets, not yet proven. | Unproven. What separates a hypothesis from a fact is verification; what separates it from a pillar is that it is a wager, not a principle. |
| `sources/` | External material (decks, filings, transcripts, web snapshots) plus synthesis. | Provenance anchors — *where the knowledge came from*. Most other nodes point back to a source via `derived_from`. Every source declares its `source_kind`. |
| `entities/` | The nouns of the business (see below). | Things, not claims. The objects that facts, decisions, and pillars talk about. |
{kinds_risk_row}| `exports/` | Generated documents: MRD, one-pager, visualizer HTML. | **Derived output, not source of truth.** Everything here is rendered from the nodes by `cb render` and can be regenerated at any time — never hand-edit it. |

### Inside `entities/`

The entity nouns, each in its own subfolder: `products/`, `product-lines/`, `personas/` (archetypal users), `customers/` (named real customers), `stakeholders/` (parties with influence on the program), `competitors/`, `vendors/`, `requirements/` (market, user, system, software, or hardware — each tagged with its class so it is never mistaken for a controlled design input), `features/`, `use-cases/`, and `metrics/` (the *concept* of a measurement; the actual numbers live as fact snapshots){inside_entities_ifu_clause}.
{inside_risk_section}
> The schema defines more node types than this vault currently uses. Epistemic types such as `concepts/`, `playbooks/`, `patterns/`, `questions/`, and `notes/` appear as that kind of knowledge gets captured. See [`_system/NODE-TYPES.md`](_system/NODE-TYPES.md) for the full authoritative list.

## The skills

These work in any Claude Code conversation with company-brain installed. The skill loader matches your wording against each skill's description, so plain English works — you don't need to type `/skill-name`.

| Skill | What it does |
|---|---|
| [`vault-architect`](https://github.com/nemock/company-brain/blob/main/skills/vault-architect/SKILL.md) | Scaffold a new vault (`cb scaffold`). Runs once per company. |
| [`intake`](https://github.com/nemock/company-brain/blob/main/skills/intake/SKILL.md) | Conversational capture into typed nodes. Sub-modes: {intake_sub_modes}. |
| [`atomize`](https://github.com/nemock/company-brain/blob/main/skills/atomize/SKILL.md) | Ingest existing docs (markdown, Word, PDF, transcripts, image screenshots) into typed nodes with provenance. |
| [`query`](https://github.com/nemock/company-brain/blob/main/skills/query/SKILL.md) | Answer questions against the graph. Auto-injects pillars, walks typed edges, cites node ids, flags vision-vs-evidence and staleness. |
| [`doc-generate`](https://github.com/nemock/company-brain/blob/main/skills/doc-generate/SKILL.md) | Render planning documents from the graph. Ships full **MRD** (md / html / docx) and **one-pager** (md / html), plus 19 scaffolds (PID, business plan, sales battle card, SRD/SRS/HRS, decision log, risk brainstorm, etc.). |
| [`maintain`](https://github.com/nemock/company-brain/blob/main/skills/maintain/SKILL.md) | Audit and repair the vault. `cb maintain repair` (auto-fix filename-id, missing inverse edges, controlled_document flag; regen `_system/INDEX.md`; regen the auto-section in this README). `cb maintain decay` (half-life confidence decay on fact snapshots). |
| [`visualize`](https://github.com/nemock/company-brain/blob/main/skills/visualize/SKILL.md) | D3 interactive HTML viewer (`cb viewer`). Modes: `graph` (default), `ifu-chain` (medical-device), `predicate-tree` (medical-device). |

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
cb maintain        <subcommand>              # repair | decay | audit | rebuild-index | rebuild-readme
cb viewer          [--mode ...]              # D3 HTML graph viewer
cb install-skills                            # symlink skills into ~/.claude/skills
```

## What you can ask the skills to do

Every example below has the equivalent `cb` command shown underneath, in case you want to bypass the skills. Run `cb` commands from inside the vault (or pass `--path <vault>`).

### Capture knowledge (intake)

> Let's do a vision intake. I'll dictate.

> Capture a competitor: Acme Robotics at https://acme-robotics.example.com.

> I just finished a customer call. Here are the notes: ...

> Add a metric: "Procedures per device per day", medium volatility.

The intake skill picks the right sub-mode from what you say. Every captured node lands in the right folder with the right frontmatter and a `derived_from` edge to a source node.

### Ingest existing documents (atomize)

> Atomize this investor deck into the vault: `~/Downloads/intro-deck.pdf`.

> Atomize this customer interview transcript: `~/transcripts/2026-04-12-customer.txt`.

> Read this competitor product-page screenshot and capture it as a web-snapshot source: `~/screenshots/acme-2026-05-20.png`.

> Atomize the output of the competitor-profiling skill at `~/research/acme.md`.

Atomize handles binary formats via `cb extract`, images via Claude's native vision, and recognizes the structure of known skill outputs (competitor-profiling, customer-research, write-spec, etc.).

```bash
cb extract ~/Downloads/intro-deck.pdf       # text only, for inspection
```

### Query the graph

> What are our governing principles?

> What are we explicitly NOT doing?

> Which claims in the vault are vision-driven vs. evidence-driven?

> Who are our competitors?

The query skill loads the auto-injecting pillars first (so its answers are governed by the company's principles), then walks typed edges to find evidence. Every load-bearing claim cites a node id.

```bash
cb list-nodes --auto-inject-only                    # all governing pillars
cb list-nodes --type competitor
cb list-nodes --type decision
cb get-node <some-node-id>                          # full node + edges both ways
```

### Generate documents (doc-generate)

> Generate an MRD for this vault.

> Generate the MRD as a docx.

> Generate the one-pager as HTML.

> Generate a sales battle card against our top competitor.

```bash
cb render mrd                                       # → exports/MRD.md
cb render mrd --format html                         # → exports/MRD.html
cb render mrd --format docx                         # → exports/MRD.docx
cb render one-pager                                 # → exports/one-pager.md
cb render decision-log
cb render sales-battle-card --competitor <id>
cb render mrd --date 2026-05-24                     # pin date (idempotency tests)
```

{mrd_profile_note}

### Visualize the graph

```bash
cb viewer                                           # → vault-graph.html
cb viewer --mode ifu-chain                          # medical-device only
cb viewer --mode predicate-tree                     # medical-device only
```

Single self-contained HTML file. D3 v7 from CDN; vault data embedded as JSON. Hover for tooltip, click for detail, drag and zoom.

### Maintain the vault

```bash
cb maintain audit                                   # read-only health summary
cb maintain repair                                  # auto-fix + INDEX.md regen + README auto-section regen
cb maintain repair --dry-run                        # preview without writing
cb maintain decay                                   # half-life decay on fact snapshots
cb maintain rebuild-index                           # regenerate _system/INDEX.md only
cb maintain rebuild-readme                          # regenerate the README auto-section only
cb validate --fix                                   # validate after auto-repair
```

### Inspection and schema

```bash
cb describe-profile --path .                        # describe the active profile
cb describe-node <type>                             # node-type spec
```

## Branding the output

Drop files under `_branding/`:

- `colors.yaml` — overrides primary, secondary, accent, text, background, muted, font_family_headings, font_family_body. CSS variables in the generated HTML pick them up.
- `logo.png` / `logo.jpg` / `logo.svg` — picked up if present (full embed in HTML/docx lands in a later milestone).
- `templates/<doc>.md.j2` — override the bundled template for any of the 21 doc types (e.g. `mrd.md.j2`, `business-plan.md.j2`, `sales-battle-card.md.j2`).
- `templates/html-wrapper.html.j2` — override the bundled HTML page chrome.

No flags needed — the render commands automatically pick up overrides when they exist.

## Idempotency

`cb render` produces byte-identical output for the same vault + pinned `--date`. The generation date lives only in the footer line. This makes git diffs on `exports/` meaningful — you can read the diff to see what *content* changed, not just "the docs got regenerated." (DOCX is the exception: zip-metadata variability means its bytes differ on each render even when the visible content is unchanged.)

## Controlled-document boundary

This vault is a **planning** layer. It is not a controlled documentation system. See [company-brain's controlled-document-boundary doc](https://github.com/nemock/company-brain/blob/main/docs/controlled-document-boundary.md) before using this vault in any regulated context.

## Maintenance

- `cb validate` — check the vault for schema issues.
- `cb maintain repair` — auto-fix issues, regenerate `_system/INDEX.md`, and refresh the auto-section of this README.
- `cb scaffold --force` — regenerate `_system/*.md`, `_branding/` starters, and this README after a company-brain upgrade. **Hand edits to this README outside the auto-markers are preserved by `cb maintain repair` but are overwritten by `cb scaffold --force`.**
"""


# ---------------------------------------------------------------------------
# Git integration
# ---------------------------------------------------------------------------


def _init_git_and_commit(
    vault_path: Path, profile: Profile, result: VaultScaffoldResult
) -> None:
    """Run ``git init`` and create the initial commit if appropriate.

    No-ops (without error) when:
      * git is not on PATH;
      * ``vault_path`` is already inside a git working tree;
      * the working tree already has commits (avoid trampling).

    Sets ``result.git_initialized`` / ``result.git_initial_commit`` /
    ``result.git_skipped_reason`` to reflect what happened.
    """

    git = shutil.which("git")
    if git is None:
        result.git_skipped_reason = "git not installed"
        return

    # Are we already inside someone else's git working tree?
    inside_existing = _is_inside_git_working_tree(git, vault_path)

    # Does vault_path itself already have a .git/ directory?
    has_own_git_dir = (vault_path / ".git").is_dir()

    if inside_existing and not has_own_git_dir:
        result.git_skipped_reason = "vault_path is inside an existing git working tree"
        return

    if not has_own_git_dir:
        _run_git(git, ["init", "-b", "main"], cwd=vault_path)
        result.git_initialized = True

    # If the repo already has commits, don't auto-commit again.
    if _has_commits(git, vault_path):
        result.git_skipped_reason = (result.git_skipped_reason or "") + (
            " (no auto-commit: repo already has commits)"
        ).lstrip()
        return

    # Stage and commit.
    _run_git(git, ["add", "."], cwd=vault_path)

    # Only commit if there's something staged.
    status = _run_git(git, ["status", "--porcelain"], cwd=vault_path, capture=True)
    if not status.strip():
        result.git_skipped_reason = "nothing to commit"
        return

    commit_msg = (
        f"Initial company-brain scaffold ({profile.name} profile)\n\n"
        f"Scaffolded with company-brain v{__version__}.\n"
    )
    _run_git(git, ["commit", "-m", commit_msg], cwd=vault_path)

    sha = _run_git(git, ["rev-parse", "HEAD"], cwd=vault_path, capture=True).strip()
    result.git_initial_commit = sha or None


def _is_inside_git_working_tree(git: str, cwd: Path) -> bool:
    """Ask git whether ``cwd`` is inside an existing working tree."""

    if not cwd.exists():
        return False
    try:
        proc = subprocess.run(
            [git, "rev-parse", "--is-inside-work-tree"],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
    except (FileNotFoundError, OSError):
        return False
    return proc.returncode == 0 and proc.stdout.strip() == "true"


def _has_commits(git: str, cwd: Path) -> bool:
    proc = subprocess.run(
        [git, "rev-parse", "--verify", "HEAD"],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode == 0


def _run_git(
    git: str, args: list[str], *, cwd: Path, capture: bool = False
) -> str:
    """Run ``git <args>`` in ``cwd`` and return stdout (if capture) else ``''``."""

    proc = subprocess.run(
        [git, *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True,
    )
    return proc.stdout if capture else ""
