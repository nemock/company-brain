"""Tests for the vault scaffold module.

These exercise scaffolding into a tmp_path and verify both the on-disk shape
and the content of the rendered _system files.

Most tests use ``init_git=False`` to keep them fast and free of git-config
side effects. A dedicated section below covers the git integration with
its own git-config fixture.
"""

from __future__ import annotations

import subprocess
from datetime import date
from pathlib import Path

import pytest

from company_brain.scaffold import (
    ProfileNotFoundError,
    VaultScaffoldResult,
    scaffold,
)


# ---------------------------------------------------------------------------
# Happy path: medical-device profile (git disabled for speed)
# ---------------------------------------------------------------------------


@pytest.fixture
def meddev_vault(tmp_path: Path) -> VaultScaffoldResult:
    return scaffold(
        tmp_path / "meddev-test",
        "medical-device",
        today=date(2026, 5, 21),
        init_git=False,
    )


def test_meddev_creates_vault_directory(meddev_vault: VaultScaffoldResult) -> None:
    assert meddev_vault.vault_path.exists()
    assert meddev_vault.vault_path.is_dir()


def test_meddev_creates_admin_folders(meddev_vault: VaultScaffoldResult) -> None:
    for folder in ("_system", "_attachments", "_branding", "exports"):
        assert (meddev_vault.vault_path / folder).is_dir(), folder


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


def test_meddev_writes_branding_files(meddev_vault: VaultScaffoldResult) -> None:
    branding = meddev_vault.vault_path / "_branding"
    assert (branding / "colors.yaml").is_file()
    assert (branding / "README.md").is_file()
    # colors.yaml has the documented keys.
    colors_text = (branding / "colors.yaml").read_text()
    for key in ("primary:", "secondary:", "text:", "font_family_headings:"):
        assert key in colors_text


def test_meddev_writes_vault_gitignore_and_readme(meddev_vault: VaultScaffoldResult) -> None:
    gitignore = (meddev_vault.vault_path / ".gitignore").read_text()
    assert "_system/INDEX.md" in gitignore
    assert "Obsidian" in gitignore

    readme = (meddev_vault.vault_path / "README.md").read_text()
    assert "company-brain" in readme
    assert "medical-device" in readme
    assert "controlled-document-boundary" in readme


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
    for field in ("clearance_number", "population", "intervention", "setting", "belongs_to_product"):
        assert f"`{field}`" in fm, field


def test_meddev_result_counts(meddev_vault: VaultScaffoldResult) -> None:
    # 5 admin folders (root, _system, _attachments, _branding, exports) +
    # 30 node-type folders = 35.
    assert meddev_vault.folder_count == 35
    # 5 _system + 2 _branding + .gitignore + README.md = 9.
    assert meddev_vault.file_count == 9
    assert meddev_vault.files_skipped == []


# ---------------------------------------------------------------------------
# Default profile: excludes medical-device folders
# ---------------------------------------------------------------------------


def test_default_profile_excludes_risk_folders(tmp_path: Path) -> None:
    result = scaffold(tmp_path / "default-vault", "default", init_git=False)
    assert not (result.vault_path / "risk").exists()
    assert not (result.vault_path / "entities" / "indications-for-use").exists()


def test_default_profile_includes_all_epistemic_and_entity_folders(tmp_path: Path) -> None:
    result = scaffold(tmp_path / "default-vault", "default", init_git=False)
    assert (result.vault_path / "pillars").is_dir()
    assert (result.vault_path / "entities" / "products").is_dir()
    assert (result.vault_path / "entities" / "competitors").is_dir()


def test_default_profile_md_says_no_activated_types(tmp_path: Path) -> None:
    result = scaffold(tmp_path / "default-vault", "default", init_git=False)
    profile_md = (result.vault_path / "_system" / "PROFILE.md").read_text()
    assert "no additional node types in v1" in profile_md
    assert "does not append the controlled-document-boundary footer" in profile_md


def test_default_profile_folder_count(tmp_path: Path) -> None:
    result = scaffold(tmp_path / "default-vault", "default", init_git=False)
    # 5 admin + 21 active node types (10 epistemic + 11 entity) = 26.
    assert result.folder_count == 26


def test_default_profile_writes_branding(tmp_path: Path) -> None:
    result = scaffold(tmp_path / "default-vault", "default", init_git=False)
    assert (result.vault_path / "_branding" / "colors.yaml").is_file()


# ---------------------------------------------------------------------------
# Idempotency and --force
# ---------------------------------------------------------------------------


def test_running_scaffold_twice_does_not_recreate_folders(tmp_path: Path) -> None:
    first = scaffold(tmp_path / "v", "medical-device", init_git=False)
    assert first.folder_count > 0
    second = scaffold(tmp_path / "v", "medical-device", init_git=False)
    assert second.folder_count == 0


def test_running_scaffold_twice_skips_files_without_force(tmp_path: Path) -> None:
    scaffold(tmp_path / "v", "medical-device", init_git=False)
    second = scaffold(tmp_path / "v", "medical-device", init_git=False)
    assert second.file_count == 0
    # 5 _system + 2 _branding + .gitignore + README.md
    assert len(second.files_skipped) == 9


def test_force_regenerates_files(tmp_path: Path) -> None:
    scaffold(tmp_path / "v", "medical-device", init_git=False)
    second = scaffold(tmp_path / "v", "medical-device", init_git=False, force=True)
    assert second.file_count == 9
    assert second.files_skipped == []


# ---------------------------------------------------------------------------
# Error paths
# ---------------------------------------------------------------------------


