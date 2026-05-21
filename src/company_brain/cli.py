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
        help="Regenerate _system/*.md even when those files already exist.",
    ),
) -> None:
    """Scaffold a new company-brain vault.

    Creates the folder tree for the chosen profile, plus ``_attachments/``,
    ``exports/``, and the ``_system/`` reference files (PROFILE.md, INDEX.md,
    NODE-TYPES.md, EDGE-TYPES.md, FRONTMATTER-SCHEMA.md).

    Does not write node content. Use the ``intake`` or ``atomize`` skill for
    that, then ``cb validate`` to check the vault.
    """

    try:
        result = scaffold_vault(path.resolve(), profile, force=force)
    except ProfileNotFoundError as exc:
        typer.secho(f"error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from exc
    except NotADirectoryError as exc:
        typer.secho(f"error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from exc

    typer.echo(f"Scaffolded company-brain vault at {result.vault_path}")
    typer.echo(f"  profile:           {result.profile_name}")
    typer.echo(f"  folders created:   {result.folder_count}")
    typer.echo(f"  _system files:     {result.file_count}")
    if result.files_skipped:
        typer.secho(
            f"  files skipped:     {len(result.files_skipped)} (existed; pass --force to regenerate)",
            fg=typer.colors.YELLOW,
        )
    typer.echo("")
    typer.echo("Next steps:")
    typer.echo("  - Add knowledge via the `intake` or `atomize` skill.")
    typer.echo("  - Run `cb validate` (lands in v0.1.0 step 4).")


def main() -> None:
    """Entry point declared in pyproject.toml as `cb`."""
    app()


if __name__ == "__main__":
    main()
