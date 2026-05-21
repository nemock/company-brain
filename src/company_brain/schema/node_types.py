"""Node types.

Three categories:

* **Epistemic** — inherited from the Infinite Brain schema (pillar, decision,
  fact, etc.). Always available regardless of profile.
* **Entity** — company-brain additions for products, people, requirements, and
  metrics. Always available regardless of profile.
* **Profile-conditional** — only present when the active profile enables
  them. Medical-device adds indications-for-use, regulatory clearances, and
  ISO-14971-vocabulary risk nodes.

Folder paths are relative to the vault root. The vault-architect skill reads
this registry to scaffold the folder tree.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .frontmatter import FieldSpec, FieldType


class NodeCategory(str, Enum):
    EPISTEMIC = "epistemic"
    ENTITY = "entity"
    PROFILE_CONDITIONAL = "profile-conditional"


@dataclass(frozen=True)
class NodeTypeSpec:
    """One node type."""

    name: str
    folder: str
    category: NodeCategory
    description: str
    profile: str | None = None  # None means always available
    extra_required_fields: tuple[FieldSpec, ...] = field(default_factory=tuple)
    notes: tuple[str, ...] = field(default_factory=tuple)


# ---------------------------------------------------------------------------
# Epistemic — inherited from Infinite Brain. Always available.
# ---------------------------------------------------------------------------

_EPISTEMIC_TYPES: tuple[NodeTypeSpec, ...] = (
    NodeTypeSpec(
        "pillar",
        "pillars",
        NodeCategory.EPISTEMIC,
        "A durable principle that should shape future agent answers. Can be written in negative form for strategic non-goals.",
        notes=(
            "Auto-inject pillars must declare applicable_when.",
            "Non-goal pillars (e.g., 'we do not enter the consumer market') belong here.",
        ),
    ),
    NodeTypeSpec(
        "decision",
        "decisions",
        NodeCategory.EPISTEMIC,
        "A concrete choice between alternatives. The body should include a '## What This Rules Out' section.",
        notes=("Anti-decisions (deliberate non-choices) live here, not in a separate type.",),
    ),
    NodeTypeSpec(
        "playbook",
        "playbooks",
        NodeCategory.EPISTEMIC,
        "A repeatable procedure.",
    ),
    NodeTypeSpec(
        "pattern",
        "patterns",
        NodeCategory.EPISTEMIC,
        "An observed regularity across examples.",
    ),
    NodeTypeSpec(
        "hypothesis",
        "hypotheses",
        NodeCategory.EPISTEMIC,
        "A falsifiable prediction or bet.",
    ),
    NodeTypeSpec(
        "fact",
        "facts",
        NodeCategory.EPISTEMIC,
        "A verified atomic claim. May be a metric snapshot if it carries metric_id.",
        notes=("Confidence decay applies to facts linked to medium/high-volatility metrics.",),
    ),
    NodeTypeSpec(
        "concept",
        "concepts",
        NodeCategory.EPISTEMIC,
        "A defined term or mental model.",
    ),
    NodeTypeSpec(
        "source",
        "sources",
        NodeCategory.EPISTEMIC,
        "External material with synthesis. Provenance anchor.",
        extra_required_fields=(
            FieldSpec(
                "source_kind",
                FieldType.STRING,
                "One of the registered SourceKind values. Drives MRD claim labeling.",
            ),
        ),
        notes=(
            "source_kind: skill-output also requires producing_skill.",
            "source_kind: web-snapshot also requires url, captured_at, captured_method, attachment.",
        ),
    ),
    NodeTypeSpec(
        "question",
        "questions",
        NodeCategory.EPISTEMIC,
        "A known unknown worth preserving because answering it would change a decision, pillar, playbook, or hypothesis.",
    ),
    NodeTypeSpec(
        "note",
        "notes",
        NodeCategory.EPISTEMIC,
        "Temporary capture or weakly-structured material. Should graduate to a more specific type when it earns one.",
    ),
)


# ---------------------------------------------------------------------------
# Entity — company-brain additions. Always available.
# ---------------------------------------------------------------------------

_ENTITY_TYPES: tuple[NodeTypeSpec, ...] = (
    NodeTypeSpec(
        "product",
        "entities/products",
        NodeCategory.ENTITY,
        "A shipped or in-development product. Opaque in v1; v2 introduces BOM and components.",
    ),
    NodeTypeSpec(
        "product-line",
        "entities/product-lines",
        NodeCategory.ENTITY,
        "A family of related products.",
    ),
    NodeTypeSpec(
        "persona",
        "entities/personas",
        NodeCategory.ENTITY,
        "An archetypal user, distinct from a named real customer.",
    ),
    NodeTypeSpec(
        "customer",
        "entities/customers",
        NodeCategory.ENTITY,
        "A named real customer (anonymize as needed).",
    ),
    NodeTypeSpec(
        "stakeholder",
        "entities/stakeholders",
        NodeCategory.ENTITY,
        "Internal or external party with influence on a product or program.",
    ),
    NodeTypeSpec(
        "competitor",
        "entities/competitors",
        NodeCategory.ENTITY,
        "A named competitor or alternative. legal_name + canonical_url required for disambiguation.",
        extra_required_fields=(
            FieldSpec("legal_name", FieldType.STRING, "Legal company name."),
            FieldSpec("canonical_url", FieldType.STRING, "The competitor's primary domain. Scopes all subsequent capture."),
        ),
    ),
    NodeTypeSpec(
        "vendor",
        "entities/vendors",
        NodeCategory.ENTITY,
        "A supplier, contractor, or service provider.",
    ),
    NodeTypeSpec(
        "requirement",
        "entities/requirements",
        NodeCategory.ENTITY,
        "A market, user, or system requirement. Class is mandatory so the node is never mistaken for a controlled design input.",
        extra_required_fields=(
            FieldSpec(
                "requirement_class",
                FieldType.STRING,
                "One of: market, user, system, software, hardware. Drives which requirements-doc generator picks the node up.",
            ),
        ),
    ),
    NodeTypeSpec(
        "feature",
        "entities/features",
        NodeCategory.ENTITY,
        "A product capability.",
    ),
    NodeTypeSpec(
        "use-case",
        "entities/use-cases",
        NodeCategory.ENTITY,
        "A scenario of use, framed around a job-to-be-done.",
    ),
    NodeTypeSpec(
        "metric",
        "entities/metrics",
        NodeCategory.ENTITY,
        "The concept of a measurement (MRR, churn, day-7 retention). Time-series fact nodes link back via metric_id.",
        extra_required_fields=(
            FieldSpec(
                "volatility_class",
                FieldType.STRING,
                "One of: low, medium, high. Drives confidence decay half-life for snapshot facts.",
            ),
        ),
    ),
)


# ---------------------------------------------------------------------------
# Profile-conditional — medical-device.
# ---------------------------------------------------------------------------

_MEDDEV_TYPES: tuple[NodeTypeSpec, ...] = (
    NodeTypeSpec(
        "indication-for-use",
        "entities/indications-for-use",
        NodeCategory.PROFILE_CONDITIONAL,
        "Population + condition + intervention + setting. Belongs to a product (ours or a competitor's). Versioned via preceded_by chain.",
        profile="medical-device",
        extra_required_fields=(
            FieldSpec("population", FieldType.STRING, "Patient or user population the device is for."),
            FieldSpec("condition", FieldType.STRING, "Condition, disease, or use context being addressed."),
            FieldSpec("intervention", FieldType.STRING, "What the device does — the action it takes or supports."),
            FieldSpec("setting", FieldType.STRING, "Care setting (hospital, ambulatory, home, etc.)."),
            FieldSpec("belongs_to_product", FieldType.STRING, "Id of the product node this IFU belongs to."),
        ),
        notes=("Always carries controlled_document: false.",),
    ),
    NodeTypeSpec(
        "regulatory-clearance",
        "risk/regulatory-clearances",
        NodeCategory.PROFILE_CONDITIONAL,
        "A specific clearance event (510(k), De Novo, PMA, breakthrough designation, letter-to-file). Predicate chains use preceded_by edges.",
        profile="medical-device",
        extra_required_fields=(
            FieldSpec("clearance_number", FieldType.STRING, "K-number or equivalent identifier."),
            FieldSpec("clearance_type", FieldType.STRING, "510k | de-novo | pma | breakthrough | letter-to-file."),
            FieldSpec("clearance_date", FieldType.DATE, "Date of clearance."),
            FieldSpec("applicant", FieldType.STRING, "Applicant company name."),
            FieldSpec("device_name", FieldType.STRING, "Cleared device name."),
            FieldSpec("product_codes", FieldType.LIST, "FDA product codes (e.g., DRT)."),
            FieldSpec("summary_url", FieldType.STRING, "URL to the public clearance summary PDF."),
        ),
        notes=("Always carries controlled_document: false.",),
    ),
    NodeTypeSpec(
        "risk-insight",
        "risk/risk-insights",
        NodeCategory.PROFILE_CONDITIONAL,
        "A planning-level observation about risk. Not a risk record.",
        profile="medical-device",
        notes=("Always carries controlled_document: false.",),
    ),
    NodeTypeSpec(
        "hazard",
        "risk/hazards",
        NodeCategory.PROFILE_CONDITIONAL,
        "A potential source of harm, in ISO 14971 vocabulary, captured for thinking.",
        profile="medical-device",
        notes=("Always carries controlled_document: false.",),
    ),
    NodeTypeSpec(
        "hazardous-situation",
        "risk/hazardous-situations",
        NodeCategory.PROFILE_CONDITIONAL,
        "A circumstance where a hazard could lead to harm.",
        profile="medical-device",
        notes=("Always carries controlled_document: false.",),
    ),
    NodeTypeSpec(
        "harm",
        "risk/harms",
        NodeCategory.PROFILE_CONDITIONAL,
        "A potential physical injury, damage, or impact.",
        profile="medical-device",
        notes=("Always carries controlled_document: false.",),
    ),
    NodeTypeSpec(
        "risk-control-idea",
        "risk/risk-control-ideas",
        NodeCategory.PROFILE_CONDITIONAL,
        "A candidate mitigation under consideration. Not a chosen risk control.",
        profile="medical-device",
        notes=("Always carries controlled_document: false.",),
    ),
    NodeTypeSpec(
        "regulation",
        "risk/regulations",
        NodeCategory.PROFILE_CONDITIONAL,
        "A cited regulation (MDR, 21 CFR 820, etc.).",
        profile="medical-device",
    ),
    NodeTypeSpec(
        "standard",
        "risk/standards",
        NodeCategory.PROFILE_CONDITIONAL,
        "A cited standard (ISO 14971, IEC 62304, IEC 60601, etc.).",
        profile="medical-device",
    ),
)


NODE_TYPE_SPECS: tuple[NodeTypeSpec, ...] = (
    *_EPISTEMIC_TYPES,
    *_ENTITY_TYPES,
    *_MEDDEV_TYPES,
)


NODE_TYPES: dict[str, NodeTypeSpec] = {spec.name: spec for spec in NODE_TYPE_SPECS}


def get_node_type(name: str) -> NodeTypeSpec | None:
    """Look up a node type spec by name."""

    return NODE_TYPES.get(name)


def get_active_node_types(profile_name: str | None) -> tuple[NodeTypeSpec, ...]:
    """Return the node types active for a given profile.

    Always-available types (epistemic + entity) are always included. A
    profile-conditional type is included only when its ``profile`` matches.
    Passing ``None`` returns only the always-available types — the ``default``
    profile.
    """

    return tuple(
        spec
        for spec in NODE_TYPE_SPECS
        if spec.profile is None or spec.profile == profile_name
    )
