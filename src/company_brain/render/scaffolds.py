"""Scaffolded document generators (v0.4.0 step 2).

PRD §11 lists 19 doc types beyond the MRD and one-pager. v0.4.0 ships
each as a *scaffold*: a runnable Jinja2 template that queries the right
typed nodes, fills in what it can, and flags the output as a scaffold
in the footer. Adopters fill in placeholders by hand; full
implementations land per-doc in v1.x as adopter demand surfaces.

Architecture:

* One small ``_build_<doc>_context`` function per scaffold (data
  assembly), reusing the helpers in :mod:`render.mrd`.
* One template per scaffold under ``src/company_brain/templates/``.
* :data:`SCAFFOLD_REGISTRY` maps the public doc name to the (builder,
  template, profile_required, default_output_format) tuple.
* :func:`render_scaffold` is the single entry point — handles loading,
  branding, format dispatch (markdown / html), and writing.

The render orchestration mirrors :func:`render.mrd.render_mrd` so a
future v1.x promotion of any scaffold to "full implementation" is a
focused rewrite of the data-assembly function, not a rebuild of the
plumbing.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Callable

from .. import __version__
from ..vault import Vault, load_vault
from .engine import Branding, build_environment, load_branding
from .html_writer import render_html
from .mrd import (
    _CONTROLLED_DOCUMENT_FOOTER,
    RenderResult,
    _by_type,
    _competitor_view,
    _decision_view,
    _ifu_view,
    _is_non_goal,
    _node_view,
    _source_view,
)


SCAFFOLD_FOOTER = (
    "> _v0.4.0 scaffold — full implementation pending in v1.x. "
    "Adopters: fill in the placeholders below and re-run `cb render`._"
)


class ScaffoldProfileError(ValueError):
    """Raised when a scaffold is invoked under a profile that doesn't enable it."""


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


_SCAFFOLD_FORMATS = {"markdown", "html"}


def render_scaffold(
    doc_name: str,
    vault_path: Path,
    *,
    output_path: Path | None = None,
    generation_date: date | None = None,
    write: bool = True,
    output_format: str = "markdown",
    options: dict[str, Any] | None = None,
) -> RenderResult:
    """Render one of the registered scaffolds.

    ``options`` carries scaffold-specific arguments (e.g. ``competitor_id``
    for the sales battle card). Unknown keys are ignored.
    """

    if doc_name not in SCAFFOLD_REGISTRY:
        raise ValueError(
            f"unknown scaffold '{doc_name}'. Registered: "
            f"{', '.join(sorted(SCAFFOLD_REGISTRY))}"
        )
    if output_format not in _SCAFFOLD_FORMATS:
        raise ValueError(
            f"scaffolds support {sorted(_SCAFFOLD_FORMATS)}; got '{output_format}'"
        )

    entry = SCAFFOLD_REGISTRY[doc_name]
    vault = load_vault(vault_path)
    profile_name = vault.profile_name or "default"

    if entry.profile_required is not None and profile_name != entry.profile_required:
        raise ScaffoldProfileError(
            f"the '{doc_name}' scaffold requires the '{entry.profile_required}' "
            f"profile; this vault uses '{profile_name}'."
        )

    branding = load_branding(vault_path)
    env = build_environment(vault_path)
    template = env.get_template(entry.template_name)

    # Normalize options to a single mutable dict so the builder and the
    # filename helper see the same instance — some builders (e.g. the
    # sales-battle-card) write back the auto-selected competitor id so the
    # filename can include it.
    options_dict: dict[str, Any] = dict(options or {})

    context = _build_base_context(
        vault, branding=branding, generation_date=generation_date or date.today()
    )
    context["meta"]["doc_title"] = entry.title
    context["meta"]["scaffold"] = True
    context["meta"]["scaffold_footer"] = SCAFFOLD_FOOTER
    extra = entry.builder(vault, options_dict)
    context.update(extra)

    body_markdown = template.render(**context)

    target = output_path or (
        vault_path / "exports" / f"{entry.filename(options_dict)}{_ext(output_format)}"
    )

    content: str
    if output_format == "markdown":
        content = body_markdown
        if write:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
    else:  # html
        content = render_html(
            title=entry.title,
            body_markdown=body_markdown,
            branding=branding,
            vault_path=vault_path,
        )
        if write:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")

    return RenderResult(
        content=content,
        output_path=target if write else None,
        template_name=entry.template_name,
        branding=branding,
        output_format=output_format,
    )


