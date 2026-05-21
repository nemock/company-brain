"""Tests for the vault scaffold module.

These exercise scaffolding into a tmp_path and verify both the on-disk shape
and the content of the rendered _system files.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from company_brain.scaffold import (
    ProfileNotFoundError,
    VaultScaffoldResult,
    scaffold,
)


# ---------------------------------------------------------------------------
# Happy path: medical-device profile
# ---------------------------------------------------------------------------


@pytest.fixture
def meddev_vault(tmp_path: Path) -> VaultScaffoldResult:
    return scaffold(
        tmp_path / "meddev-test",
        "medical-device",
        today=date(2026, 5, 21),
    )


def test_meddev_creates_vault_directory(meddev_vault: VaultScaffoldResult) -> None:
    assert meddev_vault.vault_path.exists()
    assert meddev_vault.vault_path.is_dir()


def test_meddev_creates_admin_folders(meddev_vault: VaultScaffoldResult) -> None:
    for folder in ("_system", "_attachments", "exports"):
        assert (meddev_vault.vault_path / folder).is_dir()


def test_meddev_creates_epistemic_folders(meddev_vault: VaultScaffoldResult) -> None:
    for folder in (
        "pillars",
        "decisions",
        "playbooks",
        "patterns",
        "hypotheses",
        "facts",
        "concepts",
        "sources",
        "questions",
        "notes",
    ):
        assert (meddev_vault.vault_path / folder).is_dir(), folder


def test_meddev_creates_entity_folders(meddev_vault: VaultScaffoldResult) -> None:
    for folder in (
        "entities/products",
        "entities/product-lines",
        "entities/personas",
        "entities/customers",
        "entities/stakeholders",
        "entities/competitors",
        "entities/vendors",
        "entities/requirements",
        "entities/features",
        "entities/use-cases",
        "entities/metrics",
        "entities/indications-for-use",
    ):
        assert (meddev_vault.vault_path / folder).is_dir(), folder


def test_meddev_creates_risk_folders(meddev_vault: VaultScaffoldResult) -> None:
    for folder in (
        "risk/risk-insights",
        "risk/hazards",
        "risk/hazardous-situations",
        "risk/harms",
        "risk/risk-control-ideas",
        "risk/regulations",
        "risk/standards",
        "risk/regulatory-clearances",
    ):
        assert (meddev_vault.vault_path / folder).is_dir(), folder


def test_meddev_writes_all_system_files(meddev_vault: VaultScaffoldResult) -> None:
    expected = {
        "PROFILE.md",
        "INDEX.md",
        "NODE-TYPES.md",
        "EDGE-TYPES.md",
        "FRONTMATTER-SCHEMA.md",
    }
    actual = {p.name for p in (meddev_vault.vault_path / "_system").iterdir()}
    assert actual == expected


def test_meddev_profile_md_has_expected_frontmatter(meddev_vault: VaultScaffoldResult) -> None:
    profile_md = (meddev_vault.vault_path / "_system" / "PROFILE.md").read_text()
    assert "profile: medical-device" in profile_md
    assert "scaffolded_at: 2026-05-21" in profile_md
    assert "controlled_document: false" in profile_md


def test_meddev_profile_md_lists_activated_types(meddev_vault: VaultScaffoldResult) -> None:
    profile_md = (meddev_vault.vault_path / "_system" / "PROFILE.md").read_text()
    for node_type in (
        "indication-for-use",
        "regulatory-clearance",
        "hazard",
        "hazardous-situation",
        "harm",
        "risk-control-idea",
        "risk-insight",
        "regulation",
        "standard",
    ):
        assert f"`{node_type}`" in profile_md, node_type


def test_meddev_profile_md_mentions_controlled_document_footer(meddev_vault: VaultScaffoldResult) -> None:
    profile_md = (meddev_vault.vault_path / "_system" / "PROFILE.md").read_text()
    assert "controlled-document-boundary footer" in profile_md


def test_meddev_node_types_md_includes_meddev_types(meddev_vault: VaultScaffoldResult) -> None:
    node_types_md = (meddev_vault.vault_path / "_system" / "NODE-TYPES.md").read_text()
    assert "## Profile-conditional" in node_types_md
    assert "`indication-for-use`" in node_types_md
    assert "`regulatory-clearance`" in node_types_md


def test_meddev_edge_types_md_includes_inverse_pair(meddev_vault: VaultScaffoldResult) -> None:
    edge_md = (meddev_vault.vault_path / "_system" / "EDGE-TYPES.md").read_text()
    assert "`preceded_by`" in edge_md
    assert "`followed_by`" in edge_md


def test_meddev_frontmatter_schema_md_includes_base_fields(meddev_vault: VaultScaffoldResult) -> None:
    fm = (meddev_vault.vault_path / "_system" / "FRONTMATTER-SCHEMA.md").read_text()
    for field in ("id", "title", "type", "summary", "controlled_document"):
        assert f"`{field}`" in fm, field


def test_meddev_frontmatter_schema_md_includes_extra_fields(meddev_vault: VaultScaffoldResult) -> None:
    fm = (meddev_vault.vault_path / "_system" / "FRONTMATTER-SCHEMA.md").read_text()
    # Per-type extras section should mention the medical-device-specific fields.
    for field in ("clearance_number", "population", "intervention", "setting", "belongs_to_product"):
        assert f"`{field}`" in fm, field


def test_meddev_result_counts(meddev_vault: VaultScaffoldResult) -> None:
    # 4 admin folders (root, _system, _attachments, exports) + 30 node-type folders.
    assert meddev_vault.folder_count == 34
    assert meddev_vault.file_count == 5
    assert meddev_vault.files_skipped == []


# ---------------------------------------------------------------------------
# Default profile: excludes medical-device folders
# ---------------------------------------------------------------------------


def test_default_profile_excludes_risk_folders(tmp_path: Path) -> None:
    result = scaffold(tmp_path / "default-vault", "default")
    assert not (result.vault_path / "risk").exists()
    assert not (result.vault_path / "entities" / "indications-for-use").exists()


def test_default_profile_includes_all_epistemic_and_entity_folders(tmp_path: Path) -> None:
    result = scaffold(tmp_path / "default-vault", "default")
    assert (result.vault_path / "pillars").is_dir()
    assert (result.vault_path / "entities" / "products").is_dir()
    assert (result.vault_path / "entities" / "competitors").is_dir()


def test_default_profile_md_says_no_activated_types(tmp_path: Path) -> None:
    result = scaffold(tmp_path / "default-vault", "default")
    profile_md = (result.vault_path / "_system" / "PROFILE.md").read_text()
    assert "no additional node types in v1" in profile_md
    assert "does not append the controlled-document-boundary footer" in profile_md


def test_default_profile_folder_count(tmp_path: Path) -> None:
    result = scaffold(tmp_path / "default-vault", "default")
    # 4 admin + 21 active node types (10 epistemic + 11 entity).
    assert result.folder_count == 25


# ---------------------------------------------------------------------------
# Idempotency and --force
# ---------------------------------------------------------------------------


def test_running_scaffold_twice_does_not_recreate_folders(tmp_path: Path) -> None:
    first = scaffold(tmp_path / "v", "medical-device")
    assert first.folder_count > 0
    second = scaffold(tmp_path / "v", "medical-device")
    # Second run sees all folders already there.
    assert second.folder_count == 0


def test_running_scaffold_twice_skips_system_files_without_force(tmp_path: Path) -> None:
    scaffold(tmp_path / "v", "medical-device")
    second = scaffold(tmp_path / "v", "medical-device")
    assert second.file_count == 0
    assert len(second.files_skipped) == 5  # all five _system files


def test_force_regenerates_system_files(tmp_path: Path) -> None:
    scaffold(tmp_path / "v", "medical-device")
    second = scaffold(tmp_path / "v", "medical-device", force=True)
    assert second.file_count == 5
    assert second.files_skipped == []


# ---------------------------------------------------------------------------
# Error paths
# ---------------------------------------------------------------------------


def test_unknown_profile_raises(tmp_path: Path) -> None:
    with pytest.raises(ProfileNotFoundError):
        scaffold(tmp_path / "v", "not-a-real-profile")


def test_path_that_is_a_file_raises(tmp_path: Path) -> None:
    file_path = tmp_path / "i-am-a-file"
    file_path.write_text("oops")
    with pytest.raises(NotADirectoryError):
        scaffold(file_path, "medical-device")


# ---------------------------------------------------------------------------
# Reserved profiles
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("profile_name", ["saas", "hardware", "services"])
def test_reserved_profiles_behave_like_default(tmp_path: Path, profile_name: str) -> None:
    result = scaffold(tmp_path / f"v-{profile_name}", profile_name)
    # Reserved profiles activate no extra node types, so they look like default.
    assert not (result.vault_path / "risk").exists()
    assert not (result.vault_path / "entities" / "indications-for-use").exists()
    assert (result.vault_path / "pillars").is_dir()
