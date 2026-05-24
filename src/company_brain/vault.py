"""Vault loading.

A vault is a folder containing ``_system/PROFILE.md`` plus one markdown file
per node, organized into the folders the active profile activates. This module
walks a vault, parses every node's frontmatter and body, and returns an
in-memory representation that the validator, render, and query layers all
share.

I/O lives here; schema lookups live in :mod:`company_brain.schema`.

Public API:

* :class:`Vault`, :class:`Node`, :class:`Edge` — value classes.
* :func:`load_vault` — read a vault from disk.
* :class:`VaultNotFoundError` — raised when ``vault_path`` is missing or not
  a vault (no ``_system/PROFILE.md``).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


# Folders we never crawl for nodes.
_SKIP_DIR_NAMES = frozenset(
    {"_system", "_attachments", "_branding", "exports", ".git"}
)


@dataclass
class Edge:
    """A typed directional relationship declared in node frontmatter."""

    target: str
    type: str
    weight: float
    note: str | None = None


@dataclass
class Node:
    """One markdown node file, parsed.

    ``path`` is relative to the vault root so it survives moves of the vault
    on disk (the render and query layers want a stable identifier).
    """

    path: Path
    id: str
    type: str
    frontmatter: dict[str, Any]
    edges: list[Edge]
    body: str = ""


@dataclass
class Vault:
    """An in-memory snapshot of the vault on disk.

    Construct via :func:`load_vault`. Mutation is intentional (the maintain
    skill mutates in place) but render and query code should treat instances
    as read-only.
    """

    path: Path
    profile_name: str | None
    nodes: list[Node] = field(default_factory=list)

    @property
    def nodes_by_id(self) -> dict[str, Node]:
        return {n.id: n for n in self.nodes if n.id}

    def nodes_by_type(self, type_name: str) -> list[Node]:
        return [n for n in self.nodes if n.type == type_name]


class VaultNotFoundError(FileNotFoundError):
    """The vault path is missing or doesn't have ``_system/PROFILE.md``."""


class NodeParseError(Exception):
    """A markdown file in the vault could not be parsed as a node.

    The vault loader catches this and skips the file rather than raising;
    callers that want strict loading can use :func:`parse_node` directly.
    """


def load_vault(vault_path: Path) -> Vault:
    """Read a vault from disk into an in-memory :class:`Vault`.

    Walks the vault tree, parses every markdown file that has frontmatter
    (skipping ``_system``, ``_attachments``, ``_branding``, ``exports``,
    ``.git`` and the top-level ``README.md``), and returns the result.

    Unparseable files are silently skipped here — the validator catches
    them via separate base-field checks. Render and query callers that
    encounter a missing id should treat the vault as malformed and route
    the user through ``cb validate`` first.

    Raises :class:`VaultNotFoundError` when the path is missing or doesn't
    look like a vault.
    """

    if not vault_path.exists():
        raise VaultNotFoundError(f"{vault_path} does not exist")
    if not vault_path.is_dir():
        raise VaultNotFoundError(f"{vault_path} is not a directory")

    profile_md = vault_path / "_system" / "PROFILE.md"
    if not profile_md.is_file():
        raise VaultNotFoundError(
            f"{vault_path} does not look like a company-brain vault "
            f"(missing _system/PROFILE.md)"
        )

    profile_name = _read_active_profile(profile_md)
    vault = Vault(path=vault_path, profile_name=profile_name)

    for md_path in _iter_node_files(vault_path):
        try:
            node = parse_node(md_path, vault_path)
        except NodeParseError:
            continue
        vault.nodes.append(node)
    return vault


def parse_node(path: Path, vault_path: Path) -> Node:
    """Parse one markdown file into a :class:`Node`.

    Raises :class:`NodeParseError` for files without frontmatter or with
    malformed YAML.
    """

    text = path.read_text(encoding="utf-8")
    fm_text, body = split_frontmatter(text)
    if fm_text is None:
        raise NodeParseError(f"no frontmatter in {path}")
    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError as exc:
        raise NodeParseError(f"YAML parse error in {path}: {exc}") from exc
    if not isinstance(fm, dict):
        raise NodeParseError(f"frontmatter in {path} is not a mapping")

    node_id = str(fm.get("id", ""))
    node_type = str(fm.get("type", ""))

    raw_edges = fm.get("edges") or []
    edges: list[Edge] = []
    if isinstance(raw_edges, list):
        for raw in raw_edges:
            if not isinstance(raw, dict):
                continue
            try:
                edges.append(
                    Edge(
                        target=str(raw.get("target", "")),
                        type=str(raw.get("type", "")),
                        weight=float(raw.get("weight", 0.5)),
                        note=raw.get("note"),
                    )
                )
            except (TypeError, ValueError):
                continue

    return Node(
        path=path.relative_to(vault_path),
        id=node_id,
        type=node_type,
        frontmatter=fm,
        edges=edges,
        body=body,
    )


def split_frontmatter(text: str) -> tuple[str | None, str]:
    """Return ``(frontmatter_yaml, body)``. If no frontmatter, ``(None, text)``."""

    if not text.startswith("---"):
        return None, text
    rest = text[3:]
    end = rest.find("\n---")
    if end == -1:
        return None, text
    fm = rest[:end].strip("\n")
    body = rest[end + len("\n---"):]
    # Strip the single newline that follows the closing fence, if present,
    # so consumers don't double-up on blank lines.
    if body.startswith("\n"):
        body = body[1:]
    return fm, body


def _read_active_profile(profile_md: Path) -> str | None:
    text = profile_md.read_text(encoding="utf-8")
    fm_text, _ = split_frontmatter(text)
    if not fm_text:
        return None
    try:
        data = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        return None
    profile = data.get("profile") if isinstance(data, dict) else None
    return str(profile) if profile else None


def _iter_node_files(vault_path: Path) -> list[Path]:
    results: list[Path] = []
    for path in sorted(vault_path.rglob("*.md")):
        rel_parts = path.relative_to(vault_path).parts[:-1]
        if any(part in _SKIP_DIR_NAMES for part in rel_parts):
            continue
        if path == vault_path / "README.md":
            continue
        results.append(path)
    return results
