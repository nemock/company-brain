"""company-brain CLI.

This is the typer-based command framework. Subcommands are registered against
the ``app`` Typer instance below as they land per the roadmap:

  - cb scaffold          (v0.1.0 — implemented)
  - cb validate          (v0.1.0 — implemented)
  - cb describe-*        (v0.2.0 — implemented)
  - cb extract           (v0.2.0 — implemented)
  - cb install-skills    (v0.2.0 — implemented)
  - cb list-nodes        (v0.3.0 — implemented)
  - cb get-node          (v0.3.0 — implemented)
  - cb render <doc>      (v0.3.0 — implemented)
  - cb viewer            (v0.4.0)
  - cb fetch <url>       (v1.x)
  - cb intake-510k <K>   (v1.x)
  - cb prune-snapshots   (v1.x)
"""

from __future__ import annotations

from pathlib import Path

import typer

from . import __version__
from .install_skills import SkillSourceError, install_skills as install_skills_fn
from .intake_helpers import (
    ExtractError,
    ProfileLookupError,
    UnknownNodeTypeError,
    UnsupportedFormatError,
    describe_node,
    describe_profile,
    extract_text,
    to_json,
)
from .maintain import (
    audit as maintain_audit,
    decay as maintain_decay,
    rebuild_index as maintain_rebuild_index,
    repair as maintain_repair,
)
from .query_helpers import NodeNotFoundError, get_node, list_nodes
from .render import (
    ScaffoldProfileError,
    list_scaffold_names,
    render_mrd,
    render_one_pager,
    render_scaffold,
)
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
            "Run the maintain skill's auto-repair pass before validating. "
            "Fixes filename-id mismatch, missing inverse edges, "
            "missing controlled_document:false on risk/IFU nodes, and "
            "regenerates _system/INDEX.md. Errors that need human input "
            "(unknown types, duplicate ids, broken edge targets) are left "
            "for you to address."
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

    vault_path = path.resolve()

    if fix:
        try:
            repair_result = maintain_repair(vault_path, dry_run=False)
        except VaultNotFoundError as exc:
            typer.secho(f"error: {exc}", fg=typer.colors.RED, err=True)
            raise typer.Exit(code=2) from exc
        if repair_result.actions or repair_result.index_rebuilt:
            typer.secho(
                f"Auto-fix: {len(repair_result.actions)} change(s)"
                + (", INDEX.md regenerated." if repair_result.index_rebuilt else "."),
                fg=typer.colors.GREEN,
            )
            for action in repair_result.actions:
                typer.echo(
                    f"  {action.code}  {action.node_id}  ({action.path}): {action.detail}"
                )
            typer.echo("")

    try:
        issues = validate(vault_path)
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

    if counts.get("error", 0) > 0:
        raise typer.Exit(code=1)


