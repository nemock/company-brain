"""company-brain CLI.

This is the typer-based command framework. v0.1.0 ships the framework and a
root banner; real subcommands land per the roadmap:

  - cb validate          (v0.1.0)
  - cb render <doc>      (v0.3.0)
  - cb viewer            (v0.4.0)
  - cb fetch <url>       (v1.x)
  - cb intake-510k <K>   (v1.x)
  - cb prune-snapshots   (v1.x)

Subcommands are registered against the `app` Typer instance below as they
land. `cb --help` reflects whatever has been registered.
"""

from __future__ import annotations

import typer

from . import __version__

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

Pre-1.0, under active development. No usable subcommands yet.

Run `cb --help` to see available commands as they land.

See:
  https://github.com/nemock/company-brain
  ROADMAP.md for milestone sequencing
  PRD.md for design
"""


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


def main() -> None:
    """Entry point declared in pyproject.toml as `cb`."""
    app()


if __name__ == "__main__":
    main()