def test_unknown_profile_raises(tmp_path: Path) -> None:
    with pytest.raises(ProfileNotFoundError):
        scaffold(tmp_path / "v", "not-a-real-profile", init_git=False)


def test_path_that_is_a_file_raises(tmp_path: Path) -> None:
    file_path = tmp_path / "i-am-a-file"
    file_path.write_text("oops")
    with pytest.raises(NotADirectoryError):
        scaffold(file_path, "medical-device", init_git=False)


# ---------------------------------------------------------------------------
# Reserved profiles
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("profile_name", ["saas", "hardware", "services"])
def test_reserved_profiles_behave_like_default(tmp_path: Path, profile_name: str) -> None:
    result = scaffold(tmp_path / f"v-{profile_name}", profile_name, init_git=False)
    assert not (result.vault_path / "risk").exists()
    assert not (result.vault_path / "entities" / "indications-for-use").exists()
    assert (result.vault_path / "pillars").is_dir()


# ---------------------------------------------------------------------------
# Git integration
# ---------------------------------------------------------------------------


def _git_config_for_tests(repo: Path) -> None:
    """Set a minimum git identity locally so commit doesn't fail on CI."""

    subprocess.run(
        ["git", "config", "user.name", "company-brain test"],
        cwd=repo, check=True, capture_output=True, text=True,
    )
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=repo, check=True, capture_output=True, text=True,
    )


@pytest.fixture
def git_meddev_vault(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> VaultScaffoldResult:
    """Scaffold with git enabled, providing the user.name / user.email via env."""

    # GIT_AUTHOR_* / GIT_COMMITTER_* let `git commit` succeed without a global
    # git config, which CI runners may not have.
    monkeypatch.setenv("GIT_AUTHOR_NAME", "company-brain test")
    monkeypatch.setenv("GIT_AUTHOR_EMAIL", "test@example.com")
    monkeypatch.setenv("GIT_COMMITTER_NAME", "company-brain test")
    monkeypatch.setenv("GIT_COMMITTER_EMAIL", "test@example.com")

    return scaffold(
        tmp_path / "git-vault",
        "medical-device",
        today=date(2026, 5, 21),
        init_git=True,
    )


def test_git_default_initializes_repo(git_meddev_vault: VaultScaffoldResult) -> None:
    assert git_meddev_vault.git_initialized is True
    assert (git_meddev_vault.vault_path / ".git").is_dir()


def test_git_default_creates_initial_commit(git_meddev_vault: VaultScaffoldResult) -> None:
    assert git_meddev_vault.git_initial_commit is not None
    assert len(git_meddev_vault.git_initial_commit) == 40  # full sha


def test_git_default_branch_is_main(git_meddev_vault: VaultScaffoldResult) -> None:
    branch = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=git_meddev_vault.vault_path,
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    assert branch == "main"


def test_git_default_commit_excludes_index_md(git_meddev_vault: VaultScaffoldResult) -> None:
    """INDEX.md is in .gitignore, so it must not be in the initial commit."""

    tracked = subprocess.run(
        ["git", "ls-files"],
        cwd=git_meddev_vault.vault_path,
        capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    assert "_system/INDEX.md" not in tracked
    # But it does exist on disk (we wrote it).
    assert (git_meddev_vault.vault_path / "_system" / "INDEX.md").is_file()


def test_git_default_commit_includes_expected_files(git_meddev_vault: VaultScaffoldResult) -> None:
    tracked = subprocess.run(
        ["git", "ls-files"],
        cwd=git_meddev_vault.vault_path,
        capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    for expected in (
        ".gitignore",
        "README.md",
        "_system/PROFILE.md",
        "_system/NODE-TYPES.md",
        "_branding/colors.yaml",
        "_branding/README.md",
    ):
        assert expected in tracked, expected


def test_no_git_skips_git_steps(tmp_path: Path) -> None:
    result = scaffold(tmp_path / "v", "medical-device", init_git=False)
    assert result.git_initialized is False
    assert result.git_initial_commit is None
    assert not (result.vault_path / ".git").exists()


def test_git_inside_existing_repo_skipped(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """If vault_path is inside an existing git repo, do not nest a second repo."""

    monkeypatch.setenv("GIT_AUTHOR_NAME", "test")
    monkeypatch.setenv("GIT_AUTHOR_EMAIL", "test@example.com")
    monkeypatch.setenv("GIT_COMMITTER_NAME", "test")
    monkeypatch.setenv("GIT_COMMITTER_EMAIL", "test@example.com")

    # Initialize an outer repo.
    outer = tmp_path / "outer"
    outer.mkdir()
    subprocess.run(["git", "init", "-b", "main"], cwd=outer, check=True, capture_output=True)

    # Scaffold inside it.
    inner = outer / "inner-vault"
    result = scaffold(inner, "medical-device", init_git=True)

    assert result.git_initialized is False
    assert "inside an existing git working tree" in (result.git_skipped_reason or "")
    assert not (inner / ".git").exists()


def test_git_idempotent_second_run_does_not_double_commit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("GIT_AUTHOR_NAME", "test")
    monkeypatch.setenv("GIT_AUTHOR_EMAIL", "test@example.com")
    monkeypatch.setenv("GIT_COMMITTER_NAME", "test")
    monkeypatch.setenv("GIT_COMMITTER_EMAIL", "test@example.com")

    first = scaffold(tmp_path / "v", "medical-device", init_git=True)
    assert first.git_initial_commit is not None
    first_sha = first.git_initial_commit

    second = scaffold(tmp_path / "v", "medical-device", init_git=True)
    # Second run should not create another commit; HEAD stays at first_sha.
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=second.vault_path,
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    assert head == first_sha