@app.command("describe-node")
def describe_node_command(
    type_name: str = typer.Argument(
        ...,
        metavar="TYPE",
        help="Node type name (e.g. 'pillar', 'indication-for-use').",
    ),
    path: Path | None = typer.Option(
        None,
        "--path",
        "-P",
        help=(
            "Optional vault path. When provided, emits a stderr warning if the "
            "node type is not active in the vault's profile. The JSON description "
            "is still printed (the schema itself is profile-agnostic)."
        ),
    ),
) -> None:
    """Print a JSON description of a node type, including folder and required fields.

    Read-only. Consumed by the intake/atomize skills to stay aligned with
    the schema without re-implementing it.
    """

    try:
        spec = describe_node(type_name)
    except UnknownNodeTypeError as exc:
        typer.secho(f"error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from exc

    if path is not None:
        try:
            profile_data = describe_profile(vault_path=path.resolve())
        except ProfileLookupError as exc:
            typer.secho(
                f"warning: --path provided but vault profile could not be read: {exc}",
                fg=typer.colors.YELLOW,
                err=True,
            )
        else:
            active_names = {t.get("name") for t in profile_data.get("active_node_types", [])}
            if type_name not in active_names:
                typer.secho(
                    f"warning: '{type_name}' is not active in profile "
                    f"'{profile_data.get('profile')}' at {path}.",
                    fg=typer.colors.YELLOW,
                    err=True,
                )

    typer.echo(to_json(spec))


@app.command("describe-profile")
def describe_profile_command(
    path: Path = typer.Option(
        Path("."),
        "--path",
        "-P",
        help="Vault directory to read PROFILE.md from. Ignored if --name is set.",
    ),
    name: str | None = typer.Option(
        None,
        "--name",
        "-n",
        help="Profile name to describe directly (e.g. 'medical-device'). Bypasses PROFILE.md read.",
    ),
) -> None:
    """Print a JSON description of a profile, including its active node types.

    Reads the active profile from the vault's `_system/PROFILE.md` by default,
    or describes a profile by name when `--name` is provided. Read-only.
    """

    try:
        if name is not None:
            data = describe_profile(profile_name=name)
        else:
            data = describe_profile(vault_path=path.resolve())
    except ProfileLookupError as exc:
        typer.secho(f"error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from exc
    typer.echo(to_json(data))


@app.command("extract")
def extract_command(
    file: Path = typer.Argument(
        ...,
        metavar="FILE",
        help="Path to a .docx or .pdf file to extract text from.",
    ),
) -> None:
    """Extract text from a .docx or .pdf to stdout.

    Used by the `atomize` skill to ingest binary documents. For markdown,
    plain text, or transcripts, read the file directly. For images, use
    Claude's native vision capabilities. Read-only.
    """

    try:
        text = extract_text(file)
    except UnsupportedFormatError as exc:
        typer.secho(f"error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from exc
    except ExtractError as exc:
        typer.secho(f"error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(text, nl=False)


_RENDER_FIRST_CLASS = ("mrd", "one-pager")
_RENDER_FORMAT_CHOICES = ("markdown", "html", "docx")


def _all_render_choices() -> tuple[str, ...]:
    return _RENDER_FIRST_CLASS + tuple(list_scaffold_names())


@app.command("render")
def render_command(
    doc: str = typer.Argument(
        ...,
        metavar="DOC",
        help=(
            "Document to render. v0.3.0 first-class: mrd, one-pager. v0.4.0 "
            "scaffolds: pid, project-charter, stakeholder-register, "
            "risk-register, status-report, meeting-minutes, lessons-learned, "
            "business-plan, sales-battle-card, competitive-brief, "
            "ifu-comparison, decision-log, press-release, investor-update, "
            "onboarding-doc, srd, srs, hrs, risk-brainstorm."
        ),
    ),
    path: Path = typer.Option(
        Path("."),
        "--path",
        "-P",
        help="Vault directory. Defaults to the current directory.",
    ),
    out: Path | None = typer.Option(
        None,
        "--out",
        "-o",
        help=(
            "Output path. Defaults to <vault>/exports/<doc>.<ext> where "
            "ext is .md / .html / .docx per --format."
        ),
    ),
    output_format: str = typer.Option(
        "markdown",
        "--format",
        "-f",
        help=(
            f"Output format. One of: {', '.join(_RENDER_FORMAT_CHOICES)}. "
            "Scaffolds support markdown and html only (docx + xlsx land "
            "with the v1.x full implementations). One-pager doesn't support docx."
        ),
    ),
    competitor_id: str | None = typer.Option(
        None,
        "--competitor",
        help=(
            "For the sales-battle-card scaffold: the competitor node id to "
            "render against. Defaults to the first competitor by id."
        ),
    ),
    date_override: str | None = typer.Option(
        None,
        "--date",
        help=(
            "Pin the generation date (YYYY-MM-DD). For idempotency assertions; "
            "defaults to today."
        ),
    ),
) -> None:
    """Render a planning document from the vault.

    v0.3.0 ships full MRD (markdown/html/docx) and one-pager (markdown/html).
    v0.4.0 ships 19 scaffolded generators for PID, business plan, sales
    battle card, decision log, SRD/SRS/HRS, etc. — runnable templates with
    typed-node citations and `_scaffold_` footer flags that adopters fill in.
    """

    choices = _all_render_choices()
    if doc not in choices:
        typer.secho(
            f"error: unknown doc '{doc}'. Known: {', '.join(choices)}.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=2)

    if output_format not in _RENDER_FORMAT_CHOICES:
        typer.secho(
            f"error: unknown format '{output_format}'. One of: {', '.join(_RENDER_FORMAT_CHOICES)}.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=2)

    gen_date = None
    if date_override is not None:
        from datetime import date

        try:
            gen_date = date.fromisoformat(date_override)
        except ValueError as exc:
            typer.secho(
                f"error: --date must be YYYY-MM-DD ({exc})",
                fg=typer.colors.RED,
                err=True,
            )
            raise typer.Exit(code=2) from exc

    out_resolved = out.resolve() if out is not None else None

    try:
        if doc == "mrd":
            result = render_mrd(
                path.resolve(),
                output_path=out_resolved,
                generation_date=gen_date,
                write=True,
                output_format=output_format,
            )
        elif doc == "one-pager":
            if output_format == "docx":
                typer.secho(
                    "error: the one-pager doesn't ship a docx writer "
                    "(PRD §11). Use --format markdown or --format html.",
                    fg=typer.colors.RED,
                    err=True,
                )
                raise typer.Exit(code=2)
            result = render_one_pager(
                path.resolve(),
                output_path=out_resolved,
                generation_date=gen_date,
                write=True,
                output_format=output_format,
            )
        else:
            # Scaffold path.
            if output_format == "docx":
                typer.secho(
                    f"error: scaffolds don't yet ship docx output ('{doc}'). "
                    "Use --format markdown or --format html. Full docx support "
                    "lands with the v1.x full implementations.",
                    fg=typer.colors.RED,
                    err=True,
                )
                raise typer.Exit(code=2)
            options: dict[str, str] = {}
            if competitor_id is not None:
                options["competitor_id"] = competitor_id
            result = render_scaffold(
                doc,
                path.resolve(),
                output_path=out_resolved,
                generation_date=gen_date,
                write=True,
                output_format=output_format,
                options=options,
            )
    except VaultNotFoundError as exc:
        typer.secho(f"error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from exc
    except ScaffoldProfileError as exc:
        typer.secho(f"error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from exc
    except ValueError as exc:
        typer.secho(f"error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from exc

    assert result.output_path is not None
    size = (
        len(result.content)
        if isinstance(result.content, (bytes, bytearray))
        else len(result.content.encode("utf-8"))
    )
    typer.echo(f"Rendered {doc} ({output_format}) → {result.output_path}")
    typer.echo(f"  template:  {result.template_name}")
    typer.echo(f"  bytes:     {size}")


@app.command("list-nodes")
def list_nodes_command(
    path: Path = typer.Option(
        Path("."),
        "--path",
        "-P",
        help="Vault directory to query. Defaults to the current directory.",
    ),
    type_name: str | None = typer.Option(
        None,
        "--type",
        "-t",
        help="Filter to one node type (e.g. 'pillar', 'competitor').",
    ),
    namespace: str | None = typer.Option(
        None,
        "--namespace",
        "-n",
        help="Filter to one namespace.",
    ),
    auto_inject_only: bool = typer.Option(
        False,
        "--auto-inject-only",
        help="Only return nodes with `auto_inject: true` (the pillars set).",
    ),
    source_kind: str | None = typer.Option(
        None,
        "--source-kind",
        help="Filter source nodes by source_kind (e.g. 'fda-510k-summary').",
    ),
) -> None:
    """List vault nodes as JSON. Used by the `query` skill for candidate selection.

    Returns one object per matching node with the frontmatter fields that
    matter for retrieval (id, title, type, namespace, summary, auto_inject,
    applicable_when, confidence, verified_at, staleness_signal, tags, plus
    relevant type-specific fields). Includes the outbound edge list.
    Sorted by id for deterministic output.
    """

    try:
        nodes = list_nodes(
            path.resolve(),
            type_name=type_name,
            namespace=namespace,
            auto_inject_only=auto_inject_only,
            source_kind=source_kind,
        )
    except VaultNotFoundError as exc:
        typer.secho(f"error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from exc

    typer.echo(to_json({"count": len(nodes), "nodes": nodes}))


@app.command("get-node")
def get_node_command(
    node_id: str = typer.Argument(
        ...,
        metavar="ID",
        help="The node id to fetch (e.g. 'pillar-icp-ambulatory-cardiac-patients').",
    ),
    path: Path = typer.Option(
        Path("."),
        "--path",
        "-P",
        help="Vault directory to query. Defaults to the current directory.",
    ),
) -> None:
    """Return one node's full frontmatter, body, and edges (both directions) as JSON.

    The inbound-edges view is what makes typed edge walks cheap: when an
    LLM asks 'what derives from this source?' or 'what depends on this
    decision?', the answer is one CLI call instead of a vault-wide grep.
    """

    try:
        data = get_node(path.resolve(), node_id)
    except VaultNotFoundError as exc:
        typer.secho(f"error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from exc
    except NodeNotFoundError as exc:
        typer.secho(f"error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from exc

    typer.echo(to_json(data))


maintain_app = typer.Typer(
    name="maintain",
    help=(
        "Vault maintenance: auto-repair, confidence decay, INDEX.md "
        "regeneration, audit. Read+write companion to `cb validate`."
    ),
    no_args_is_help=True,
    add_completion=False,
)
app.add_typer(maintain_app, name="maintain")


@maintain_app.command("repair")
def maintain_repair_command(
    path: Path = typer.Option(
        Path("."),
        "--path",
        "-P",
        help="Vault directory. Defaults to the current directory.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show what would change without writing anything.",
    ),
) -> None:
    """Auto-fix what can be fixed without ambiguity.

    Repairs filename-id mismatch (renames the file to match its id),
    missing inverse edges (auto-fills `followed_by` when `preceded_by`
    points the other way), and missing `controlled_document: false` on
    risk/IFU nodes. Regenerates `_system/INDEX.md`. Idempotent.

    Errors that need human input (unknown types, duplicate ids, broken
    edge targets, missing required fields) are left alone — run
    `cb validate` to see them.
    """

    try:
        result = maintain_repair(path.resolve(), dry_run=dry_run)
    except VaultNotFoundError as exc:
        typer.secho(f"error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from exc

    prefix = "(dry-run) " if dry_run else ""
    typer.echo(f"{prefix}{len(result.actions)} repair action(s).")
    for action in result.actions:
        typer.echo(
            f"  {action.code}  {action.node_id}  ({action.path}): {action.detail}"
        )
    if result.index_rebuilt:
        typer.echo(f"{prefix}INDEX.md regenerated.")


@maintain_app.command("decay")
def maintain_decay_command(
    path: Path = typer.Option(
        Path("."),
        "--path",
        "-P",
        help="Vault directory. Defaults to the current directory.",
    ),
    today: str | None = typer.Option(
        None,
        "--today",
        help=(
            "Pin the reference date (YYYY-MM-DD) for decay computation. "
            "Defaults to the system date."
        ),
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show what would change without writing anything.",
    ),
) -> None:
    """Apply confidence decay to fact snapshots linked to volatile metrics.

    Fact nodes with a `metric_id` get their confidence reduced based on
    age and the metric's `volatility_class`. Half-life by class:
    low = 24mo, medium = 6mo, high = 1mo. The original confidence is
    preserved as `confidence_original` so re-runs are idempotent.
    """

    today_date = None
    if today is not None:
        from datetime import date

        try:
            today_date = date.fromisoformat(today)
        except ValueError as exc:
            typer.secho(
                f"error: --today must be YYYY-MM-DD ({exc})",
                fg=typer.colors.RED,
                err=True,
            )
            raise typer.Exit(code=2) from exc

    try:
        result = maintain_decay(path.resolve(), today=today_date, dry_run=dry_run)
    except VaultNotFoundError as exc:
        typer.secho(f"error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from exc

    prefix = "(dry-run) " if dry_run else ""
    typer.echo(f"{prefix}{len(result.actions)} decay update(s).")
    for action in result.actions:
        typer.echo(
            f"  {action.node_id}  metric={action.metric_id} "
            f"({action.volatility_class}, age={action.age_months}mo): "
            f"{action.confidence_before:.2f} → {action.confidence_after:.2f}"
        )


@maintain_app.command("audit")
def maintain_audit_command(
    path: Path = typer.Option(
        Path("."),
        "--path",
        "-P",
        help="Vault directory. Defaults to the current directory.",
    ),
) -> None:
    """Read-only health summary: repair candidates, decay candidates, notices."""

    try:
        report = maintain_audit(path.resolve())
    except VaultNotFoundError as exc:
        typer.secho(f"error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from exc

    typer.echo(f"Repair candidates: {len(report.repair_candidates)}")
    for action in report.repair_candidates:
        typer.echo(f"  {action.code}  {action.node_id}: {action.detail}")
    typer.echo("")
    typer.echo(f"Decay candidates: {len(report.decay_candidates)}")
    for action in report.decay_candidates:
        typer.echo(
            f"  {action.node_id}  ({action.volatility_class}, "
            f"age={action.age_months}mo): "
            f"{action.confidence_before:.2f} → {action.confidence_after:.2f}"
        )
    typer.echo("")
    typer.echo("Findings:")
    for finding in report.findings:
        color = (
            typer.colors.CYAN if finding.severity == "info" else typer.colors.YELLOW
        )
        typer.secho(f"  [{finding.severity}] {finding.code}: {finding.message}", fg=color)


@maintain_app.command("rebuild-index")
def maintain_rebuild_index_command(
    path: Path = typer.Option(
        Path("."),
        "--path",
        "-P",
        help="Vault directory. Defaults to the current directory.",
    ),
) -> None:
    """Regenerate `<vault>/_system/INDEX.md` from the current nodes."""

    try:
        target = maintain_rebuild_index(path.resolve())
    except VaultNotFoundError as exc:
        typer.secho(f"error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from exc
    typer.echo(f"Regenerated {target}")


@app.command("install-skills")
def install_skills_command(
    source: Path = typer.Option(
        Path("."),
        "--source",
        "-s",
        help=(
            "Path to the company-brain repo (must contain a skills/ directory). "
            "Defaults to the current directory."
        ),
    ),
    target: Path = typer.Option(
        Path.home() / ".claude" / "skills",
        "--target",
        "-t",
        help="Directory where Claude Code looks for skills. Default: ~/.claude/skills/.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help=(
            "Replace any existing file or symlink at target paths. Without --force, "
            "conflicts are reported and skipped."
        ),
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show what would happen without making any filesystem changes.",
    ),
) -> None:
    """Symlink the company-brain skills into Claude Code's skill directory.

    Run once after ``uv tool install`` so Claude Code can find the seven skills
    shipped with company-brain (``vault-architect``, ``intake``, ``atomize``,
    ``query``, ``doc-generate``, ``maintain``, ``visualize``).

    Re-running is safe: symlinks already pointing at the right source are
    reported as ``skipped``. Conflicts with existing files or links pointing
    elsewhere are reported and skipped unless ``--force`` is passed.
    """

    try:
        result = install_skills_fn(source, target, force=force, dry_run=dry_run)
    except SkillSourceError as exc:
        typer.secho(f"error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from exc

    if dry_run:
        typer.secho("(dry-run; no changes will be made)", fg=typer.colors.CYAN)
    typer.echo(f"source: {result.source}")
    typer.echo(f"target: {result.target}")
    if result.target_created:
        typer.echo(f"  {'would create' if dry_run else 'created'} target directory")
    typer.echo("")

    for action in result.actions:
        if action.status == "installed":
            typer.secho(f"  installed   {action.name}", fg=typer.colors.GREEN)
        elif action.status == "replaced":
            typer.secho(f"  replaced    {action.name}", fg=typer.colors.GREEN)
        elif action.status == "planned":
            typer.secho(f"  would link  {action.name}  ({action.detail})", fg=typer.colors.CYAN)
        elif action.status == "skipped":
            typer.echo(f"  skipped     {action.name}  ({action.detail})")
        elif action.status == "conflict":
            typer.secho(
                f"  conflict    {action.name}  ({action.detail})",
                fg=typer.colors.YELLOW,
            )

    if result.conflicts:
        typer.echo("")
        typer.secho(
            f"{len(result.conflicts)} conflict(s). Re-run with --force to replace, "
            "or remove the existing entries manually.",
            fg=typer.colors.YELLOW,
            err=True,
        )
        raise typer.Exit(code=1)


def main() -> None:
    """Entry point declared in pyproject.toml as `cb`."""
    app()


if __name__ == "__main__":
    main()
