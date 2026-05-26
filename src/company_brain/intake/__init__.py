"""Intake helpers — document-driven interview support.

The classic intake sub-modes (``vision``, ``persona``, ``competitor``, …) live
in the intake skill's SKILL.md. The Python side just exposes read-only
helpers so the LLM can stay aligned with the schema and the active vault.

This package currently ships the document-driven intake helpers
(:mod:`.doc_questions`): question manifests + gap detection that the
``for-doc`` sub-mode consumes.
"""

from .doc_questions import (
    DocQuestionsError,
    FeedsFrom,
    Manifest,
    ManifestError,
    Question,
    Section,
    SectionGap,
    SlotStatus,
    UnknownDocError,
    compute_gaps,
    filter_for_profile,
    gaps_to_dict,
    list_manifests,
    load_manifest,
    manifest_to_dict,
)

__all__ = [
    "DocQuestionsError",
    "UnknownDocError",
    "ManifestError",
    "FeedsFrom",
    "Question",
    "Section",
    "Manifest",
    "SlotStatus",
    "SectionGap",
    "list_manifests",
    "load_manifest",
    "filter_for_profile",
    "compute_gaps",
    "manifest_to_dict",
    "gaps_to_dict",
]