def list_scaffold_names() -> list[str]:
    """Public list of registered scaffold doc names. Used by the CLI."""

    return sorted(SCAFFOLD_REGISTRY)


# ---------------------------------------------------------------------------
# Shared context helpers
# ---------------------------------------------------------------------------


def _ext(output_format: str) -> str:
    return ".md" if output_format == "markdown" else ".html"


def _build_base_context(
    vault: Vault, *, branding: Branding, generation_date: date
) -> dict[str, Any]:
    profile = vault.profile_name or "default"
    is_meddev = profile == "medical-device"
    return {
        "meta": {
            "vault_path": str(vault.path),
            "profile": profile,
            "is_medical_device": is_meddev,
            "appends_controlled_document_footer": is_meddev,
            "controlled_document_footer": _CONTROLLED_DOCUMENT_FOOTER,
            "cb_version": __version__,
            "generation_date": generation_date.isoformat(),
        },
        "branding": branding.as_dict(),
    }


# ---------------------------------------------------------------------------
# Per-scaffold data assembly
# ---------------------------------------------------------------------------


def _b_pid(vault: Vault, options: dict[str, Any]) -> dict[str, Any]:
    nodes = sorted(vault.nodes, key=lambda n: n.id)
    return {
        "pillars": [_node_view(n) for n in _by_type(nodes, "pillar")],
        "products": [_node_view(n) for n in _by_type(nodes, "product")],
        "stakeholders": [_node_view(n) for n in _by_type(nodes, "stakeholder")],
        "decisions": [_node_view(n) for n in _by_type(nodes, "decision")],
        "risk_insights": [_node_view(n) for n in _by_type(nodes, "risk-insight")],
    }


def _b_project_charter(vault: Vault, options: dict[str, Any]) -> dict[str, Any]:
    nodes = sorted(vault.nodes, key=lambda n: n.id)
    pillars = [_node_view(n) for n in _by_type(nodes, "pillar") if not _is_non_goal(n)]
    return {
        "primary_pillar": pillars[0] if pillars else None,
        "stakeholders": [_node_view(n) for n in _by_type(nodes, "stakeholder")],
    }


def _b_stakeholder_register(vault: Vault, options: dict[str, Any]) -> dict[str, Any]:
    nodes = sorted(vault.nodes, key=lambda n: n.id)
    return {
        "stakeholders": [_node_view(n) for n in _by_type(nodes, "stakeholder")],
    }


def _b_risk_register(vault: Vault, options: dict[str, Any]) -> dict[str, Any]:
    nodes = sorted(vault.nodes, key=lambda n: n.id)
    return {
        "risk_insights": [_node_view(n) for n in _by_type(nodes, "risk-insight")],
        "hazards": [_node_view(n) for n in _by_type(nodes, "hazard")],
        "hazardous_situations": [
            _node_view(n) for n in _by_type(nodes, "hazardous-situation")
        ],
        "harms": [_node_view(n) for n in _by_type(nodes, "harm")],
        "risk_control_ideas": [
            _node_view(n) for n in _by_type(nodes, "risk-control-idea")
        ],
    }


def _b_status_report(vault: Vault, options: dict[str, Any]) -> dict[str, Any]:
    nodes = sorted(vault.nodes, key=lambda n: n.id)
    return {
        "facts": [_node_view(n) for n in _by_type(nodes, "fact")],
        "decisions": [_node_view(n) for n in _by_type(nodes, "decision")],
        "questions": [_node_view(n) for n in _by_type(nodes, "question")],
        "patterns": [_node_view(n) for n in _by_type(nodes, "pattern")],
    }


