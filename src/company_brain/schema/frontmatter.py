"""Frontmatter schema: field specs and the base required set.

The shape borrowed wholesale from the Infinite Brain schema, with company-brain
additions documented per node type in :mod:`company_brain.schema.node_types`.

This module is data only. Validators live in
:mod:`company_brain.schema.validators`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class FieldType(str, Enum):
    """Allowed field types in node frontmatter.

    Kept narrow on purpose. EDGE_LIST is special-cased because edges have
    their own structured shape (target / type / weight / note).
    """

    STRING = "string"
    BOOLEAN = "boolean"
    NUMBER = "number"
    DATE = "date"
    LIST = "list"
    EDGE_LIST = "edge-list"


@dataclass(frozen=True)
class FieldSpec:
    """A single frontmatter field."""

    name: str
    type: FieldType
    description: str
    default: object | None = None
    required: bool = True


# ---------------------------------------------------------------------------
# Base required fields — inherited from the Infinite Brain schema and applied
# to every node regardless of type or profile.
# ---------------------------------------------------------------------------

BASE_REQUIRED_FIELDS: tuple[FieldSpec, ...] = (
    FieldSpec("id", FieldType.STRING, "Stable kebab-case identifier, prefix matches the node type."),
    FieldSpec("title", FieldType.STRING, "Human-readable title."),
    FieldSpec("type", FieldType.STRING, "The node type. Must match a registered NodeTypeSpec.name."),
    FieldSpec("namespace", FieldType.STRING, "Visibility / category label. Free-form for v1."),
    FieldSpec("summary", FieldType.STRING, "One line, 100–200 chars, lets an agent decide whether to load the body."),
    FieldSpec("auto_inject", FieldType.BOOLEAN, "If true, the node enters agent context when applicable_when matches.", default=False),
    FieldSpec("applicable_when", FieldType.STRING, "When auto_inject is true, the condition under which the node injects.", required=False),
    FieldSpec("confidence", FieldType.NUMBER, "0.0–1.0. How trustworthy is this node?"),
    FieldSpec("verified_at", FieldType.DATE, "ISO date the node was last verified."),
    FieldSpec("verified_by", FieldType.STRING, "Handle of the verifier."),
    FieldSpec("staleness_signal", FieldType.STRING, "Concrete description of what would make this node stale.", required=False),
    FieldSpec("tags", FieldType.LIST, "Free-form tags.", default=list()),
    FieldSpec("edges", FieldType.EDGE_LIST, "Typed outbound edges.", default=list()),
    FieldSpec("related", FieldType.LIST, "Loose related-to references (untyped). Prefer edges.", default=list()),
    FieldSpec("source_url", FieldType.STRING, "External URL backing this node, when one exists.", required=False),
    FieldSpec(
        "controlled_document",
        FieldType.BOOLEAN,
        "Affirmative declaration that this is a planning artifact, not a controlled record.",
        default=False,
    ),
)


def base_field_names() -> frozenset[str]:
    """Return the set of base-required field names. Used by validators."""

    return frozenset(f.name for f in BASE_REQUIRED_FIELDS)
