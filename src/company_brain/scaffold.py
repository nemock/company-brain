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
    return f"""# Company Brain Vault

A [company-brain](https://github.com/nemock/company-brain) knowledge vault, scaffolded {today.isoformat()} for the **{profile.name}** profile.

## What this is

An AI-native knowledge graph of a company — products, people, decisions, vision, evidence, competitive landscape. The graph lives in Obsidian-compatible markdown so humans can browse it; the typed schema makes it cheap for agents to retrieve from.

**This vault is a git repository.** Clone it, browse with any markdown viewer (Obsidian recommended), and read the latest generated documents from `exports/`. With the [company-brain](https://github.com/nemock/company-brain) skills installed, you can also contribute new nodes via the `intake` and `atomize` skills.

## Layout

| Path | What's there |
|---|---|
| `_system/` | Schema reference docs (rendered from the schema package). `INDEX.md` is gitignored and rebuilt on demand. |
| `_branding/` | Logos, brand colors, fonts, optional doc templates. |
| `_attachments/` | Binary captures: screenshots, PDFs, raw HTML. Referenced by source nodes. |
| `exports/` | Generated documents (MRD, PID, etc.) and the visualizer HTML. |
| `pillars/`, `decisions/`, `entities/`, `risk/`, ... | Node folders, one per node type. |

## Controlled-document boundary

This vault is a **planning** layer. It is not a controlled documentation system. See [company-brain's controlled-document-boundary doc](https://github.com/nemock/company-brain/blob/main/docs/controlled-document-boundary.md) before using this vault in any regulated context.

## Maintenance

- `cb validate` — check the vault for schema issues.
- `cb scaffold --force` — regenerate `_system/*.md`, `_branding/` starters, and this README after a company-brain upgrade.
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