def _b_meeting_minutes(vault: Vault, options: dict[str, Any]) -> dict[str, Any]:
    nodes = sorted(vault.nodes, key=lambda n: n.id)
    sources = [
        n
        for n in _by_type(nodes, "source")
        if str(n.frontmatter.get("source_kind", ""))
        in {"customer-interview", "internal-data"}
    ]
    return {"meeting_source": _source_view(sources[0]) if sources else None}


def _b_lessons_learned(vault: Vault, options: dict[str, Any]) -> dict[str, Any]:
    nodes = sorted(vault.nodes, key=lambda n: n.id)
    return {
        "patterns": [_node_view(n) for n in _by_type(nodes, "pattern")],
        "decisions": [_node_view(n) for n in _by_type(nodes, "decision")],
        "questions": [_node_view(n) for n in _by_type(nodes, "question")],
        "hypotheses": [_node_view(n) for n in _by_type(nodes, "hypothesis")],
    }


def _b_business_plan(vault: Vault, options: dict[str, Any]) -> dict[str, Any]:
    nodes = sorted(vault.nodes, key=lambda n: n.id)
    nodes_by_id = vault.nodes_by_id
    pillars = _by_type(nodes, "pillar")
    return {
        "pillars_positive": [
            _node_view(n) for n in pillars if not _is_non_goal(n)
        ],
        "pillars_non_goal": [_node_view(n) for n in pillars if _is_non_goal(n)],
        "products": [_node_view(n) for n in _by_type(nodes, "product")],
        "personas": [_node_view(n) for n in _by_type(nodes, "persona")],
        "customers": [_node_view(n) for n in _by_type(nodes, "customer")],
        "competitors": [
            _competitor_view(n, nodes_by_id) for n in _by_type(nodes, "competitor")
        ],
        "market_requirements": [
            _node_view(n)
            for n in _by_type(nodes, "requirement")
            if str(n.frontmatter.get("requirement_class", "")) == "market"
        ],
        "metrics": [_node_view(n) for n in _by_type(nodes, "metric")],
    }


def _b_sales_battle_card(vault: Vault, options: dict[str, Any]) -> dict[str, Any]:
    nodes = sorted(vault.nodes, key=lambda n: n.id)
    nodes_by_id = vault.nodes_by_id
    competitors = _by_type(nodes, "competitor")
    if not competitors:
        # Mutate options so the filename template doesn't break.
        options.setdefault("competitor_id", "none")
        return {
            "competitor": None,
            "pillars_positive": [],
            "pillars_non_goal": [],
            "rules_out_decisions": [],
        }
    chosen_id = options.get("competitor_id")
    competitor = None
    if chosen_id:
        for n in competitors:
            if n.id == chosen_id:
                competitor = n
                break
        if competitor is None:
            raise ValueError(
                f"competitor '{chosen_id}' not found in vault. "
                f"Known: {', '.join(c.id for c in competitors)}."
            )
    else:
        competitor = competitors[0]
        # Record the auto-chosen competitor so the output filename includes it.
        options["competitor_id"] = competitor.id

    pillars = _by_type(nodes, "pillar")
    decisions = _by_type(nodes, "decision")
    rules_out_decisions = [
        _decision_view(d) for d in decisions if "## What This Rules Out" in d.body
    ]
    return {
        "competitor": _competitor_view(competitor, nodes_by_id),
        "pillars_positive": [
            _node_view(n) for n in pillars if not _is_non_goal(n)
        ],
        "pillars_non_goal": [_node_view(n) for n in pillars if _is_non_goal(n)],
        "rules_out_decisions": rules_out_decisions,
    }


