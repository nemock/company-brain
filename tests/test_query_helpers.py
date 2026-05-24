"""Tests for the read-only query helpers used by the `query` skill."""

from __future__ import annotations

from pathlib import Path

import pytest

from company_brain.query_helpers import (
    NodeNotFoundError,
    VaultNotFoundError,
    get_node,
    list_nodes,
)


REPO_ROOT = Path(__file__).parent.parent
MEDDEV_VAULT = REPO_ROOT / "examples" / "meddev-fictional"


# ---------------------------------------------------------------------------
# list_nodes
# ---------------------------------------------------------------------------


def test_list_nodes_returns_every_node_in_example_vault() -> None:
    nodes = list_nodes(MEDDEV_VAULT)
    # The example vault ships with 65 markdown files; the validator drops
    # the README and _system/* so we expect a non-trivial node count.
    assert len(nodes) > 40
    # Sorted by id, deterministic.
    ids = [n["id"] for n in nodes]
    assert ids == sorted(ids)


def test_list_nodes_filters_by_type() -> None:
    pillars = list_nodes(MEDDEV_VAULT, type_name="pillar")
    assert pillars  # the example vault has pillars
    assert all(n["type"] == "pillar" for n in pillars)


def test_list_nodes_filters_by_auto_inject() -> None:
    auto = list_nodes(MEDDEV_VAULT, auto_inject_only=True)
    assert auto  # at least one pillar is auto_inject
    assert all(n.get("auto_inject") is True for n in auto)


def test_list_nodes_filters_by_source_kind() -> None:
    sources = list_nodes(
        MEDDEV_VAULT, type_name="source", source_kind="fda-510k-summary"
    )
    assert sources
    assert all(n.get("source_kind") == "fda-510k-summary" for n in sources)


def test_list_nodes_filters_compose() -> None:
    nodes = list_nodes(
        MEDDEV_VAULT, type_name="source", source_kind="customer-interview"
    )
    assert nodes
    assert all(n["type"] == "source" for n in nodes)
    assert all(n.get("source_kind") == "customer-interview" for n in nodes)


def test_list_nodes_emits_summary_fields() -> None:
    pillars = list_nodes(MEDDEV_VAULT, type_name="pillar")
    pillar = pillars[0]
    for required in ("id", "title", "type", "summary", "confidence", "verified_at", "path"):
        assert required in pillar, f"missing summary field: {required}"
    # The body should NOT be in the summary view.
    assert "body" not in pillar
    # Edges are surfaced as a structural list.
    assert isinstance(pillar.get("edges"), list)


def test_list_nodes_normalizes_dates_to_strings() -> None:
    pillars = list_nodes(MEDDEV_VAULT, type_name="pillar")
    pillar = pillars[0]
    assert isinstance(pillar["verified_at"], str)


def test_list_nodes_raises_on_missing_vault(tmp_path: Path) -> None:
    with pytest.raises(VaultNotFoundError):
        list_nodes(tmp_path / "does-not-exist")


def test_list_nodes_raises_when_no_profile_md(tmp_path: Path) -> None:
    # Empty directory — no _system/PROFILE.md.
    (tmp_path / "some-folder").mkdir()
    with pytest.raises(VaultNotFoundError):
        list_nodes(tmp_path)


# ---------------------------------------------------------------------------
# get_node
# ---------------------------------------------------------------------------


def test_get_node_returns_full_record() -> None:
    # Pick a pillar that we know exists in the example vault.
    node = get_node(MEDDEV_VAULT, "pillar-no-pediatric-use")
    assert node["id"] == "pillar-no-pediatric-use"
    assert node["type"] == "pillar"
    assert node["path"].endswith("pillar-no-pediatric-use.md")
    # Frontmatter is present minus the raw edges list.
    assert "summary" in node["frontmatter"]
    assert "edges" not in node["frontmatter"]
    # The body is preserved.
    assert node["body"]
    # Both directions of edges are returned.
    assert isinstance(node["edges_outbound"], list)
    assert isinstance(node["edges_inbound"], list)


def test_get_node_inbound_edges_reverse_outbound() -> None:
    # Find any source node that other nodes derive from.
    sources = list_nodes(MEDDEV_VAULT, type_name="source")
    assert sources
    # Pick a source that has derived_from edges pointing at it from other nodes.
    target_id = None
    for src in sources:
        node = get_node(MEDDEV_VAULT, src["id"])
        if any(e["type"] == "derived_from" for e in node["edges_inbound"]):
            target_id = src["id"]
            break
    assert target_id is not None, "expected at least one source with inbound derived_from"
    node = get_node(MEDDEV_VAULT, target_id)
    inbound = node["edges_inbound"]
    # Inbound edges are sorted deterministically.
    assert inbound == sorted(inbound, key=lambda e: (e["source"], e["type"]))


def test_get_node_raises_on_unknown_id() -> None:
    with pytest.raises(NodeNotFoundError):
        get_node(MEDDEV_VAULT, "pillar-does-not-exist")


def test_get_node_raises_on_missing_vault(tmp_path: Path) -> None:
    with pytest.raises(VaultNotFoundError):
        get_node(tmp_path / "does-not-exist", "any-id")
