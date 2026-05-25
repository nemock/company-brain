"""D3-based interactive HTML visualization of a vault graph (v0.4.0 step 3).

The viewer is a single self-contained HTML file the user can open in any
browser — no server required. D3 is loaded from CDN; the vault data is
embedded as a ``<script>`` JSON island.

Three view modes:

* ``graph`` (default) — every node, every edge. Color by node type.
* ``ifu-chain`` — only ``indication-for-use`` nodes connected via
  ``preceded_by`` / ``followed_by``. Medical-device profile only.
* ``predicate-tree`` — only ``regulatory-clearance`` nodes connected via
  ``preceded_by``. Medical-device profile only.

Community detection (mentioned in PRD §15) is deferred to a later
milestone — the v0.4.0 bar is a usable graph, IFU chain, and predicate
tree.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from . import __version__
from .render.engine import build_environment, load_branding
from .vault import Node, Vault, VaultNotFoundError, load_vault


VIEW_MODES = ("graph", "ifu-chain", "predicate-tree")
_MEDDEV_MODES = frozenset({"ifu-chain", "predicate-tree"})


class ViewerProfileError(ValueError):
    """Raised when a view mode requires a profile this vault doesn't use."""


@dataclass
class ViewerResult:
    content: str
    output_path: Path | None
    mode: str
    node_count: int
    link_count: int


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def render_viewer(
    vault_path: Path,
    *,
    output_path: Path | None = None,
    mode: str = "graph",
    write: bool = True,
    generation_date: date | None = None,
) -> ViewerResult:
    """Render the viewer HTML for the vault.

    Defaults to writing ``<vault>/vault-graph.html``. Pass ``write=False``
    to get just the rendered string back.
    """

    if mode not in VIEW_MODES:
        raise ValueError(
            f"unknown viewer mode '{mode}'. One of: {', '.join(VIEW_MODES)}"
        )

    vault = load_vault(vault_path)
    profile = vault.profile_name or "default"

    if mode in _MEDDEV_MODES and profile != "medical-device":
        raise ViewerProfileError(
            f"the '{mode}' view mode requires the medical-device profile; "
            f"this vault uses '{profile}'."
        )

    branding = load_branding(vault_path)
    graph = _build_graph(vault, mode=mode)

    env = build_environment(vault_path)
    template = env.get_template("viewer.html.j2")

    context = {
        "meta": {
            "vault_path": str(vault.path),
            "profile": profile,
            "mode": mode,
            "cb_version": __version__,
            "generation_date": (generation_date or date.today()).isoformat(),
            "node_count": len(graph["nodes"]),
            "link_count": len(graph["links"]),
        },
        "branding": branding.as_dict(),
        "graph_json": json.dumps(graph, sort_keys=True, separators=(",", ":")),
    }
    html = template.render(**context)

    target = output_path or (vault_path / "vault-graph.html")
    if write:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")

    return ViewerResult(
        content=html,
        output_path=target if write else None,
        mode=mode,
        node_count=len(graph["nodes"]),
        link_count=len(graph["links"]),
    )


# ---------------------------------------------------------------------------
# Graph assembly
# ---------------------------------------------------------------------------


def _build_graph(vault: Vault, *, mode: str) -> dict[str, list[dict[str, Any]]]:
    """Return ``{"nodes": [...], "links": [...]}`` as plain dicts the JSON
    island in the template can embed verbatim. Sorted for idempotency.
    """

    if mode == "graph":
        nodes, links = _build_full_graph(vault)
    elif mode == "ifu-chain":
        nodes, links = _build_ifu_chain(vault)
    elif mode == "predicate-tree":
        nodes, links = _build_predicate_tree(vault)
    else:  # pragma: no cover - guarded above
        raise ValueError(mode)

    nodes.sort(key=lambda n: n["id"])
    links.sort(key=lambda e: (e["source"], e["type"], e["target"]))
    return {"nodes": nodes, "links": links}


def _node_payload(node: Node) -> dict[str, Any]:
    fm = node.frontmatter
    return {
        "id": node.id,
        "type": node.type,
        "title": str(fm.get("title", node.id)),
        "summary": str(fm.get("summary", "")),
        "namespace": str(fm.get("namespace", "")),
        "confidence": fm.get("confidence"),
        "verified_at": _to_str(fm.get("verified_at")),
        "source_kind": fm.get("source_kind"),
    }


def _to_str(value: Any) -> str | None:
    if value is None:
        return None
    if hasattr(value, "isoformat") and not isinstance(value, str):
        return value.isoformat()
    return str(value)


def _build_full_graph(
    vault: Vault,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    nodes_by_id = vault.nodes_by_id
    nodes = [_node_payload(n) for n in vault.nodes if n.id]
    links: list[dict[str, Any]] = []
    for node in vault.nodes:
        if not node.id:
            continue
        for edge in node.edges:
            if edge.target not in nodes_by_id:
                continue
            links.append(
                {
                    "source": node.id,
                    "target": edge.target,
                    "type": edge.type,
                    "weight": edge.weight,
                }
            )
    return nodes, links


def _build_ifu_chain(
    vault: Vault,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    ifu_nodes = [n for n in vault.nodes if n.type == "indication-for-use"]
    ifu_ids = {n.id for n in ifu_nodes}
    nodes = [_node_payload(n) for n in ifu_nodes]
    links: list[dict[str, Any]] = []
    for n in ifu_nodes:
        for edge in n.edges:
            if edge.type not in {"preceded_by", "followed_by"}:
                continue
            if edge.target not in ifu_ids:
                continue
            links.append(
                {
                    "source": n.id,
                    "target": edge.target,
                    "type": edge.type,
                    "weight": edge.weight,
                }
            )
    return nodes, links


def _build_predicate_tree(
    vault: Vault,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    clearances = [n for n in vault.nodes if n.type == "regulatory-clearance"]
    clearance_ids = {n.id for n in clearances}
    nodes = [_node_payload(n) for n in clearances]
    links: list[dict[str, Any]] = []
    for n in clearances:
        for edge in n.edges:
            if edge.type != "preceded_by":
                continue
            if edge.target not in clearance_ids:
                continue
            links.append(
                {
                    "source": n.id,
                    "target": edge.target,
                    "type": edge.type,
                    "weight": edge.weight,
                }
            )
    return nodes, links


__all__ = [
    "VIEW_MODES",
    "ViewerProfileError",
    "ViewerResult",
    "VaultNotFoundError",
    "render_viewer",
]
