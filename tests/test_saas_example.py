"""Tests for the saas-fictional example vault (v0.5.0 step 1).

These tests assert that the second example vault stays in a renderable,
validatable, profile-correct state — so a regression in default-profile
rendering or schema validation fails CI loudly.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from company_brain.render import (
    ScaffoldProfileError,
    list_scaffold_names,
    render_mrd,
    render_one_pager,
    render_scaffold,
)
from company_brain.validator import validate
from company_brain.viewer import ViewerProfileError, render_viewer


REPO_ROOT = Path(__file__).parent.parent
SAAS_VAULT = REPO_ROOT / "examples" / "saas-fictional"


def test_saas_vault_exists_and_uses_default_profile() -> None:
    assert (SAAS_VAULT / "_system" / "PROFILE.md").is_file()
    text = (SAAS_VAULT / "_system" / "PROFILE.md").read_text()
    assert "profile: default" in text


def test_saas_vault_validates_clean() -> None:
    issues = validate(SAAS_VAULT)
    errors = [i for i in issues if i.severity == "error"]
    assert errors == [], f"expected zero errors, got: {errors}"


def test_saas_mrd_renders_without_medical_device_sections(tmp_path: Path) -> None:
    out = tmp_path / "mrd.md"
    render_mrd(SAAS_VAULT, output_path=out, generation_date=date(2026, 5, 25))
    content = out.read_text()
    assert "## 1. Executive summary" in content
    # Default profile MRD has no §3 IFU section.
    assert "Indications for use" not in content
    # Default profile MRD has no §7 Regulatory landscape section.
    assert "Regulatory landscape" not in content
    # Section numbers shift to fill the gap.
    assert "## 3. Market and personas" in content  # (would be 4 in meddev)
    # No controlled-document footer on the default profile.
    assert "This is a planning artifact" not in content


def test_saas_one_pager_renders(tmp_path: Path) -> None:
    out = tmp_path / "one-pager.md"
    render_one_pager(SAAS_VAULT, output_path=out, generation_date=date(2026, 5, 25))
    content = out.read_text()
    assert "Loftwing" in content


@pytest.mark.parametrize(
    "doc_name",
    sorted(set(list_scaffold_names()) - {"risk-register", "ifu-comparison", "risk-brainstorm"}),
)
def test_saas_renders_every_non_meddev_scaffold(doc_name: str, tmp_path: Path) -> None:
    out = tmp_path / f"{doc_name}.md"
    render_scaffold(
        doc_name,
        SAAS_VAULT,
        output_path=out,
        generation_date=date(2026, 5, 25),
    )
    assert out.exists()
    content = out.read_text()
    assert "v0.4.0 scaffold" in content


@pytest.mark.parametrize("doc_name", ("risk-register", "ifu-comparison", "risk-brainstorm"))
def test_saas_rejects_medical_device_only_scaffolds(doc_name: str, tmp_path: Path) -> None:
    with pytest.raises(ScaffoldProfileError, match="medical-device"):
        render_scaffold(doc_name, SAAS_VAULT, write=False)


def test_saas_viewer_renders_graph_mode(tmp_path: Path) -> None:
    out = tmp_path / "graph.html"
    result = render_viewer(
        SAAS_VAULT, output_path=out, generation_date=date(2026, 5, 25)
    )
    assert out.exists()
    # The saas vault has ~25-40 nodes; assert non-trivial.
    assert result.node_count >= 20


def test_saas_viewer_rejects_ifu_chain_mode(tmp_path: Path) -> None:
    with pytest.raises(ViewerProfileError, match="medical-device"):
        render_viewer(SAAS_VAULT, mode="ifu-chain", write=False)


def test_saas_vault_does_not_have_medical_device_folders() -> None:
    """The default profile excludes risk/* and entities/indications-for-use."""

    assert not (SAAS_VAULT / "risk").exists()
    assert not (SAAS_VAULT / "entities" / "indications-for-use").exists()
