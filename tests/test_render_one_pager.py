"""Tests for the one-pager generator (v0.3.0 sub-piece 3)."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from company_brain.render import render_one_pager
from company_brain.scaffold import scaffold
from company_brain.vault import VaultNotFoundError


REPO_ROOT = Path(__file__).parent.parent
MEDDEV_VAULT = REPO_ROOT / "examples" / "meddev-fictional"


def test_render_one_pager_is_byte_identical_on_repeat(tmp_path: Path) -> None:
    pinned = date(2026, 5, 24)
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    render_one_pager(MEDDEV_VAULT, output_path=a, generation_date=pinned)
    render_one_pager(MEDDEV_VAULT, output_path=b, generation_date=pinned)
    assert a.read_bytes() == b.read_bytes()


def test_render_one_pager_differs_only_in_date_line(tmp_path: Path) -> None:
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    render_one_pager(MEDDEV_VAULT, output_path=a, generation_date=date(2026, 5, 24))
    render_one_pager(MEDDEV_VAULT, output_path=b, generation_date=date(2026, 6, 1))
    la, lb = a.read_text().splitlines(), b.read_text().splitlines()
    diff = [i for i, (x, y) in enumerate(zip(la, lb)) if x != y]
    assert len(diff) == 1
    assert "one-pager generated" in la[diff[0]]


def test_render_one_pager_includes_primary_product_and_pillar(tmp_path: Path) -> None:
    out = tmp_path / "op.md"
    render_one_pager(MEDDEV_VAULT, output_path=out, generation_date=date(2026, 5, 24))
    content = out.read_text()
    # Primary product is the first product by id (vitalisens-cardio).
    assert content.startswith("# Vitalisens Cardio")
    # The highest-confidence positive pillar's summary appears as the tagline.
    # In the example vault that's ICP (confidence 0.9, sorted before disposable-pad at 0.85).
    assert "ambulatory" in content.lower()


def test_render_one_pager_cites_persona_and_interview(tmp_path: Path) -> None:
    out = tmp_path / "op.md"
    render_one_pager(MEDDEV_VAULT, output_path=out, generation_date=date(2026, 5, 24))
    content = out.read_text()
    assert "[persona-ambulatory-cardiac-patient]" in content
    assert "[source-customer-interview-2026-04-12-nurse-anderson]" in content


def test_render_one_pager_meddev_appends_controlled_document_footer(tmp_path: Path) -> None:
    out = tmp_path / "op.md"
    render_one_pager(MEDDEV_VAULT, output_path=out, generation_date=date(2026, 5, 24))
    content = out.read_text()
    assert "This is a planning artifact" in content


def test_render_one_pager_default_profile_omits_controlled_footer(tmp_path: Path) -> None:
    scaffold(tmp_path / "vault", "default", init_git=False)
    out = tmp_path / "op.md"
    render_one_pager(tmp_path / "vault", output_path=out, generation_date=date(2026, 5, 24))
    content = out.read_text()
    assert "This is a planning artifact" not in content
    # Empty-vault graceful degradation: each section explains how to populate it.
    assert "Run `intake" in content


def test_render_one_pager_writes_to_default_exports_path(tmp_path: Path) -> None:
    import shutil

    cloned = tmp_path / "vault"
    shutil.copytree(MEDDEV_VAULT, cloned)
    exports = cloned / "exports"
    if exports.exists():
        shutil.rmtree(exports)
    result = render_one_pager(cloned, generation_date=date(2026, 5, 24))
    assert result.output_path == cloned / "exports" / "one-pager.md"
    assert (cloned / "exports" / "one-pager.md").is_file()


def test_render_one_pager_raises_on_missing_vault(tmp_path: Path) -> None:
    with pytest.raises(VaultNotFoundError):
        render_one_pager(tmp_path / "does-not-exist")


def test_render_one_pager_is_short(tmp_path: Path) -> None:
    """A one-pager should fit on a page — assert against a generous upper bound.

    Roughly: a printed page holds ~3000 chars of body text. Our generated
    one-pager + footers + citations should stay comfortably below 4000.
    """

    out = tmp_path / "op.md"
    render_one_pager(MEDDEV_VAULT, output_path=out, generation_date=date(2026, 5, 24))
    content = out.read_text()
    assert len(content) < 4000, f"one-pager grew to {len(content)} chars; tighten the template"
