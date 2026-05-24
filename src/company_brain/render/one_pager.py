"""One-pager generator.

A 1-page summary suitable as a sales leave-behind, partnership intro, or
new-hire orientation handout. PRD §11 structure:

1. Product name + one-line positioning (from primary pillar).
2. Who it's for (from primary persona + ICP pillar).
3. What it does (from product + primary feature).
4. Why it matters (from one customer-interview source, if present).
5. Status + how to learn more (footer with version + link).

The one-pager exists to prove the doc-generate framework is general — it
shares the Jinja env, the branding loader, the idempotency contract, and
the controlled-document footer policy with the MRD, but renders a tight,
single-page artifact instead of a 5–10-page MRD.

Output formats: markdown (this module) and html (sub-piece 4). Docx less
useful for a one-pager; skipped unless requested per PRD §11.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from .. import __version__
from ..vault import Node, Vault, load_vault
from .engine import build_environment, load_branding
from .html_writer import render_html
from .mrd import (
    _CONTROLLED_DOCUMENT_FOOTER,
    _FORMAT_EXTENSIONS,
    RenderResult,
    _by_type,
    _is_non_goal,
    _node_view,
    _source_view,
)


_ONE_PAGER_FORMATS = {"markdown", "html"}


def render_one_pager(
    vault_path: Path,
    *,
    output_path: Path | None = None,
    generation_date: date | None = None,
    write: bool = True,
    output_format: str = "markdown",
) -> RenderResult:
    """Render the one-pager for the vault at ``vault_path``.

    Supports ``output_format`` ``markdown`` (default) and ``html``. Docx is
    not supported for the one-pager per PRD §11 ("Docx less useful for a
    one-pager; skipped unless requested").
    """

    if output_format not in _ONE_PAGER_FORMATS:
        raise ValueError(
            f"one-pager supports {sorted(_ONE_PAGER_FORMATS)}; got '{output_format}'"
        )

    vault = load_vault(vault_path)
    branding = load_branding(vault_path)
    env = build_environment(vault_path)
    template = env.get_template("one-pager.md.j2")

    context = _build_context(
        vault,
        branding=branding,
        generation_date=generation_date or date.today(),
    )
    body_markdown = template.render(**context)

    target = output_path or (
        vault_path / "exports" / f"one-pager{_FORMAT_EXTENSIONS[output_format]}"
    )

    if output_format == "markdown":
        content: str = body_markdown
        if write:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
    else:  # html
        content = render_html(
            title=context["meta"]["doc_title"],
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
        template_name="one-pager.md.j2",
        branding=branding,
        output_format=output_format,
    )


def _build_context(
    vault: Vault, *, branding, generation_date: date
) -> dict[str, Any]:
    profile = vault.profile_name or "default"
    is_meddev = profile == "medical-device"
    nodes = sorted(vault.nodes, key=lambda n: n.id)

    products = _by_type(nodes, "product")
    pillars = _by_type(nodes, "pillar")
    personas = _by_type(nodes, "persona")
    features = _by_type(nodes, "feature")
    customer_interviews = [
        n
        for n in _by_type(nodes, "source")
        if str(n.frontmatter.get("source_kind", "")) == "customer-interview"
    ]

    primary_product = products[0] if products else None
    primary_pillar = _pick_primary_pillar(pillars)
    primary_persona = personas[0] if personas else None
    primary_feature = _pick_primary_feature(features, primary_product)
    primary_interview = customer_interviews[0] if customer_interviews else None

    return {
        "meta": {
            "vault_path": str(vault.path),
            "profile": profile,
            "is_medical_device": is_meddev,
            "appends_controlled_document_footer": is_meddev,
            "controlled_document_footer": _CONTROLLED_DOCUMENT_FOOTER,
            "cb_version": __version__,
            "generation_date": generation_date.isoformat(),
            "doc_title": "One-pager",
        },
        "branding": branding.as_dict(),
        "product": _node_view(primary_product) if primary_product else None,
        "pillar": _node_view(primary_pillar) if primary_pillar else None,
        "persona": _node_view(primary_persona) if primary_persona else None,
        "feature": _node_view(primary_feature) if primary_feature else None,
        "interview": _source_view(primary_interview) if primary_interview else None,
    }


def _pick_primary_pillar(pillars: list[Node]) -> Node | None:
    """Highest-confidence positive (non-goal-excluded) pillar; first id wins ties."""

    positive = [p for p in pillars if not _is_non_goal(p)]
    if not positive:
        return None
    # Sort by (-confidence, id) so the head is highest confidence, then
    # lexicographically first id as the tiebreaker.
    positive_sorted = sorted(
        positive,
        key=lambda p: (-float(p.frontmatter.get("confidence") or 0.0), p.id),
    )
    return positive_sorted[0]


def _pick_primary_feature(
    features: list[Node], product: Node | None
) -> Node | None:
    """Prefer features whose edges touch the primary product, else the first feature."""

    if not features:
        return None
    if product is None:
        return features[0]
    product_id = product.id
    for feature in features:
        for edge in feature.edges:
            if edge.target == product_id and edge.type in {"part_of", "supports", "related_to"}:
                return feature
    return features[0]
