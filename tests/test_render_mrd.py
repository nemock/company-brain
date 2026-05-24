"""Tests for the MRD generator (v0.3.0 sub-piece 2)."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from company_brain.render import render_mrd
from company_brain.render.engine import load_branding
from company_brain.scaffold import scaffold
from company_brain.vault import VaultNotFoundError


REPO_ROOT = Path(__file__).parent.parent
MEDDEV_VAULT = REPO_ROOT / "examples" / "meddev-fictional"


# ---------------------------------------------------------------------------
# Idempotency
# ---------------------------------------------------------------------------


def test_render_mrd_is_byte_identical_on_repeat(tmp_path: Path) -> None:
    """Re-rendering with the same generation_date must produce identical bytes."""

    out1 = tmp_path / "MRD-1.md"
    out2 = tmp_path / "MRD-2.md"
    pinned = date(2026, 5, 24)
    render_mrd(MEDDEV_VAULT, output_path=out1, generation_date=pinned, write=True)
    render_mrd(MEDDEV_VAULT, output_path=out2, generation_date=pinned, write=True)
    assert out1.read_bytes() == out2.read_bytes()


def test_render_mrd_differs_only_in_date_line_across_dates(tmp_path: Path) -> None:
    """Rendering on two different dates differs only in the footer line."""

    out1 = tmp_path / "MRD-day1.md"
    out2 = tmp_path / "MRD-day2.md"
    render_mrd(MEDDEV_VAULT, output_path=out1, generation_date=date(2026, 5, 24))
    render_mrd(MEDDEV_VAULT, output_path=out2, generation_date=date(2026, 6, 1))
    lines1 = out1.read_text().splitlines()
    lines2 = out2.read_text().splitlines()
    diff_indexes = [i for i, (a, b) in enumerate(zip(lines1, lines2)) if a != b]
    assert len(diff_indexes) == 1, f"expected exactly one differing line, got {diff_indexes}"
    diff_line = lines1[diff_indexes[0]]
    assert "MRD generated" in diff_line


# ---------------------------------------------------------------------------
# Medical-device profile content
# ---------------------------------------------------------------------------


def test_render_mrd_meddev_includes_ifu_section(tmp_path: Path) -> None:
    out = tmp_path / "MRD.md"
    render_mrd(MEDDEV_VAULT, output_path=out, generation_date=date(2026, 5, 24))
    content = out.read_text()
    assert "## 3. Indications for use" in content
    assert "IFU comparison matrix" in content


def test_render_mrd_meddev_includes_regulatory_landscape(tmp_path: Path) -> None:
    out = tmp_path / "MRD.md"
    render_mrd(MEDDEV_VAULT, output_path=out, generation_date=date(2026, 5, 24))
    content = out.read_text()
    assert "## 7. Regulatory landscape" in content
    assert "K231234" in content


def test_render_mrd_meddev_appends_controlled_document_footer(tmp_path: Path) -> None:
    out = tmp_path / "MRD.md"
    render_mrd(MEDDEV_VAULT, output_path=out, generation_date=date(2026, 5, 24))
    content = out.read_text()
    assert "This is a planning artifact" in content
    assert "ISO 14971" in content


def test_render_mrd_meddev_non_goal_pillars_in_section_10(tmp_path: Path) -> None:
    out = tmp_path / "MRD.md"
    render_mrd(MEDDEV_VAULT, output_path=out, generation_date=date(2026, 5, 24))
    content = out.read_text()
    # Section header
    assert "## 10. What we are explicitly not doing" in content
    # Both non-goal pillars (tagged with non-goal) should appear in this section.
    section_start = content.index("## 10.")
    section = content[section_start:]
    assert "pillar-no-pediatric-use" in section
    assert "pillar-no-physical-documentation" in section


def test_render_mrd_meddev_decisions_with_rules_out_in_section_10(tmp_path: Path) -> None:
    out = tmp_path / "MRD.md"
    render_mrd(MEDDEV_VAULT, output_path=out, generation_date=date(2026, 5, 24))
    content = out.read_text()
    section_start = content.index("## 10.")
    section = content[section_start:]
    # Each of the example decisions has a `## What This Rules Out` section.
    assert "decision-001-online-only-documentation" in section
    assert "decision-002-prescription-only-not-otc" in section
    assert "decision-003-7-day-wear-not-14-day" in section


def test_render_mrd_meddev_evidence_vs_vision_split(tmp_path: Path) -> None:
    out = tmp_path / "MRD.md"
    render_mrd(MEDDEV_VAULT, output_path=out, generation_date=date(2026, 5, 24))
    content = out.read_text()
    section = content[content.index("## 8. Evidence vs. vision split"):]
    # All three counts present.
    assert "Evidence-derived claims:" in section
    assert "Vision-derived claims:" in section
    assert "Uncited claims:" in section


def test_render_mrd_meddev_source_bibliography(tmp_path: Path) -> None:
    out = tmp_path / "MRD.md"
    render_mrd(MEDDEV_VAULT, output_path=out, generation_date=date(2026, 5, 24))
    content = out.read_text()
    section = content[content.index("## 11. Sources"):]
    # The bibliography table header.
    assert "| Source | Kind | Title |" in section
    # Every source_kind that appears in the example vault is labeled.
    assert "founder-vision" in section
    assert "fda-510k-summary" in section
    assert "customer-interview" in section


def test_render_mrd_writes_to_default_exports_path(tmp_path: Path) -> None:
    """Cloning the example vault and rendering without --out lands at exports/MRD.md."""

    import shutil

    cloned = tmp_path / "vault"
    shutil.copytree(MEDDEV_VAULT, cloned)
    # Clear any existing exports.
    exports = cloned / "exports"
    if exports.exists():
        shutil.rmtree(exports)

    result = render_mrd(cloned, generation_date=date(2026, 5, 24))
    assert result.output_path == cloned / "exports" / "MRD.md"
    assert (cloned / "exports" / "MRD.md").is_file()


# ---------------------------------------------------------------------------
# Profile-aware section omission
# ---------------------------------------------------------------------------


def test_render_mrd_default_profile_omits_meddev_sections(tmp_path: Path) -> None:
    """A `default` profile vault has no IFU or Regulatory Landscape sections."""

    scaffold(tmp_path / "vault", "default", init_git=False)
    out = tmp_path / "MRD.md"
    render_mrd(tmp_path / "vault", output_path=out, generation_date=date(2026, 5, 24))
    content = out.read_text()
    # Profile-conditional sections should be omitted entirely.
    assert "Indications for use" not in content
    assert "Regulatory landscape" not in content
    # And the controlled-document footer should not appear.
    assert "This is a planning artifact" not in content
    # Section numbering should skip the meddev sections.
    assert "## 1. Executive summary" in content
    assert "## 3. Market and personas" in content  # (would be 4 in meddev)
    assert "## 6. Evidence vs. vision split" in content  # (would be 8 in meddev)


def test_render_mrd_default_profile_does_not_render_ifu_table(tmp_path: Path) -> None:
    scaffold(tmp_path / "vault", "default", init_git=False)
    out = tmp_path / "MRD.md"
    render_mrd(tmp_path / "vault", output_path=out, generation_date=date(2026, 5, 24))
    content = out.read_text()
    assert "IFU comparison matrix" not in content


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


def test_render_mrd_raises_on_missing_vault(tmp_path: Path) -> None:
    with pytest.raises(VaultNotFoundError):
        render_mrd(tmp_path / "does-not-exist")


# ---------------------------------------------------------------------------
# Branding
# ---------------------------------------------------------------------------


def test_load_branding_picks_up_vault_colors_yaml() -> None:
    branding = load_branding(MEDDEV_VAULT)
    # The example vault sets a clinical-blue primary.
    assert branding.primary == "#1f3a5f"
    # No logo file is shipped in the example vault.
    assert branding.logo_path is None


def test_load_branding_defaults_when_no_branding_folder(tmp_path: Path) -> None:
    branding = load_branding(tmp_path)
    # Falls back to the default palette.
    assert branding.primary == "#1f3a5f"
    assert branding.logo_path is None


def test_template_override_takes_precedence(tmp_path: Path) -> None:
    """Placing mrd.md.j2 under _branding/templates/ overrides the bundled template."""

    scaffold(tmp_path / "vault", "default", init_git=False)
    overrides = tmp_path / "vault" / "_branding" / "templates"
    overrides.mkdir(parents=True, exist_ok=True)
    (overrides / "mrd.md.j2").write_text(
        "# OVERRIDDEN TEMPLATE\n\nGenerated: {{ meta.generation_date }}\n",
        encoding="utf-8",
    )
    out = tmp_path / "MRD.md"
    render_mrd(tmp_path / "vault", output_path=out, generation_date=date(2026, 5, 24))
    content = out.read_text()
    assert content.startswith("# OVERRIDDEN TEMPLATE")
    assert "Generated: 2026-05-24" in content