def _b_competitive_brief(vault: Vault, options: dict[str, Any]) -> dict[str, Any]:
    nodes = sorted(vault.nodes, key=lambda n: n.id)
    nodes_by_id = vault.nodes_by_id
    competitors = [
        _competitor_view(n, nodes_by_id) for n in _by_type(nodes, "competitor")
    ]
    sources = _by_type(nodes, "source")
    market_data = [
        _source_view(s)
        for s in sources
        if str(s.frontmatter.get("source_kind", "")) == "market-data"
    ]
    press_releases = [
        _source_view(s)
        for s in sources
        if str(s.frontmatter.get("source_kind", "")) == "press-release"
    ]
    return {
        "competitors": competitors,
        "market_data_sources": market_data,
        "press_release_sources": press_releases,
    }


def _b_ifu_comparison(vault: Vault, options: dict[str, Any]) -> dict[str, Any]:
    nodes = sorted(vault.nodes, key=lambda n: n.id)
    nodes_by_id = vault.nodes_by_id
    ifus = [_ifu_view(n) for n in _by_type(nodes, "indication-for-use")]
    clearances = _by_type(nodes, "regulatory-clearance")

    # Build the comparison matrix rows: one row per product (real or referenced).
    by_product: dict[str, list[dict[str, Any]]] = {}
    for ifu in ifus:
        pid = str(ifu.get("belongs_to_product") or "")
        if not pid:
            continue
        by_product.setdefault(pid, []).append(ifu)

    rows: list[dict[str, Any]] = []
    for pid in sorted(by_product):
        # Latest IFU per product by verified_at.
        chain = sorted(by_product[pid], key=lambda v: v.get("verified_at") or "")
        latest = chain[-1]
        product_node = nodes_by_id.get(pid)
        rows.append(
            {
                "product_id": pid,
                "product_title": (
                    str(product_node.frontmatter.get("title", pid))
                    if product_node is not None
                    else pid
                ),
                "chain_ids": [c["id"] for c in chain],
                "latest": latest,
            }
        )

    return {
        "ifu_rows": rows,
        "clearances": [_node_view(c) for c in clearances],
    }


def _b_decision_log(vault: Vault, options: dict[str, Any]) -> dict[str, Any]:
    nodes = sorted(vault.nodes, key=lambda n: n.id)
    decisions = _by_type(nodes, "decision")
    non_goal_pillars = [
        _node_view(n) for n in _by_type(nodes, "pillar") if _is_non_goal(n)
    ]
    return {
        "decisions": [_decision_view(d) for d in decisions],
        "non_goal_pillars": non_goal_pillars,
    }


def _b_press_release(vault: Vault, options: dict[str, Any]) -> dict[str, Any]:
    nodes = sorted(vault.nodes, key=lambda n: n.id)
    nodes_by_id = vault.nodes_by_id
    products = _by_type(nodes, "product")
    clearances = _by_type(nodes, "regulatory-clearance")
    pillars = [n for n in _by_type(nodes, "pillar") if not _is_non_goal(n)]
    sources = _by_type(nodes, "source")
    interview_or_thesis = [
        s
        for s in sources
        if str(s.frontmatter.get("source_kind", ""))
        in {"customer-interview", "strategic-thesis"}
    ]
    primary_product = products[0] if products else None
    primary_ifu = None
    if primary_product is not None:
        for edge in primary_product.edges:
            target = nodes_by_id.get(edge.target)
            if target is not None and target.type == "indication-for-use":
                primary_ifu = _ifu_view(target)
                break
    return {
        "product": _node_view(primary_product) if primary_product else None,
        "ifu": primary_ifu,
        "clearance": _node_view(clearances[0]) if clearances else None,
        "supporting_source": (
            _source_view(interview_or_thesis[0]) if interview_or_thesis else None
        ),
        "pillar": _node_view(pillars[0]) if pillars else None,
    }


def _b_investor_update(vault: Vault, options: dict[str, Any]) -> dict[str, Any]:
    nodes = sorted(vault.nodes, key=lambda n: n.id)
    facts_with_metric = [
        n
        for n in _by_type(nodes, "fact")
        if n.frontmatter.get("metric_id")
    ]
    return {
        "fact_snapshots": [_node_view(n) for n in facts_with_metric],
        "decisions": [_node_view(n) for n in _by_type(nodes, "decision")],
        "questions": [_node_view(n) for n in _by_type(nodes, "question")],
        "risk_insights": [_node_view(n) for n in _by_type(nodes, "risk-insight")],
    }


