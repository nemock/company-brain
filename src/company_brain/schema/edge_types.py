"""Edge types.

v1 inherits the Infinite Brain edge set unchanged. Predicate-of-clearance and
IFU-history relationships use ``preceded_by`` / ``followed_by`` rather than
introducing new types.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EdgeTypeSpec:
    """One typed edge."""

    name: str
    symmetric: bool
    inverse: str | None
    default_weight: float
    description: str


EDGE_TYPE_SPECS: tuple[EdgeTypeSpec, ...] = (
    EdgeTypeSpec(
        "related_to",
        symmetric=True,
        inverse=None,
        default_weight=0.5,
        description="Real but non-specific relationship. Prefer a more specific edge when one fits.",
    ),
    EdgeTypeSpec(
        "depends_on",
        symmetric=False,
        inverse=None,
        default_weight=0.7,
        description="A cannot stand without B. Use sparingly; depends_on edges suggest brittleness.",
    ),
    EdgeTypeSpec(
        "derived_from",
        symmetric=False,
        inverse=None,
        default_weight=0.8,
        description="A claim, decision, or pattern derives from a source, note, interview, or data point. Required for provenance.",
    ),
    EdgeTypeSpec(
        "contradicts",
        symmetric=True,
        inverse=None,
        default_weight=0.8,
        description="A and B cannot both be true. Preserve contradictions rather than smoothing them.",
    ),
    EdgeTypeSpec(
        "supports",
        symmetric=False,
        inverse=None,
        default_weight=0.7,
        description="A strengthens or expresses B. Common for decision → pillar.",
    ),
    EdgeTypeSpec(
        "part_of",
        symmetric=False,
        inverse=None,
        default_weight=0.8,
        description="A belongs to a larger pillar, playbook, or concept. In v2, quantity edge metadata extends this for BOM modeling.",
    ),
    EdgeTypeSpec(
        "preceded_by",
        symmetric=False,
        inverse="followed_by",
        default_weight=0.8,
        description=(
            "A came after B in time or sequence. Used for IFU history chains "
            "(later IFU preceded_by earlier IFU) and predicate device chains "
            "(clearance preceded_by its predicate)."
        ),
    ),
    EdgeTypeSpec(
        "followed_by",
        symmetric=False,
        inverse="preceded_by",
        default_weight=0.8,
        description=(
            "A came before B in time or sequence. Inverse of preceded_by. "
            "The maintainer auto-fills this when preceded_by is set."
        ),
    ),
    EdgeTypeSpec(
        "authored_by",
        symmetric=False,
        inverse=None,
        default_weight=0.6,
        description="A was authored by B. Used when people are modeled as nodes.",
    ),
    EdgeTypeSpec(
        "tagged_with",
        symmetric=False,
        inverse=None,
        default_weight=0.4,
        description="A is tagged with B. Use only if tags are modeled as nodes; otherwise use the tags frontmatter field.",
    ),
)


EDGE_TYPES: dict[str, EdgeTypeSpec] = {spec.name: spec for spec in EDGE_TYPE_SPECS}


def get_edge_type(name: str) -> EdgeTypeSpec | None:
    """Look up an edge type spec by name."""

    return EDGE_TYPES.get(name)
