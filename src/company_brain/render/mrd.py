"""MRD (Marketing Requirements Document) generator.

The MRD pulls from the typed vault: pillars, persona, customer, competitor,
indication-for-use, requirements (class=market), metrics, sources. The
template (``templates/mrd.md.j2``) is profile-aware — medical-device-only
sections are not rendered for other profiles.

The MRD section structure follows PRD §11:

| # | Section                          | Profile           |
|---|----------------------------------|-------------------|
| 1 | Executive summary                | all               |
| 2 | Vision and positioning           | all               |
| 3 | Indications for use              | medical-device    |
| 4 | Market and personas              | all               |
| 5 | Market requirements              | all               |
| 6 | Competitive landscape            | all               |
| 7 | Regulatory landscape             | medical-device    |
| 8 | Evidence vs. vision split        | all               |
| 9 | Open questions                   | all               |
| 10| What we are explicitly not doing | all               |
| 11| Sources                          | all               |

Generation is deterministic. Re-running on an unchanged vault produces
byte-identical output modulo the single ``Generated`` footer line, which
is the only place the timestamp lives.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from .. import __version__
from ..vault import Node, Vault, load_vault
from .docx_writer import render_docx
from .engine import Branding, build_environment, load_branding
from .html_writer import render_html


# Source kinds that flag a claim as vision-driven vs. evidence-driven.
# Used for the evidence-vs-vision split section of the MRD.
_VISION_SOURCE_KINDS = frozenset(
    {"founder-vision", "strategic-thesis", "domain-expertise"}
)
_EVIDENCE_SOURCE_KINDS = frozenset(
    {
        "customer-interview",
        "market-data",
        "internal-data",
        "prior-internal-doc",
        "fda-510k-summary",
        "regulatory-filing",
        "web-snapshot",
        "web-snapshot-network",
        "press-release",
    }
)
# `citation` and `skill-output` are neutral — they're labeled but not
# bucketed as vision or evidence in the split.

_CONTROLLED_DOCUMENT_FOOTER = (
    "> This is a planning artifact. It is not a controlled document and is "
    "not part of any design history file, risk management file, or "
    "traceability matrix per ISO 14971, IEC 62304, or 21 CFR 820."
)


@dataclass
class RenderResult:
    """The result of rendering one document."""

    content: str | bytes
    output_path: Path | None
    template_name: str
    branding: Branding
    output_format: str = "markdown"


_FORMAT_EXTENSIONS = {"markdown": ".md", "html": ".html", "docx": ".docx"}


def render_mrd(
    vault_path: Path,
    *,
    output_path: Path | None = None,
    generation_date: date | None = None,
    write: bool = True,
    output_format: str = "markdown",
) -> RenderResult:
    """Render the MRD for the vault at ``vault_path``.

    ``output_format`` is one of ``markdown`` (default), ``html``, or ``docx``.
    When ``write`` is true, the result is written to ``output_path`` (defaults
    to ``<vault>/exports/MRD<ext>`` with the extension chosen by format).

    ``generation_date`` lets tests pin the date for idempotency assertions.
    Defaults to today's date.
    """

    if output_format not in _FORMAT_EXTENSIONS:
        raise ValueError(
            f"unknown output_format '{output_format}'; "
            f"one of: {', '.join(_FORMAT_EXTENSIONS)}"
        )

    vault = load_vault(vault_path)
    branding = load_branding(vault_path)
    env = build_environment(vault_path)
    template = env.get_template("mrd.md.j2")

    context = _build_context(
        vault,
        branding=branding,
        generation_date=generation_date or date.today(),
    )
    body_markdown = template.render(**context)

    target = output_path or (
        vault_path / "exports" / f"MRD{_FORMAT_EXTENSIONS[output_format]}"
    )

    content: str | bytes
    if output_format == "markdown":
        content = body_markdown
        if write:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
    elif output_format == "html":
        content = render_html(
            title=context["meta"]["doc_title"],
            body_markdown=body_markdown,
            branding=branding,
            vault_path=vault_path,
        )
        if write:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
    else:  # docx
        content = render_docx(
            title=context["meta"]["doc_title"],
            body_markdown=body_markdown,
            branding=branding,
            output_path=target if write else None,
            generation_date=generation_date or date.today(),
        )

    return RenderResult(
        content=content,
        output_path=target if write else None,
        template_name="mrd.md.j2",
        branding=branding,
        output_format=output_format,
    )


# ---------------------------------------------------------------------------
# Context assembly
# ---------------------------------------------------------------------------


def _build_context(
    vault: Vault, *, branding: Branding, generation_date: date
) -> dict[str, Any]:
    """Walk the vault and assemble the MRD render context.

    Iteration order is deterministic everywhere (sorted by id). This is the
    foundation of the idempotency guarantee.
    """

    profile = vault.profile_name or "default"
    is_meddev = profile == "medical-device"

    nodes_by_id = vault.nodes_by_id
    nodes = sorted(vault.nodes, key=lambda n: n.id)

    pillars = _by_type(nodes, "pillar")
    positive_pillars = [p for p in pillars if not _is_non_goal(p)]
    non_goal_pillars = [p for p in pillars if _is_non_goal(p)]

    sources = _by_type(nodes, "source")
    vision_sources = [s for s in sources if _source_kind(s) in _VISION_SOURCE_KINDS]

    personas = _by_type(nodes, "persona")
    customers = _by_type(nodes, "customer")
    competitors = _by_type(nodes, "competitor")
    products = _by_type(nodes, "product")
    questions = _by_type(nodes, "question")

    market_requirements = [
        n
        for n in _by_type(nodes, "requirement")
        if str(n.frontmatter.get("requirement_class", "")) == "market"
    ]

    decisions = _by_type(nodes, "decision")
    rules_out_decisions = [d for d in decisions if _has_rules_out_section(d)]

    # Medical-device-only buckets.
    our_ifus: list[Node] = []
    competitor_ifus: list[Node] = []
    competitor_products: set[str] = set()
    clearances: list[Node] = []
    regulations: list[Node] = []
    standards: list[Node] = []

    if is_meddev:
        # Build the set of competitor product ids by walking competitor edges
        # to their IFUs and back to belongs_to_product. This lets us split
        # our IFUs from competitor IFUs deterministically.
        competitor_ifu_ids: set[str] = set()
        for competitor in competitors:
            for edge in competitor.edges:
                target = nodes_by_id.get(edge.target)
                if target is not None and target.type == "indication-for-use":
                    competitor_ifu_ids.add(target.id)
        for ifu in _by_type(nodes, "indication-for-use"):
            (competitor_ifus if ifu.id in competitor_ifu_ids else our_ifus).append(ifu)

        for ifu in competitor_ifus:
            product_id = ifu.frontmatter.get("belongs_to_product")
            if product_id:
                competitor_products.add(str(product_id))

        clearances = _by_type(nodes, "regulatory-clearance")
        regulations = _by_type(nodes, "regulation")
        standards = _by_type(nodes, "standard")

    # IFU comparison: rows = products that have at least one IFU. Latest IFU
    # per product wins (by verified_at).
    ifu_comparison_rows = _build_ifu_comparison(
        our_ifus + competitor_ifus, nodes_by_id
    ) if is_meddev else []

    # Evidence-vs-vision split: classify every "claim" node by its derived_from
    # source kinds. Claim nodes = pillars, decisions, requirements, hypotheses,
    # facts, patterns, indications-for-use (when present). Sources themselves
    # are excluded.
    evidence_split = _classify_evidence_vs_vision(nodes, nodes_by_id)

    return {
        "meta": {
            "vault_path": str(vault.path),
            "profile": profile,
            "is_medical_device": is_meddev,
            "appends_controlled_document_footer": is_meddev,
            "controlled_document_footer": _CONTROLLED_DOCUMENT_FOOTER,
            "cb_version": __version__,
            "generation_date": generation_date.isoformat(),
            "doc_title": "Marketing Requirements Document",
        },
        "branding": branding.as_dict(),
        "products": [_node_view(n) for n in products],
        "pillars_positive": [_node_view(n) for n in positive_pillars],
        "pillars_non_goal": [_node_view(n) for n in non_goal_pillars],
        "vision_sources": [_source_view(n) for n in vision_sources],
        "personas": [_node_view(n) for n in personas],
        "customers": [_node_view(n) for n in customers],
        "competitors": [_competitor_view(n, nodes_by_id) for n in competitors],
        "market_requirements": [_node_view(n) for n in market_requirements],
        "our_ifus": [_ifu_view(n) for n in our_ifus],
        "competitor_ifus": [_ifu_view(n) for n in competitor_ifus],
        "ifu_comparison_rows": ifu_comparison_rows,
        "clearances": [_clearance_view(n) for n in clearances],
        "regulations": [_node_view(n) for n in regulations],
        "standards": [_node_view(n) for n in standards],
        "rules_out_decisions": [_decision_view(n) for n in rules_out_decisions],
        "open_questions": [_node_view(n) for n in questions],
        "all_sources": [_source_view(n) for n in sources],
        "evidence_split": evidence_split,
    }


# ---------------------------------------------------------------------------
# Helpers — node classification and viewing
# ---------------------------------------------------------------------------


def _by_type(nodes: list[Node], type_name: str) -> list[Node]:
    return sorted([n for n in nodes if n.type == type_name], key=lambda n: n.id)


def _is_non_goal(pillar: Node) -> bool:
    """A pillar is a non-goal pillar if its tags include 'non-goal' or its
    title starts with 'Non-Goal' (case-insensitive). Tag is the primary
    signal; title is the fallback for vaults that haven't tagged yet.
    """

    tags = pillar.frontmatter.get("tags") or []
    if isinstance(tags, list) and any(str(t).lower() == "non-goal" for t in tags):
        return True
    title = str(pillar.frontmatter.get("title", "")).strip().lower()
    return title.startswith("non-goal")


def _has_rules_out_section(decision: Node) -> bool:
    return "## What This Rules Out" in decision.body


def _source_kind(node: Node) -> str:
    return str(node.frontmatter.get("source_kind", ""))


def _node_view(node: Node) -> dict[str, Any]:
    """Compact dict the template renders against. Includes id, title, summary,
    confidence, verified_at, source_kind (if any), and a 'cite' alias for
    in-template citation rendering.
    """

    fm = node.frontmatter
    return {
        "id": node.id,
        "type": node.type,
        "title": str(fm.get("title", node.id)),
        "summary": str(fm.get("summary", "")),
        "namespace": str(fm.get("namespace", "")),
        "confidence": fm.get("confidence"),
        "verified_at": _to_str(fm.get("verified_at")),
        "tags": list(fm.get("tags") or []),
        "applicable_when": fm.get("applicable_when"),
        "source_kind": fm.get("source_kind"),
        "cite": f"[{node.id}]",
    }


def _source_view(node: Node) -> dict[str, Any]:
    view = _node_view(node)
    view["source_kind"] = _source_kind(node) or "unknown"
    view["url"] = node.frontmatter.get("url") or node.frontmatter.get("source_url")
    return view


def _competitor_view(node: Node, nodes_by_id: dict[str, Node]) -> dict[str, Any]:
    view = _node_view(node)
    view["legal_name"] = node.frontmatter.get("legal_name")
    view["canonical_url"] = node.frontmatter.get("canonical_url")
    related_ids = sorted({e.target for e in node.edges if e.target in nodes_by_id})
    view["related_ifus"] = [
        nodes_by_id[i].id for i in related_ids if nodes_by_id[i].type == "indication-for-use"
    ]
    view["related_clearances"] = [
        nodes_by_id[i].id for i in related_ids if nodes_by_id[i].type == "regulatory-clearance"
    ]
    return view


def _ifu_view(node: Node) -> dict[str, Any]:
    view = _node_view(node)
    fm = node.frontmatter
    view["population"] = str(fm.get("population", "")).strip()
    view["condition"] = str(fm.get("condition", "")).strip()
    view["intervention"] = str(fm.get("intervention", "")).strip()
    view["setting"] = str(fm.get("setting", "")).strip()
    view["belongs_to_product"] = fm.get("belongs_to_product")
    return view


def _clearance_view(node: Node) -> dict[str, Any]:
    view = _node_view(node)
    fm = node.frontmatter
    for k in (
        "clearance_number",
        "clearance_type",
        "clearance_date",
        "applicant",
        "device_name",
        "product_codes",
        "summary_url",
    ):
        view[k] = _to_str(fm.get(k))
    # preceded_by edges are the predicate chain.
    view["predicates"] = sorted({e.target for e in node.edges if e.type == "preceded_by"})
    return view


def _decision_view(node: Node) -> dict[str, Any]:
    view = _node_view(node)
    view["rules_out"] = _extract_rules_out(node.body)
    return view


def _extract_rules_out(body: str) -> str:
    """Pull the markdown block under ``## What This Rules Out`` until the next
    H2. Returns the inner content trimmed of trailing whitespace."""

    marker = "## What This Rules Out"
    idx = body.find(marker)
    if idx == -1:
        return ""
    rest = body[idx + len(marker):]
    end = rest.find("\n## ")
    if end == -1:
        chunk = rest
    else:
        chunk = rest[:end]
    return chunk.strip()


def _to_str(value: Any) -> str:
    if value is None:
        return ""
    if hasattr(value, "isoformat") and not isinstance(value, str):
        return value.isoformat()
    return str(value)


# ---------------------------------------------------------------------------
# Evidence vs. vision split
# ---------------------------------------------------------------------------


_CLAIM_TYPES = frozenset(
    {
        "pillar",
        "decision",
        "requirement",
        "hypothesis",
        "fact",
        "pattern",
        "indication-for-use",
        "regulatory-clearance",
    }
)


def _classify_evidence_vs_vision(
    nodes: list[Node], nodes_by_id: dict[str, Node]
) -> dict[str, Any]:
    """Classify every claim node by the source_kinds it derives from.

    A node's classification is:

    * **vision** if any one-hop ``derived_from`` lands on a source whose
      ``source_kind`` is in :data:`_VISION_SOURCE_KINDS`.
    * **evidence** if any one-hop ``derived_from`` lands on a source whose
      ``source_kind`` is in :data:`_EVIDENCE_SOURCE_KINDS`.
    * Both are possible — a decision can derive from a strategic thesis AND
      a customer interview. The node appears in both buckets.
    * **neither** if no derived_from edges resolve, or only neutral-kind
      sources do. This is flagged as 'uncited' in the report.
    """

    vision_nodes: list[dict[str, Any]] = []
    evidence_nodes: list[dict[str, Any]] = []
    uncited_nodes: list[dict[str, Any]] = []

    for node in nodes:
        if node.type not in _CLAIM_TYPES:
            continue
        kinds = _derived_source_kinds(node, nodes_by_id)
        view = {"id": node.id, "title": str(node.frontmatter.get("title", node.id))}
        is_vision = any(k in _VISION_SOURCE_KINDS for k in kinds)
        is_evidence = any(k in _EVIDENCE_SOURCE_KINDS for k in kinds)
        if is_vision:
            vision_nodes.append(view)
        if is_evidence:
            evidence_nodes.append(view)
        if not is_vision and not is_evidence:
            uncited_nodes.append(view)

    vision_nodes.sort(key=lambda v: v["id"])
    evidence_nodes.sort(key=lambda v: v["id"])
    uncited_nodes.sort(key=lambda v: v["id"])

    return {
        "vision_count": len(vision_nodes),
        "evidence_count": len(evidence_nodes),
        "uncited_count": len(uncited_nodes),
        "vision_nodes": vision_nodes,
        "evidence_nodes": evidence_nodes,
        "uncited_nodes": uncited_nodes,
    }


def _derived_source_kinds(node: Node, nodes_by_id: dict[str, Node]) -> set[str]:
    out: set[str] = set()
    for edge in node.edges:
        if edge.type != "derived_from":
            continue
        target = nodes_by_id.get(edge.target)
        if target is None or target.type != "source":
            continue
        kind = _source_kind(target)
        if kind:
            out.add(kind)
    return out


# ---------------------------------------------------------------------------
# IFU comparison table
# ---------------------------------------------------------------------------


def _build_ifu_comparison(
    ifus: list[Node], nodes_by_id: dict[str, Node]
) -> list[dict[str, Any]]:
    """Return one row per product, with its latest IFU's structured fields.

    Latest = max ``verified_at`` among IFUs for that product. Rows sorted by
    product id for determinism.
    """

    by_product: dict[str, list[Node]] = {}
    for ifu in ifus:
        product_id = str(ifu.frontmatter.get("belongs_to_product") or "")
        if not product_id:
            continue
        by_product.setdefault(product_id, []).append(ifu)

    rows: list[dict[str, Any]] = []
    for product_id in sorted(by_product.keys()):
        latest = max(
            by_product[product_id],
            key=lambda n: _to_str(n.frontmatter.get("verified_at")),
        )
        product = nodes_by_id.get(product_id)
        rows.append(
            {
                "product_id": product_id,
                "product_title": product.frontmatter.get("title", product_id)
                if product is not None
                else product_id,
                "ifu_id": latest.id,
                "population": str(latest.frontmatter.get("population", "")).strip(),
                "condition": str(latest.frontmatter.get("condition", "")).strip(),
                "intervention": str(latest.frontmatter.get("intervention", "")).strip(),
                "setting": str(latest.frontmatter.get("setting", "")).strip(),
            }
        )
    return rows
