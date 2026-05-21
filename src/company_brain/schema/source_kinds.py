"""Source kinds for ``source`` nodes.

The ``source_kind`` field is what the MRD generator uses to label each claim
in its output. See PRD §9 for the full provenance model.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SourceKind(str, Enum):
    """All recognized source kinds. Stable string values; do not renumber."""

    CUSTOMER_INTERVIEW = "customer-interview"
    MARKET_DATA = "market-data"
    CITATION = "citation"
    FOUNDER_VISION = "founder-vision"
    DOMAIN_EXPERTISE = "domain-expertise"
    STRATEGIC_THESIS = "strategic-thesis"
    INTERNAL_DATA = "internal-data"
    PRIOR_INTERNAL_DOC = "prior-internal-doc"
    SKILL_OUTPUT = "skill-output"
    PRESS_RELEASE = "press-release"
    WEB_SNAPSHOT = "web-snapshot"
    WEB_SNAPSHOT_NETWORK = "web-snapshot-network"
    FDA_510K_SUMMARY = "fda-510k-summary"
    REGULATORY_FILING = "regulatory-filing"


@dataclass(frozen=True)
class SourceKindSpec:
    """Description of a source kind, used to render docs and MRD bibliography labels."""

    kind: SourceKind
    label: str
    description: str
    example: str


SOURCE_KIND_SPECS: tuple[SourceKindSpec, ...] = (
    SourceKindSpec(
        SourceKind.CUSTOMER_INTERVIEW,
        "Customer interview",
        "A specific conversation with a real or prospective customer.",
        "Interview 2026-04-12 with neurosurgeon Dr. X",
    ),
    SourceKindSpec(
        SourceKind.MARKET_DATA,
        "Market data",
        "Third-party market research or public statistics.",
        "IMV Medical Information Division MRI report 2025",
    ),
    SourceKindSpec(
        SourceKind.CITATION,
        "Citation",
        "A book, paper, talk, or article.",
        "Norman, The Design of Everyday Things",
    ),
    SourceKindSpec(
        SourceKind.FOUNDER_VISION,
        "Founder vision",
        "A documented thesis from a company founder or principal.",
        "Founder vision 2026: workflow-time is the surgical bottleneck",
    ),
    SourceKindSpec(
        SourceKind.DOMAIN_EXPERTISE,
        "Domain expertise",
        "Documented expertise of a named team member.",
        "20 years operating-room exposure, neurosurgical procedures",
    ),
    SourceKindSpec(
        SourceKind.STRATEGIC_THESIS,
        "Strategic thesis",
        "A bet about the market that the company is making.",
        "We believe surgeons adopt robotics if procedure time drops 30%",
    ),
    SourceKindSpec(
        SourceKind.INTERNAL_DATA,
        "Internal data",
        "Internal telemetry, user data, or observed product behavior.",
        "Q1 2026 user activity log, 14-day cohort",
    ),
    SourceKindSpec(
        SourceKind.PRIOR_INTERNAL_DOC,
        "Prior internal document",
        "An existing internal document being ingested.",
        "Project Initiation Document, drafted 2025-Q3",
    ),
    SourceKindSpec(
        SourceKind.SKILL_OUTPUT,
        "Skill output",
        "The output of another Claude Code skill, ingested via atomize. Requires a ``producing_skill`` field.",
        "competitor-profiling output for Competitor X",
    ),
    SourceKindSpec(
        SourceKind.PRESS_RELEASE,
        "Press release",
        "Date-stamped corporate announcement.",
        "Acme Medical press release 2026-02-14",
    ),
    SourceKindSpec(
        SourceKind.WEB_SNAPSHOT,
        "Web snapshot",
        "Page captured at a moment in time (HTML, screenshot, or both).",
        "acme-medical.com/products/cardiac-monitor on 2026-05-20",
    ),
    SourceKindSpec(
        SourceKind.WEB_SNAPSHOT_NETWORK,
        "Web snapshot — network",
        "List of network requests from a captured page; tech-stack intel.",
        "Network manifest for acme-medical.com homepage",
    ),
    SourceKindSpec(
        SourceKind.FDA_510K_SUMMARY,
        "FDA 510(k) summary",
        "The public PDF summary for a 510(k) clearance.",
        "K223456 summary PDF",
    ),
    SourceKindSpec(
        SourceKind.REGULATORY_FILING,
        "Regulatory filing",
        "Broader bucket for non-510(k) regulatory documents.",
        "CE Technical File summary, MDR public report",
    ),
)


SOURCE_KINDS_BY_VALUE: dict[str, SourceKindSpec] = {spec.kind.value: spec for spec in SOURCE_KIND_SPECS}


def get_source_kind(value: str) -> SourceKindSpec | None:
    """Look up a source-kind spec by its stable string value."""

    return SOURCE_KINDS_BY_VALUE.get(value)
