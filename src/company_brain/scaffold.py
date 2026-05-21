"""Vault scaffolding.

Creates the on-disk structure for a new company-brain vault, including:

* All node-type folders active for the chosen profile
* ``_attachments/`` (heavy binaries — gitignored by convention)
* ``exports/`` (generated documents)
* ``_system/PROFILE.md`` declaring the active profile
* ``_system/INDEX.md`` (empty starter)
* ``_system/NODE-TYPES.md``, ``EDGE-TYPES.md``, ``FRONTMATTER-SCHEMA.md``
  rendered from :mod:`company_brain.schema` data filtered by profile

Folder creation is idempotent. ``_system/*.md`` files refuse to overwrite by
default; pass ``force=True`` to regenerate them (useful when the schema
package has been updated and a vault needs its system docs refreshed).

This module never writes node content. That is the job of the ``intake`` and
``atomize`` skills.
"""

from __future__ import annotations

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
    today: date | None = None,
    verified_by: str | None = None,
) -> VaultScaffoldResult:
    """Scaffold a vault at ``vault_path`` for the given profile.

    Args:
      vault_path: target directory. Created if missing.
      profile_name: must resolve to a registered profile.
      force: if True, regenerate ``_system/*.md`` even when they already exist.
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
        path = system_dir / filename
        if path.exists() and not force:
            result.files_skipped.append(path)
            continue
        path.write_text(content, encoding="utf-8")
        result.files_written.append(path)

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
        vault_path / "exports",
    }
    for spec in active_types:
        folder_set.add(vault_path / spec.folder)

    # Sort so test assertions are stable. mkdir(parents=True) handles the
    # implied parent chain.
    return sorted(folder_set)


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
