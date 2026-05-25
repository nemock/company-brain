"""Tests for the 19 doc scaffolds (v0.4.0 step 2).

Strategy: one smoke test per scaffold to confirm it renders, contains
the scaffold footer flag, and is idempotent. Plus tests for profile
gating, the sales-battle-card competitor selection, and the scaffold
registry surface.

We don't test full content equivalence per scaffold — those are runnable
templates whose content will evolve when promoted to full implementation
in v1.x. The PRD bar for v0.4.0 is "produces a documented skeleton
flagged as scaffold."
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from company_brain.render import (
    SCAFFOLD_REGISTRY,
    ScaffoldProfileError,
    list_scaffold_names,
    render_scaffold,
)
from company_brain.scaffold import scaffold
from company_brain.vault import VaultNotFoundError


REPO_ROOT = Path(__file__).parent.parent
MEDDEV_VAULT = REPO_ROOT / "examples" / "meddev-fictional"


# Registered scaffold names per PRD §11. Tests below iterate over this so the
# moment we add or rename one, the failure surfaces here, not in CI.
EXPECTED_SCAFFOLDS = {
    "pid",
    "project-charter",
    "stakeholder-register",
    "risk-register",
    "status-report",
    "meeting-minutes",
    "lessons-learned",
    "business-plan",
    "sales-battle-card",
    "competitive-brief",
    "ifu-comparison",
    "decision-log",
    "press-release",
    "investor-update",
    "onboarding-doc",
    "srd",
    "srs",
    "hrs",
    "risk-brainstorm",
}

MEDDEV_ONLY = {"risk-register", "ifu-comparison", "risk-brainstorm"}


# ---------------------------------------------------------------------------
# Registry surface
# ---------------------------------------------------------------------------


def test_all_19_scaffolds_registered() -> None:
    registered = set(list_scaffold_names())
    assert registered == EXPECTED_SCAFFOLDS, (
        f"missing: {EXPECTED_SCAFFOLDS - registered}; "
        f"extra: {registered - EXPECTED_SCAFFOLDS}"
    )


def test_registry_marks_medical_device_scaffolds() -> None:
    for name in MEDDEV_ONLY:
        assert SCAFFOLD_REGISTRY[name].profile_required == "medical-device"
    for name in EXPECTED_SCAFFOLDS - MEDDEV_ONLY:
        assert SCAFFOLD_REGISTRY[name].profile_required is None


# ---------------------------------------------------------------------------
# Per-scaffold smoke tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("doc_name", sorted(EXPECTED_SCAFFOLDS))
def test_scaffold_renders_markdown(doc_name: str, tmp_path: Path) -> None:
    out = tmp_path / f"{doc_name}.md"
    result = render_scaffold(
        doc_name,
        MEDDEV_VAULT,
        output_path=out,
        generation_date=date(2026, 5, 25),
        write=True,
        output_format="markdown",
    )
    assert out.exists()
    content = result.content
    assert isinstance(content, str)
    # The scaffold footer flag MUST appear.
    assert "v0.4.0 scaffold" in content
    # The doc title is in the registry.
    assert SCAFFOLD_REGISTRY[doc_name].title in content


@pytest.mark.parametrize("doc_name", sorted(EXPECTED_SCAFFOLDS))
def test_scaffold_markdown_is_idempotent(doc_name: str, tmp_path: Path) -> None:
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    pinned = date(2026, 5, 25)
    render_scaffold(
        doc_name, MEDDEV_VAULT, output_path=a, generation_date=pinned
    )
    render_scaffold(
        doc_name, MEDDEV_VAULT, output_path=b, generation_date=pinned
    )
    assert a.read_bytes() == b.read_bytes()


@pytest.mark.parametrize("doc_name", sorted(EXPECTED_SCAFFOLDS))
def test_scaffold_renders_html(doc_name: str, tmp_path: Path) -> None:
    out = tmp_path / f"{doc_name}.html"
    result = render_scaffold(
        doc_name,
        MEDDEV_VAULT,
        output_path=out,
        generation_date=date(2026, 5, 25),
        write=True,
        output_format="html",
    )
    assert out.exists()
    assert "<!doctype html>" in str(result.content)


# ---------------------------------------------------------------------------
# Medical-device gating
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("doc_name", sorted(MEDDEV_ONLY))
def test_meddev_only_scaffolds_reject_default_profile(
    doc_name: str, tmp_path: Path
) -> None:
    scaffold(tmp_path / "v", "default", init_git=False)
    with pytest.raises(ScaffoldProfileError, match="medical-device"):
        render_scaffold(doc_name, tmp_path / "v", write=False)


def test_universal_scaffolds_work_on_default_profile(tmp_path: Path) -> None:
    """A scaffold without profile_required should render on a default-profile
    vault even when sections are sparse."""

    scaffold(tmp_path / "v", "default", init_git=False)
    out = tmp_path / "pid.md"
    render_scaffold(
        "pid", tmp_path / "v", output_path=out, generation_date=date(2026, 5, 25)
    )
    content = out.read_text()
    assert "Project Initiation Document" in content
    # Graceful degradation when inputs are empty.
    assert "No pillars captured" in content or "No product nodes" in content


# ---------------------------------------------------------------------------
# Sales battle card competitor selection
# ---------------------------------------------------------------------------


def test_battle_card_defaults_to_first_competitor(tmp_path: Path) -> None:
    result = render_scaffold(
        "sales-battle-card",
        MEDDEV_VAULT,
        output_path=tmp_path / "out.md",
        generation_date=date(2026, 5, 25),
    )
    # Filename should include the auto-selected competitor id. The example
    # vault's first competitor by id is `competitor-cardiotrace-inc`.
    assert result.output_path is not None
    assert result.output_path.name == "out.md"
    # And the content should cite the competitor.
    assert "competitor-cardiotrace-inc" in str(result.content)


def test_battle_card_honors_explicit_competitor(tmp_path: Path) -> None:
    result = render_scaffold(
        "sales-battle-card",
        MEDDEV_VAULT,
        output_path=tmp_path / "out.md",
        generation_date=date(2026, 5, 25),
        options={"competitor_id": "competitor-pulseguard-medical"},
    )
    assert "competitor-pulseguard-medical" in str(result.content)


def test_battle_card_unknown_competitor_raises(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="not found in vault"):
        render_scaffold(
            "sales-battle-card",
            MEDDEV_VAULT,
            output_path=tmp_path / "out.md",
            options={"competitor_id": "competitor-does-not-exist"},
        )


def test_battle_card_default_output_path_includes_competitor_id(
    tmp_path: Path,
) -> None:
    """When the caller doesn't supply output_path, the default filename
    embeds the competitor id so different competitors land in distinct files."""

    import shutil

    cloned = tmp_path / "vault"
    shutil.copytree(MEDDEV_VAULT, cloned)
    # Clear exports so we see what the renderer chose.
    exports = cloned / "exports"
    if exports.exists():
        shutil.rmtree(exports)
    result = render_scaffold(
        "sales-battle-card",
        cloned,
        generation_date=date(2026, 5, 25),
    )
    assert result.output_path is not None
    assert "competitor-cardiotrace-inc" in result.output_path.name


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


def test_unknown_scaffold_raises() -> None:
    with pytest.raises(ValueError, match="unknown scaffold"):
        render_scaffold("not-a-real-scaffold", MEDDEV_VAULT, write=False)


def test_unknown_format_raises() -> None:
    with pytest.raises(ValueError, match="scaffolds support"):
        render_scaffold(
            "pid", MEDDEV_VAULT, output_format="pdf", write=False
        )


def test_missing_vault_raises(tmp_path: Path) -> None:
    with pytest.raises(VaultNotFoundError):
        render_scaffold("pid", tmp_path / "does-not-exist", write=False)