def _b_onboarding_doc(vault: Vault, options: dict[str, Any]) -> dict[str, Any]:
    nodes = sorted(vault.nodes, key=lambda n: n.id)
    pillars = _by_type(nodes, "pillar")
    auto_inject = [n for n in pillars if bool(n.frontmatter.get("auto_inject"))]
    non_goal = [n for n in pillars if _is_non_goal(n)]
    concepts = _by_type(nodes, "concept")
    personas = _by_type(nodes, "persona")
    customers = _by_type(nodes, "customer")
    decisions = _by_type(nodes, "decision")
    return {
        "auto_injecting_pillars": [_node_view(n) for n in auto_inject],
        "non_goal_pillars": [_node_view(n) for n in non_goal],
        "key_decisions": [_node_view(n) for n in decisions],
        "concepts": [_node_view(n) for n in concepts],
        "persona": _node_view(personas[0]) if personas else None,
        "customer": _node_view(customers[0]) if customers else None,
    }


def _b_requirement_doc(
    vault: Vault, requirement_class: str
) -> dict[str, Any]:
    nodes = sorted(vault.nodes, key=lambda n: n.id)
    reqs = [
        _node_view(n)
        for n in _by_type(nodes, "requirement")
        if str(n.frontmatter.get("requirement_class", "")) == requirement_class
    ]
    return {
        "requirements": reqs,
        "features": [_node_view(n) for n in _by_type(nodes, "feature")],
        "use_cases": [_node_view(n) for n in _by_type(nodes, "use-case")],
        "risk_insights": [
            _node_view(n) for n in _by_type(nodes, "risk-insight")
        ],
    }


def _b_srd(vault: Vault, options: dict[str, Any]) -> dict[str, Any]:
    return _b_requirement_doc(vault, "system")


def _b_srs(vault: Vault, options: dict[str, Any]) -> dict[str, Any]:
    return _b_requirement_doc(vault, "software")


def _b_hrs(vault: Vault, options: dict[str, Any]) -> dict[str, Any]:
    return _b_requirement_doc(vault, "hardware")


def _b_risk_brainstorm(vault: Vault, options: dict[str, Any]) -> dict[str, Any]:
    nodes = sorted(vault.nodes, key=lambda n: n.id)
    return {
        "risk_insights": [_node_view(n) for n in _by_type(nodes, "risk-insight")],
        "hazards": [_node_view(n) for n in _by_type(nodes, "hazard")],
        "hazardous_situations": [
            _node_view(n) for n in _by_type(nodes, "hazardous-situation")
        ],
        "harms": [_node_view(n) for n in _by_type(nodes, "harm")],
        "risk_control_ideas": [
            _node_view(n) for n in _by_type(nodes, "risk-control-idea")
        ],
        "related_decisions": [
            _node_view(n) for n in _by_type(nodes, "decision")
        ],
        "related_pillars": [
            _node_view(n) for n in _by_type(nodes, "pillar")
        ],
    }


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


class _ScaffoldEntry:
    """One scaffold registration."""

    def __init__(
        self,
        *,
        builder: Callable[[Vault, dict[str, Any]], dict[str, Any]],
        template_name: str,
        title: str,
        profile_required: str | None = None,
        filename_template: str | None = None,
    ) -> None:
        self.builder = builder
        self.template_name = template_name
        self.title = title
        self.profile_required = profile_required
        self._filename_template = filename_template

    def filename(self, options: dict[str, Any]) -> str:
        """Output filename stem (no extension). Defaults to template stem."""

        if self._filename_template is not None:
            return self._filename_template.format(**options)
        return self.template_name.replace(".md.j2", "")


