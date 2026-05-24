"""Tests for the install-skills CLI helper.

These exercise the symlink behavior using tmp_path so they're fast and
don't touch the user's real ~/.claude/skills/.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from company_brain.install_skills import (
    InstallResult,
    SkillSourceError,
    install_skills,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_source(root: Path, names: tuple[str, ...] = ("alpha", "beta", "gamma")) -> Path:
    """Build a fake company-brain source tree at `root` with the given skill names."""

    skills = root / "skills"
    skills.mkdir(parents=True)
    for name in names:
        skill = skills / name
        skill.mkdir()
        (skill / "SKILL.md").write_text(f"---\nname: {name}\n---\n# {name}\n")
    return root


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------


def test_installs_all_skills_to_empty_target(tmp_path: Path) -> None:
    source = _make_source(tmp_path / "repo")
    target = tmp_path / "claude-skills"

    result = install_skills(source, target)

    assert result.target_created is True
    assert len(result.installed) == 3
    assert result.conflicts == []
    for name in ("alpha", "beta", "gamma"):
        link = target / name
        assert link.is_symlink()
        assert link.resolve() == (source / "skills" / name).resolve()


def test_target_dir_already_exists_is_fine(tmp_path: Path) -> None:
    source = _make_source(tmp_path / "repo")
    target = tmp_path / "claude-skills"
    target.mkdir()

    result = install_skills(source, target)

    assert result.target_created is False
    assert len(result.installed) == 3


def test_result_object_categorizes_actions(tmp_path: Path) -> None:
    source = _make_source(tmp_path / "repo")
    target = tmp_path / "claude-skills"

    result = install_skills(source, target)

    assert isinstance(result, InstallResult)
    assert len(result.actions) == 3
    assert {a.status for a in result.actions} == {"installed"}


# ---------------------------------------------------------------------------
# Idempotency
# ---------------------------------------------------------------------------


def test_rerun_skips_already_correct_links(tmp_path: Path) -> None:
    source = _make_source(tmp_path / "repo")
    target = tmp_path / "claude-skills"

    install_skills(source, target)
    second = install_skills(source, target)

    assert len(second.installed) == 0
    assert len(second.skipped) == 3
    for action in second.skipped:
        assert action.detail == "already linked"


# ---------------------------------------------------------------------------
# Conflicts
# ---------------------------------------------------------------------------


def test_conflict_when_target_path_is_a_file(tmp_path: Path) -> None:
    source = _make_source(tmp_path / "repo")
    target = tmp_path / "claude-skills"
    target.mkdir()
    (target / "alpha").write_text("pre-existing")

    result = install_skills(source, target)

    assert (target / "alpha").read_text() == "pre-existing"
    conflicts = result.conflicts
    assert len(conflicts) == 1
    assert conflicts[0].name == "alpha"
    assert "non-symlink" in conflicts[0].detail


def test_conflict_when_existing_symlink_points_elsewhere(tmp_path: Path) -> None:
    source = _make_source(tmp_path / "repo")
    other = tmp_path / "other-skill"
    other.mkdir()
    (other / "SKILL.md").write_text("---\nname: alpha\n---\n")

    target = tmp_path / "claude-skills"
    target.mkdir()
    (target / "alpha").symlink_to(other)

    result = install_skills(source, target)

    assert (target / "alpha").resolve() == other.resolve()  # untouched
    assert len(result.conflicts) == 1
    assert "points to" in result.conflicts[0].detail


def test_force_replaces_existing_symlink(tmp_path: Path) -> None:
    source = _make_source(tmp_path / "repo")
    other = tmp_path / "other-skill"
    other.mkdir()
    (other / "SKILL.md").write_text("---\nname: alpha\n---\n")

    target = tmp_path / "claude-skills"
    target.mkdir()
    (target / "alpha").symlink_to(other)

    result = install_skills(source, target, force=True)

    assert (target / "alpha").resolve() == (source / "skills" / "alpha").resolve()
    assert len(result.installed) == 3  # alpha is "replaced", beta/gamma "installed"


def test_force_replaces_existing_file(tmp_path: Path) -> None:
    source = _make_source(tmp_path / "repo")
    target = tmp_path / "claude-skills"
    target.mkdir()
    (target / "alpha").write_text("pre-existing")

    result = install_skills(source, target, force=True)

    assert (target / "alpha").is_symlink()
    assert (target / "alpha").resolve() == (source / "skills" / "alpha").resolve()
    assert len(result.installed) == 3


# ---------------------------------------------------------------------------
# Dry-run
# ---------------------------------------------------------------------------


def test_dry_run_makes_no_changes(tmp_path: Path) -> None:
    source = _make_source(tmp_path / "repo")
    target = tmp_path / "claude-skills"

    result = install_skills(source, target, dry_run=True)

    assert not target.exists()
    assert result.target_created is True  # we report it would be created
    for action in result.actions:
        assert action.status == "planned"
        assert not (target / action.name).exists()


def test_dry_run_reports_conflicts_without_resolving(tmp_path: Path) -> None:
    source = _make_source(tmp_path / "repo")
    target = tmp_path / "claude-skills"
    target.mkdir()
    (target / "alpha").write_text("pre-existing")

    result = install_skills(source, target, dry_run=True)

    assert (target / "alpha").read_text() == "pre-existing"  # untouched
    # The alpha entry conflicts; beta and gamma would be created.
    assert len(result.conflicts) == 1
    assert len(result.planned) == 2


# ---------------------------------------------------------------------------
# Error paths
# ---------------------------------------------------------------------------


def test_missing_skills_directory_raises(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    with pytest.raises(SkillSourceError, match="no skills/ directory"):
        install_skills(repo, tmp_path / "target")


def test_empty_skills_directory_raises(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "skills").mkdir(parents=True)
    with pytest.raises(SkillSourceError, match="no skill directories"):
        install_skills(repo, tmp_path / "target")


def test_skill_without_SKILL_md_is_ignored(tmp_path: Path) -> None:
    """A directory with no SKILL.md isn't a skill — should be silently ignored."""

    source = _make_source(tmp_path / "repo")
    (source / "skills" / "not-a-skill").mkdir()  # no SKILL.md
    target = tmp_path / "claude-skills"

    result = install_skills(source, target)

    assert len(result.actions) == 3  # only the three valid skills
    assert {a.name for a in result.actions} == {"alpha", "beta", "gamma"}


# ---------------------------------------------------------------------------
# Real-world: the company-brain repo itself
# ---------------------------------------------------------------------------


def test_can_install_companys_own_seven_skills(tmp_path: Path) -> None:
    """Smoke test against the actual company-brain repo (the test runs inside it)."""

    # Find the repo root by walking up until we find a `skills/` directory
    # with `vault-architect/SKILL.md`.
    here = Path(__file__).resolve()
    candidates = [here.parent.parent, *here.parents]
    repo_root = next(
        (p for p in candidates if (p / "skills" / "vault-architect" / "SKILL.md").is_file()),
        None,
    )
    assert repo_root is not None, "couldn't locate company-brain repo root"

    target = tmp_path / "claude-skills"
    result = install_skills(repo_root, target)

    expected_skills = {
        "vault-architect", "intake", "atomize",
        "query", "doc-generate", "maintain", "visualize",
    }
    actual = {a.name for a in result.actions}
    assert expected_skills.issubset(actual), f"missing skills: {expected_skills - actual}"
    assert len(result.installed) == len(result.actions)
