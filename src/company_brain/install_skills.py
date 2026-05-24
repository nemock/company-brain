"""Install the company-brain Claude Code skills.

Symlinks each subdirectory of ``<source>/skills/`` into ``<target>/`` so
Claude Code can find them. Idempotent: re-running with the same source and
target leaves correctly-symlinked entries alone and reports them as
``skipped``.

Source defaults to the current working directory (assumes you're running
from the company-brain repo). Pass ``source=...`` to point elsewhere.

Target defaults to ``~/.claude/skills/``, which is where Claude Code
discovers globally-installed skills.

Used by the ``cb install-skills`` CLI command.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class SkillSourceError(ValueError):
    """Raised when the source directory does not contain installable skills."""


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------


@dataclass
class SkillAction:
    """One per skill: what happened (or would happen)."""

    name: str
    source: Path
    target: Path
    status: str  # "installed" | "skipped" | "conflict" | "replaced" | "planned"
    detail: str = ""


@dataclass
class InstallResult:
    """Aggregate result of an install_skills() run."""

    source: Path
    target: Path
    target_created: bool = False
    actions: list[SkillAction] = field(default_factory=list)
    dry_run: bool = False

    @property
    def installed(self) -> list[SkillAction]:
        return [a for a in self.actions if a.status in {"installed", "replaced"}]

    @property
    def skipped(self) -> list[SkillAction]:
        return [a for a in self.actions if a.status == "skipped"]

    @property
    def conflicts(self) -> list[SkillAction]:
        return [a for a in self.actions if a.status == "conflict"]

    @property
    def planned(self) -> list[SkillAction]:
        return [a for a in self.actions if a.status == "planned"]


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def install_skills(
    source: Path,
    target: Path,
    *,
    force: bool = False,
    dry_run: bool = False,
) -> InstallResult:
    """Symlink every valid skill from ``source/skills/`` into ``target/``.

    Args:
      source: company-brain repo root (must contain a ``skills/`` directory).
      target: directory where Claude Code finds skills (typically
        ``~/.claude/skills/``).
      force: if True, replace existing files / symlinks pointing elsewhere.
        If False, conflicts are reported and the entry is skipped.
      dry_run: if True, no filesystem changes are made; the result still
        describes what *would* happen.

    Returns:
      :class:`InstallResult` describing every skill considered.

    Raises:
      SkillSourceError: if ``source/skills/`` is missing or contains no
        valid skill directories (a valid skill is a directory containing
        ``SKILL.md``).
    """

    source = Path(source).resolve()
    skills_dir = source / "skills"
    if not skills_dir.is_dir():
        raise SkillSourceError(
            f"no skills/ directory at {source}. Run from the company-brain repo, "
            "or pass --source <repo-path>."
        )

    skills = _discover_skills(skills_dir)
    if not skills:
        raise SkillSourceError(
            f"no skill directories found in {skills_dir} (a skill is a directory "
            "containing SKILL.md)."
        )

    # Resolve target without requiring it to exist yet.
    target = Path(target).expanduser()
    target_existed = target.exists()
    result = InstallResult(source=source, target=target.resolve() if target_existed else target, dry_run=dry_run)

    if not target_existed and not dry_run:
        target.mkdir(parents=True, exist_ok=True)
        result.target_created = True
        result.target = target.resolve()
    elif not target_existed and dry_run:
        result.target_created = True  # would create

    for skill_path in skills:
        action = _install_one(skill_path, target, force=force, dry_run=dry_run)
        result.actions.append(action)

    return result


# ---------------------------------------------------------------------------
# Internals
# ---------------------------------------------------------------------------


def _discover_skills(skills_dir: Path) -> list[Path]:
    """Return sorted skill directories (each containing SKILL.md)."""

    return sorted(
        p for p in skills_dir.iterdir()
        if p.is_dir() and (p / "SKILL.md").is_file()
    )


def _install_one(
    skill_path: Path, target: Path, *, force: bool, dry_run: bool
) -> SkillAction:
    """Symlink a single skill into target/<name>. Returns the action taken."""

    name = skill_path.name
    link = target / name
    resolved_source = skill_path.resolve()

    # Already a symlink pointing at our source: skip.
    if link.is_symlink():
        try:
            existing_target = link.resolve()
        except (OSError, RuntimeError):
            existing_target = None
        if existing_target == resolved_source:
            return SkillAction(name, resolved_source, link, "skipped", "already linked")

        if not force:
            return SkillAction(
                name,
                resolved_source,
                link,
                "conflict",
                f"symlink points to {existing_target or '<unresolved>'}; --force to replace",
            )

        if dry_run:
            return SkillAction(name, resolved_source, link, "planned", "would replace existing symlink")

        link.unlink()
        link.symlink_to(resolved_source)
        return SkillAction(name, resolved_source, link, "replaced", "")

    # Exists but is not a symlink: only replace under --force.
    if link.exists():
        if not force:
            return SkillAction(
                name,
                resolved_source,
                link,
                "conflict",
                "existing non-symlink file or directory; --force to replace",
            )

        if dry_run:
            return SkillAction(
                name, resolved_source, link, "planned", "would remove existing entry and link"
            )

        if link.is_dir() and not link.is_symlink():
            shutil.rmtree(link)
        else:
            link.unlink()
        link.symlink_to(resolved_source)
        return SkillAction(name, resolved_source, link, "replaced", "")

    # Fresh install.
    if dry_run:
        return SkillAction(name, resolved_source, link, "planned", "would link")

    link.symlink_to(resolved_source)
    return SkillAction(name, resolved_source, link, "installed", "")