SCAFFOLD_REGISTRY: dict[str, _ScaffoldEntry] = {
    "pid": _ScaffoldEntry(
        builder=_b_pid,
        template_name="pid.md.j2",
        title="Project Initiation Document",
    ),
    "project-charter": _ScaffoldEntry(
        builder=_b_project_charter,
        template_name="project-charter.md.j2",
        title="Project Charter",
    ),
    "stakeholder-register": _ScaffoldEntry(
        builder=_b_stakeholder_register,
        template_name="stakeholder-register.md.j2",
        title="Stakeholder Register",
    ),
    "risk-register": _ScaffoldEntry(
        builder=_b_risk_register,
        template_name="risk-register.md.j2",
        title="Risk Register (planning)",
        profile_required="medical-device",
    ),
    "status-report": _ScaffoldEntry(
        builder=_b_status_report,
        template_name="status-report.md.j2",
        title="Status Report",
    ),
    "meeting-minutes": _ScaffoldEntry(
        builder=_b_meeting_minutes,
        template_name="meeting-minutes.md.j2",
        title="Meeting Minutes",
    ),
    "lessons-learned": _ScaffoldEntry(
        builder=_b_lessons_learned,
        template_name="lessons-learned.md.j2",
        title="Lessons Learned",
    ),
    "business-plan": _ScaffoldEntry(
        builder=_b_business_plan,
        template_name="business-plan.md.j2",
        title="Business Plan",
    ),
    "sales-battle-card": _ScaffoldEntry(
        builder=_b_sales_battle_card,
        template_name="sales-battle-card.md.j2",
        title="Sales Battle Card",
        filename_template="sales-battle-card-{competitor_id}",
    ),
    "competitive-brief": _ScaffoldEntry(
        builder=_b_competitive_brief,
        template_name="competitive-brief.md.j2",
        title="Competitive Brief",
    ),
    "ifu-comparison": _ScaffoldEntry(
        builder=_b_ifu_comparison,
        template_name="ifu-comparison.md.j2",
        title="IFU Comparison Report",
        profile_required="medical-device",
    ),
    "decision-log": _ScaffoldEntry(
        builder=_b_decision_log,
        template_name="decision-log.md.j2",
        title="Decision Log",
    ),
    "press-release": _ScaffoldEntry(
        builder=_b_press_release,
        template_name="press-release.md.j2",
        title="Press Release",
    ),
    "investor-update": _ScaffoldEntry(
        builder=_b_investor_update,
        template_name="investor-update.md.j2",
        title="Investor Update",
    ),
    "onboarding-doc": _ScaffoldEntry(
        builder=_b_onboarding_doc,
        template_name="onboarding-doc.md.j2",
        title="Onboarding Doc",
    ),
    "srd": _ScaffoldEntry(
        builder=_b_srd,
        template_name="srd.md.j2",
        title="System Requirements Document (SRD)",
    ),
    "srs": _ScaffoldEntry(
        builder=_b_srs,
        template_name="srs.md.j2",
        title="Software Requirements Specification (SRS)",
    ),
    "hrs": _ScaffoldEntry(
        builder=_b_hrs,
        template_name="hrs.md.j2",
        title="Hardware Requirements Specification (HRS)",
    ),
    "risk-brainstorm": _ScaffoldEntry(
        builder=_b_risk_brainstorm,
        template_name="risk-brainstorm.md.j2",
        title="Risk Brainstorm",
        profile_required="medical-device",
    ),
}


def _filename_options_for_battle_card(options: dict[str, Any]) -> dict[str, Any]:
    """Build the options dict used by the battle-card filename template.

    The battle card's output filename includes the competitor id so multiple
    competitors can each produce a distinct file in ``exports/``. This helper
    normalizes the lookup so the CLI doesn't have to special-case it.
    """

    if "competitor_id" in options:
        return options
    return {**options, "competitor_id": "unknown"}


__all__ = [
    "SCAFFOLD_REGISTRY",
    "ScaffoldProfileError",
    "list_scaffold_names",
    "render_scaffold",
]
