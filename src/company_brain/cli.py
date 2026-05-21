"""company-brain CLI.

This is the typer-based command framework. Subcommands are registered against
the ``app`` Typer instance below as they land per the roadmap:

  - cb scaffold          (v0.1.0 — implemented)
  - cb validate          (v0.1.0 — pending)
  - cb render <doc>      (v0.3.0)
  - cb viewer            (v0.4.0)
  - cb fetch <url>       (v1.x)
  - cb intake-510k <K>   (v1.x)
  - cb prune-snapshots   (v1.x)
"""

from __future__ import annotations

from pathlib import Path

import typer

from . import __version__
from .scaffold import ProfileNotFoundError, scaffold as scaffold_vault
from .schema import PROFILE_SPECS
from .validator import VaultNotFoundError, summarize, validate

app = typer.Typer(
    name="cb",
    help=(
        "company-brain — AI-native company knowledge graph.\n\n"
        "Pre-1.0, under active development. Run `cb --help` to see the "
        "subcommands that have landed so far."
    ),
    no_args_is_help=False,
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)


_BANNER = f"""company-brain {__version__}

Pre-1.0, under active development. Run `cb --help` to see available subcommands.

See:
  https://github.com/nemock/company-brain
  ROADMAP.md for milestone sequencing
  PRD.md for design
"""


_VALID_PROFILES = sorted(p.name for p in PROFILE_SPECS)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def root(
    ctx: typer.Context,
    version: bool = typer.Option(
        False,
        "-V",
        "--version",
        callback=_version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    """company-brain CLI.

    When invoked with no subcommand, prints the pre-development banner. As
    subcommands land in v0.1.0+, they appear in `cb --help`.
    """
    if ctx.invoked_subcommand is None:
        typer.echo(_BANNER, nl=False)


@app.command("scaffold")
def scaffold_command(
    profile: str = typer.Option(
        ...,
        "--profile",
        "-p",
        help=f"Industry profile. One of: {', '.join(_VALID_PROFILES)}.",
    ),
    path: Path = typer.Option(
        Path("."),
        "--path",
        "-P",
        help="Vault directory. Created if missing. Defaults to the current directory.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help=(
            "Regenerate _system/*.md, _branding/ starters, .gitignore, "
            "and README.md even when those files already exist."
        ),
    ),
    git: bool = typer.Option(
        True,
        "--git/--no-git",
        help=(
            "Initialize the vault as a git repository (default). Runs "
            "`git init` and creates an initial commit. Pass --no-git to "
            "scaffold without touching git (useful for example vaults "
            "that live inside another git repo, or for users without git)."
        ),
    ),
) -> None:
    """Scaffold a new company-brain vault.

    Creates the folder tree for the chosen profile, plus ``_attachments/``,
    ``_branding/``, ``exports/``, and the ``_system/`` reference files
    (PROFILE.md, INDEX.md, NODE-TYPES.md, EDGE-TYPES.md,
    FRONTMATTER-SCHEMA.md). Writes a vault-level ``.gitignore`` and
    ``README.md``. By default, runs ``git init`` and creates an initial
    commit so the vault is ready to push to GitHub / GitLab / Bitbucket /
    any git host.

    Does not write node content. Use the ``intake`` or ``atomize`` skill for
    that, then ``cb validate`` to check the vault.
    """

    try:
        result = scaffold_vault(path.resolve(), profile, force=force, init_git=git)
    except ProfileNotFoundError as exc:
        typer.secho(f"error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from exc
    except NotADirectoryError as exc:
        typer.secho(f"error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from exc

    typer.echo(f"Scaffolded company-brain vault at {result.vault_path}")
    typer.echo(f"  profile:           {result.profile_name}")
    typer.echo(f"  folders created:   {result.folder_count}")
    typer.echo(f"  files written:     {result.file_count}")
    if result.files_skipped:
        typer.secho(
            f"  files skipped:     {len(result.files_skipped)} (existed; pass --force to regenerate)",
            fg=typer.colors.YELLOW,
        )

    if git:
        if result.git_initialized and result.git_initial_commit:
            typer.echo(f"  git:               initialized; initial commit {result.git_initial_commit[:10]}")
        elif result.git_initialized:
            typer.echo("  git:               initialized")
        elif result.git_skipped_reason:
            typer.secho(
                f"  git:               skipped ({result.git_skipped_reason})",
                fg=typer.colors.YELLOW,
            )
    else:
        typer.echo("  git:               disabled (--no-git)")

    typer.echo("")
    typer.echo("Next steps:")
    if git and result.git_initialized:
        typer.echo("  - Add a remote: `git remote add origin <url>` then `git push -u origin main`.")
    typer.echo("  - Add knowledge via the `intake` or `atomize` skill.")
    typer.echo("  - Run `cb validate` (lands in v0.1.0 step 4).")


@app.command("validate")
def validate_command(
    path: Path = typer.Option(
        Path("."),
        "--path",
        "-P",
        help="Vault directory to validate. Defaults to the current directory.",
    ),
    fix: bool = typer.Option(
        False,
        "--fix",
        help=(
            "Auto-fix issues where possible. v0.1.0 stub — full implementation "
            "lands with the maintain skill in v0.4.0."
        ),
    ),
) -> None:
    """Validate a company-brain vault against the schema.

    Loads every node markdown file in the vault, parses frontmatter, and
    runs schema checks. Reports errors and warnings, then exits non-zero
    if any errors were found.

    Vault must contain ``_system/PROFILE.md`` declaring an active profile;
    otherwise the path is not recognized as a vault.
    """

    try:
        issues = validate(path.resolve())
    except VaultNotFoundError as exc:
        typer.secho(f"error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from exc

    # Stable sort by severity (errors first), then code.
    severity_order = {"error": 0, "warning": 1, "info": 2}
    issues_sorted = sorted(issues, key=lambda i: (severity_order.get(i.severity, 99), i.code, str(i.path or "")))

    colors = {
        "error": typer.colors.RED,
        "warning": typer.colors.YELLOW,
        "info": typer.colors.CYAN,
    }

    for issue in issues_sorted:
        prefix = typer.style(
            f"[{issue.severity}]", fg=colors.get(issue.severity, typer.colors.WHITE)
        )
        loc = f" ({issue.path})" if issue.path else ""
        nid = f" {issue.node_id}" if issue.node_id else ""
        typer.echo(f"{prefix} {issue.code}{nid}{loc}: {issue.message}")

    counts = summarize(issues)
    typer.echo("")
    typer.echo(
        f"Summary: {counts.get('error', 0)} error(s), "
        f"{counts.get('warning', 0)} warning(s), "
        f"{counts.get('info', 0)} info."
    )

    if fix:
        typer.secho(
            "  --fix is a stub in v0.1.0; full auto-fix lands in v0.4.0 with the maintain skill.",
            fg=typer.colors.YELLOW,
        )

    if counts.get("error", 0) > 0:
        raise typer.Exit(code=1)


def main() -> None:
    """Entry point declared in pyproject.toml as `cb`."""
    app()


if __name__ == "__main__":
    main()
