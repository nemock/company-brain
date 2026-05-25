"""Tests for the viewer (v0.4.0 step 3)."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

import pytest

from company_brain.scaffold import scaffold
from company_brain.viewer import (
    VIEW_MODES,
    ViewerProfileError,
    render_viewer,
)
from company_brain.vault import VaultNotFoundError


REPO_ROOT = Path(__file__).parent.parent
MEDDEV_VAULT = REPO_ROOT / "examples" / "meddev-fictional"


def _extract_graph_json(html: str) -> dict:
    """Pull the JSON island the template embeds and parse it."""

    match = re.search(
        r'<script id="graph-data" type="application/json">(.*?)</script>',
        html,
        flags=re.DOTALL,
    )
    assert match is not None, "graph-data script island missing"
    return json.loads(match.group(1))


# ---------------------------------------------------------------------------
# Modes
# ---------------------------------------------------------------------------


def test_default_mode_includes_every_node_and_resolved_link(tmp_path: Path) -> None:
    out = tmp_path / "graph.html"
    result = render_viewer(
        MEDDEV_VAULT, output_path=out, generation_date=date(2026, 5, 25)
    )
    assert result.mode == "graph"
    assert out.exists()
    graph = _extract_graph_json(out.read_text())
    # The meddev-fictional vault has 58 valid nodes after maintain repaired
    # the inverse-edge gaps; allow some slack so the test doesn't break on
    # new fixtures.
    assert len(graph["nodes"]) >= 50
    assert len(graph["links"]) > 0
    # Every link's source and target resolve to a known node id.
    node_ids = {n["id"] for n in graph["nodes"]}
    for link in graph["links"]:
        assert link["source"] in node_ids
        assert link["target"] in node_ids


def test_ifu_chain_mode_only_emits_ifu_nodes(tmp_path: Path) -> None:
    out = tmp_path / "ifu.html"
    result = render_viewer(
        MEDDEV_VAULT,
        output_path=out,
        mode="ifu-chain",
        generation_date=date(2026, 5, 25),
    )
    graph = _extract_graph_json(out.read_text())
    assert {n["type"] for n in graph["nodes"]} == {"indication-for-use"}
    # Every link is preceded_by or followed_by.
    assert all(e["type"] in {"preceded_by", "followed_by"} for e in graph["links"])
    assert result.node_count == len(graph["nodes"])


def test_predicate_tree_mode_only_emits_clearances(tmp_path: Path) -> None:
    out = tmp_path / "pred.html"
    result = render_viewer(
        MEDDEV_VAULT,
        output_path=out,
        mode="predicate-tree",
        generation_date=date(2026, 5, 25),
    )
    graph = _extract_graph_json(out.read_text())
    assert {n["type"] for n in graph["nodes"]} == {"regulatory-clearance"}
    assert all(e["type"] == "preceded_by" for e in graph["links"])
    assert result.node_count == len(graph["nodes"])


# ---------------------------------------------------------------------------
# Profile gating
# ---------------------------------------------------------------------------


def test_ifu_chain_rejects_default_profile(tmp_path: Path) -> None:
    scaffold(tmp_path / "v", "default", init_git=False)
    with pytest.raises(ViewerProfileError, match="medical-device"):
        render_viewer(tmp_path / "v", mode="ifu-chain", write=False)


def test_predicate_tree_rejects_default_profile(tmp_path: Path) -> None:
    scaffold(tmp_path / "v", "default", init_git=False)
    with pytest.raises(ViewerProfileError, match="medical-device"):
        render_viewer(tmp_path / "v", mode="predicate-tree", write=False)


def test_default_mode_works_on_default_profile(tmp_path: Path) -> None:
    scaffold(tmp_path / "v", "default", init_git=False)
    result = render_viewer(
        tmp_path / "v",
        output_path=tmp_path / "out.html",
        generation_date=date(2026, 5, 25),
    )
    assert result.mode == "graph"
    assert result.node_count == 0  # empty vault


# ---------------------------------------------------------------------------
# Idempotency
# ---------------------------------------------------------------------------


def test_viewer_is_byte_identical_on_repeat(tmp_path: Path) -> None:
    a = tmp_path / "a.html"
    b = tmp_path / "b.html"
    pinned = date(2026, 5, 25)
    render_viewer(MEDDEV_VAULT, output_path=a, generation_date=pinned)
    render_viewer(MEDDEV_VAULT, output_path=b, generation_date=pinned)
    assert a.read_bytes() == b.read_bytes()


def test_viewer_default_output_path(tmp_path: Path) -> None:
    import shutil

    cloned = tmp_path / "vault"
    shutil.copytree(MEDDEV_VAULT, cloned)
    # Clean any prior viewer file.
    leftover = cloned / "vault-graph.html"
    if leftover.exists():
        leftover.unlink()
    result = render_viewer(cloned, generation_date=date(2026, 5, 25))
    assert result.output_path == cloned / "vault-graph.html"
    assert (cloned / "vault-graph.html").is_file()


# ---------------------------------------------------------------------------
# Branding integration
# ---------------------------------------------------------------------------


def test_viewer_picks_up_branding_colors(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    scaffold(vault, "default", init_git=False)
    (vault / "_branding" / "colors.yaml").write_text(
        "primary: \"#ff0066\"\nsecondary: \"#003366\"\n",
        encoding="utf-8",
    )
    out = tmp_path / "out.html"
    render_viewer(vault, output_path=out, generation_date=date(2026, 5, 25))
    html = out.read_text()
    assert "--cb-primary: #ff0066" in html
    assert "--cb-secondary: #003366" in html


def test_viewer_template_override_takes_precedence(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    scaffold(vault, "default", init_git=False)
    overrides = vault / "_branding" / "templates"
    overrides.mkdir(parents=True, exist_ok=True)
    (overrides / "viewer.html.j2").write_text(
        "<html><body>CUSTOM VIEWER for {{ meta.profile }}</body></html>",
        encoding="utf-8",
    )
    out = tmp_path / "out.html"
    render_viewer(vault, output_path=out, generation_date=date(2026, 5, 25))
    assert "CUSTOM VIEWER for default" in out.read_text()


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


def test_unknown_mode_raises() -> None:
    with pytest.raises(ValueError, match="unknown viewer mode"):
        render_viewer(MEDDEV_VAULT, mode="3d-quaternion", write=False)


def test_missing_vault_raises(tmp_path: Path) -> None:
    with pytest.raises(VaultNotFoundError):
        render_viewer(tmp_path / "does-not-exist", write=False)


def test_view_modes_constant_matches_implementation() -> None:
    assert set(VIEW_MODES) == {"graph", "ifu-chain", "predicate-tree"}
