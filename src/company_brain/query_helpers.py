"""Read-only helpers consumed by the ``query`` skill.

The query skill is LLM-driven: Claude reads node files, walks edges, and
composes an answer. These helpers exist so the skill can do cheap candidate
selection without having to grep every file:

* ``cb list-nodes`` — emit a JSON array of node summaries (frontmatter
  fields that matter for retrieval, plus the relative path). Filterable by
  type, namespace, auto-inject-only.
* ``cb get-node <id>`` — emit one node's full frontmatter + body, plus its
  outbound edges and the inbound edges other nodes point at it from. The
  inbound view is what makes typed edge walks fast.

Nothing here writes. Vault loading is shared with the validator via
:mod:`company_brain.vault`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .vault import Edge, Node, Vault, VaultNotFoundError, load_vault


class QueryError(Exception):
    """Base class for errors raised by the query helpers."""


class NodeNotFoundError(QueryError):
    """The requested node id does not exist in the vault."""


# The subset of frontmatter fields we surface in list-nodes. Anything else
# is left out to keep the JSON payload tight — call get-node for the rest.
_SUMMARY_FIELDS = (
    "id",
    "title",
    "type",
    "namespace",
    "summary",
    "auto_inject",
    "applicable_when",
    "confidence",
    "verified_at",
    "verified_by",
    "staleness_signal",
    "tags",
    "source_kind",
    "producing_skill",
    "requirement_class",
    "volatility_class",
    "metric_id",
    "belongs_to_product",
    "legal_name",
    "canonical_url",
    "controlled_document",
)


def list_nodes(
    vault_path: Path,
    *,
    type_name: str | None = None,
    namespace: str | None = None,
    auto_inject_only: bool = False,
    source_kind: str | None = None,
) -> list[dict[str, Any]]:
    """Return a JSON-friendly summary of every matching node in the vault.

    Filters compose with AND semantics. The output is sorted by ``id`` so
    consumers get deterministic ordering.
    """

    vault = load_vault(vault_path)
    out: list[dict[str, Any]] = []
    for node in vault.nodes:
        if type_name is not None and node.type != type_name:
            continue
        if namespace is not None and str(node.frontmatter.get("namespace", "")) != namespace:
            continue
        if auto_inject_only and not bool(node.frontmatter.get("auto_inject", False)):
            continue
        if source_kind is not None and str(node.frontmatter.get("source_kind", "")) != source_kind:
            continue
        out.append(_summarize_node(node))
    out.sort(key=lambda n: str(n.get("id", "")))
    return out


def get_node(vault_path: Path, node_id: str) -> dict[str, Any]:
    """Return a full description of one node: frontmatter, body, edges (both directions)."""

    vault = load_vault(vault_path)
    node = vault.nodes_by_id.get(node_id)
    if node is None:
        raise NodeNotFoundError(
            f"node id '{node_id}' not found in vault at {vault_path}"
        )

    inbound = _inbound_edges(node_id, vault)
    return {
        "id": node.id,
        "type": node.type,
        "path": str(node.path),
        "frontmatter": _serialize_frontmatter(node.frontmatter),
        "body": node.body,
        "edges_outbound": [_edge_to_dict(e) for e in node.edges],
        "edges_inbound": inbound,
    }


def _summarize_node(node: Node) -> dict[str, Any]:
    fm = node.frontmatter
    summary: dict[str, Any] = {"path": str(node.path)}
    for field in _SUMMARY_FIELDS:
        if field in fm:
            value = fm[field]
            summary[field] = _normalize_value(value)
    summary["edges"] = [_edge_to_dict(e) for e in node.edges]
    return summary


def _inbound_edges(node_id: str, vault: Vault) -> list[dict[str, Any]]:
    inbound: list[dict[str, Any]] = []
    for other in vault.nodes:
        for edge in other.edges:
            if edge.target == node_id:
                inbound.append(
                    {
                        "source": other.id,
                        "type": edge.type,
                        "weight": edge.weight,
                        "note": edge.note,
                    }
                )
    inbound.sort(key=lambda e: (str(e.get("source", "")), str(e.get("type", ""))))
    return inbound


def _edge_to_dict(edge: Edge) -> dict[str, Any]:
    return {
        "target": edge.target,
        "type": edge.type,
        "weight": edge.weight,
        "note": edge.note,
    }


def _serialize_frontmatter(fm: dict[str, Any]) -> dict[str, Any]:
    """Strip the raw ``edges`` list from frontmatter — it's already surfaced
    structurally as ``edges_outbound`` in the response.
    """

    out: dict[str, Any] = {}
    for key, value in fm.items():
        if key == "edges":
            continue
        out[key] = _normalize_value(value)
    return out


def _normalize_value(value: Any) -> Any:
    """Convert non-JSON-friendly YAML values to strings."""

    # PyYAML returns dates as datetime.date; the CLI consumer wants strings.
    if hasattr(value, "isoformat") and not isinstance(value, str):
        return value.isoformat()
    if isinstance(value, list):
        return [_normalize_value(v) for v in value]
    if isinstance(value, dict):
        return {k: _normalize_value(v) for k, v in value.items()}
    return value


# Re-exported for the CLI so it doesn't have to import from .vault too.
__all__ = [
    "VaultNotFoundError",
    "NodeNotFoundError",
    "QueryError",
    "list_nodes",
    "get_node",
]
