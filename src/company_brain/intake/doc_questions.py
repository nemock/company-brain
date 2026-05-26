"""Document-driven intake: question manifests + gap detection.

The ``intake for-doc <doc>`` sub-mode reads a YAML manifest that declares the
sections of a target document, what node types each section consumes, and what
questions to ask. Gap detection walks the vault and classifies every section
as ``complete`` / ``partial`` / ``empty`` so the interview can skip what's
already populated and focus on what's missing.

Manifests live next to this module under ``manifests/<doc>.yaml`` and ship
with the wheel via the hatchling force-include in ``pyproject.toml``.

Public API:

* :func:`load_manifest` — load and validate a manifest by doc name.
* :func:`list_manifests` — list available doc names.
* :func:`filter_for_profile` — drop sections gated by an inactive profile.
* :func:`compute_gaps` — per-section gap analysis against a loaded vault.
* :func:`manifest_to_dict`, :func:`gaps_to_dict` — JSON serialization helpers
  for the CLI layer.
* :class:`UnknownDocError`, :class:`ManifestError` — typed errors.

Nothing here writes. Node writes are the LLM's job, mediated by the
``intake`` skill instructions.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from ..schema import NODE_TYPES, PROFILES
from ..vault import Node, Vault


_MANIFESTS_DIR = Path(__file__).parent / "manifests"


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class DocQuestionsError(Exception):
    """Base class for errors raised by this module."""


class UnknownDocError(DocQuestionsError):
    """No manifest registered for the requested doc name."""


class ManifestError(DocQuestionsError):
    """A manifest file is malformed."""


# ---------------------------------------------------------------------------
# Manifest data classes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FeedsFrom:
    """One node-type slot a section consumes.

    ``role`` is a type-specific discriminator interpreted by
    :func:`_matches_role`. For ``pillar`` it's ``positive`` / ``non-goal``.
    For ``decision`` it's ``rules-out``. For ``requirement`` it's the
    ``requirement_class`` value (``market``, ``user``, etc.). For ``source``
    it's the ``source_kind``. For other types ``role`` is ignored.
    """

    type: str
    role: str | None
    min: int


@dataclass(frozen=True)
class Question:
    """One question in a section.

    ``captures`` is a list of node-type hints — the LLM uses these to
    type-classify what it extracts from the answer. The list is non-binding
    (the LLM may file strays into other sections' slots).
    """

    prompt: str
    captures: tuple[str, ...]


@dataclass(frozen=True)
class Section:
    """One section of a target document."""

    id: str
    title: str
    intent: str
    profile_required: str | None
    feeds_from: tuple[FeedsFrom, ...]
    questions: tuple[Question, ...]


@dataclass(frozen=True)
class Manifest:
    """A loaded document question manifest."""

    doc: str
    title: str
    intro: str
    sections: tuple[Section, ...]


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------


def list_manifests() -> list[str]:
    """Return the sorted list of doc names that have shipped manifests."""

    if not _MANIFESTS_DIR.is_dir():
        return []
    return sorted(p.stem for p in _MANIFESTS_DIR.glob("*.yaml"))


def load_manifest(doc_name: str) -> Manifest:
    """Load and validate a manifest by doc name.

    Raises :class:`UnknownDocError` if no manifest is registered.
    Raises :class:`ManifestError` on parse or validation failures.
    """

    path = _MANIFESTS_DIR / f"{doc_name}.yaml"
    if not path.is_file():
        known = list_manifests()
        raise UnknownDocError(
            f"no question manifest for doc '{doc_name}'. "
            f"Known: {', '.join(known) if known else '(none)'}"
        )
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ManifestError(f"YAML parse error in {path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise ManifestError(f"manifest {path} root is not a mapping")
    return _parse_manifest(raw, path)


def _parse_manifest(raw: dict[str, Any], path: Path) -> Manifest:
    def required(key: str) -> Any:
        if key not in raw:
            raise ManifestError(f"{path}: missing required field '{key}'")
        return raw[key]

    doc = str(required("doc"))
    title = str(required("title"))
    intro = str(raw.get("intro", "")).strip()
    sections_raw = required("sections")
    if not isinstance(sections_raw, list) or not sections_raw:
        raise ManifestError(f"{path}: 'sections' must be a non-empty list")

    sections: list[Section] = []
    seen_ids: set[str] = set()
    for idx, sec_raw in enumerate(sections_raw):
        if not isinstance(sec_raw, dict):
            raise ManifestError(f"{path}: section {idx} is not a mapping")
        section = _parse_section(sec_raw, idx, path)
        if section.id in seen_ids:
            raise ManifestError(f"{path}: duplicate section id '{section.id}'")
        seen_ids.add(section.id)
        sections.append(section)

    return Manifest(
        doc=doc,
        title=title,
        intro=intro,
        sections=tuple(sections),
    )


def _parse_section(raw: dict[str, Any], idx: int, path: Path) -> Section:
    def required(key: str) -> Any:
        if key not in raw:
            raise ManifestError(
                f"{path}: section {idx} missing required field '{key}'"
            )
        return raw[key]

    section_id = str(required("id"))
    title = str(required("title"))
    intent = str(raw.get("intent", "")).strip()

    profile_required = raw.get("profile_required")
    if profile_required is not None:
        profile_required = str(profile_required)
        if profile_required not in PROFILES:
            known = sorted(PROFILES)
            raise ManifestError(
                f"{path}: section '{section_id}' has unknown profile_required "
                f"'{profile_required}'. Known: {', '.join(known)}"
            )

    feeds_raw = raw.get("feeds_from", [])
    if not isinstance(feeds_raw, list):
        raise ManifestError(
            f"{path}: section '{section_id}' 'feeds_from' must be a list"
        )
    feeds: list[FeedsFrom] = []
    for fidx, f_raw in enumerate(feeds_raw):
        if not isinstance(f_raw, dict):
            raise ManifestError(
                f"{path}: section '{section_id}' feeds_from[{fidx}] is not a mapping"
            )
        ftype = str(f_raw.get("type", ""))
        if not ftype:
            raise ManifestError(
                f"{path}: section '{section_id}' feeds_from[{fidx}] missing 'type'"
            )
        if ftype not in NODE_TYPES:
            known = sorted(NODE_TYPES)
            raise ManifestError(
                f"{path}: section '{section_id}' feeds_from[{fidx}] has unknown "
                f"node type '{ftype}'. Known: {', '.join(known)}"
            )
        role_raw = f_raw.get("role")
        role = str(role_raw) if role_raw is not None else None

        min_raw = f_raw.get("min", 1)
        try:
            min_int = int(min_raw)
        except (TypeError, ValueError) as exc:
            raise ManifestError(
                f"{path}: section '{section_id}' feeds_from[{fidx}] 'min' "
                f"is not an integer: {min_raw!r}"
            ) from exc
        if min_int < 0:
            raise ManifestError(
                f"{path}: section '{section_id}' feeds_from[{fidx}] 'min' is negative"
            )
        feeds.append(FeedsFrom(type=ftype, role=role, min=min_int))

    questions_raw = raw.get("questions", [])
    if not isinstance(questions_raw, list):
        raise ManifestError(
            f"{path}: section '{section_id}' 'questions' must be a list"
        )
    questions: list[Question] = []
    for qidx, q_raw in enumerate(questions_raw):
        if not isinstance(q_raw, dict):
            raise ManifestError(
                f"{path}: section '{section_id}' questions[{qidx}] is not a mapping"
            )
        prompt = str(q_raw.get("prompt", "")).strip()
        if not prompt:
            raise ManifestError(
                f"{path}: section '{section_id}' questions[{qidx}] missing 'prompt'"
            )
        captures_raw = q_raw.get("captures", [])
        if not isinstance(captures_raw, list):
            raise ManifestError(
                f"{path}: section '{section_id}' questions[{qidx}] "
                "'captures' must be a list"
            )
        captures: tuple[str, ...] = tuple(str(c) for c in captures_raw)
        for cap in captures:
            # The capture hints may carry a dotted suffix (e.g.
            # "indication-for-use.population") to point at a specific field.
            # We validate the head against the node-type registry.
            head = cap.split(".", 1)[0]
            if head and head not in NODE_TYPES:
                raise ManifestError(
                    f"{path}: section '{section_id}' questions[{qidx}] "
                    f"captures '{cap}' references unknown node type '{head}'"
                )
        questions.append(Question(prompt=prompt, captures=captures))

    return Section(
        id=section_id,
        title=title,
        intent=intent,
        profile_required=profile_required,
        feeds_from=tuple(feeds),
        questions=tuple(questions),
    )


# ---------------------------------------------------------------------------
# Profile filtering
# ---------------------------------------------------------------------------


def filter_for_profile(manifest: Manifest, profile_name: str | None) -> Manifest:
    """Return a new manifest with sections gated by an inactive profile dropped.

    A section's ``profile_required`` of ``None`` means "always render."
    A non-None value means "only when the vault's active profile matches."
    """

    kept = tuple(
        s
        for s in manifest.sections
        if s.profile_required is None or s.profile_required == profile_name
    )
    return Manifest(
        doc=manifest.doc,
        title=manifest.title,
        intro=manifest.intro,
        sections=kept,
    )


# ---------------------------------------------------------------------------
# Gap detection
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SlotStatus:
    """The state of one ``feeds_from`` slot in a section."""

    type: str
    role: str | None
    min: int
    found_ids: tuple[str, ...]

    @property
    def count(self) -> int:
        return len(self.found_ids)

    @property
    def satisfied(self) -> bool:
        return self.count >= self.min


@dataclass(frozen=True)
class SectionGap:
    """Per-section gap analysis."""

    section_id: str
    title: str
    profile_required: str | None
    status: str  # complete | partial | empty
    slots: tuple[SlotStatus, ...]


def compute_gaps(manifest: Manifest, vault: Vault) -> list[SectionGap]:
    """Walk the vault and classify each section.

    * **complete** — every slot has ``count >= min``.
    * **empty** — every slot has ``count == 0``.
    * **partial** — at least one slot has nodes but at least one is below its
      ``min``.

    A section with no ``feeds_from`` slots is always **complete** — there's
    nothing for the interview to capture (such sections exist to let the
    manifest describe purely-rendered content; in practice the interview
    skips them).
    """

    gaps: list[SectionGap] = []
    nodes = vault.nodes

    for section in manifest.sections:
        slots: list[SlotStatus] = []
        for slot in section.feeds_from:
            matched = _match_slot(slot, nodes)
            slots.append(
                SlotStatus(
                    type=slot.type,
                    role=slot.role,
                    min=slot.min,
                    found_ids=tuple(sorted(n.id for n in matched)),
                )
            )

        if not slots:
            status = "complete"
        else:
            all_satisfied = all(s.satisfied for s in slots)
            any_present = any(s.count > 0 for s in slots)
            if all_satisfied:
                status = "complete"
            elif any_present:
                status = "partial"
            else:
                status = "empty"

        gaps.append(
            SectionGap(
                section_id=section.id,
                title=section.title,
                profile_required=section.profile_required,
                status=status,
                slots=tuple(slots),
            )
        )

    return gaps


def _match_slot(slot: FeedsFrom, nodes: list[Node]) -> list[Node]:
    """Filter nodes to those matching a ``feeds_from`` slot's type + role."""

    candidates = [n for n in nodes if n.type == slot.type]
    if slot.role is None:
        return candidates
    return [n for n in candidates if _matches_role(n, slot.type, slot.role)]


def _matches_role(node: Node, type_name: str, role: str) -> bool:
    """Apply the role discriminator for a node type.

    See :class:`FeedsFrom` for the role semantics by type.
    """

    if type_name == "pillar":
        is_non_goal = _is_non_goal_pillar(node)
        if role == "positive":
            return not is_non_goal
        if role == "non-goal":
            return is_non_goal
        return True

    if type_name == "decision":
        if role == "rules-out":
            return "## What This Rules Out" in node.body
        return True

    if type_name == "requirement":
        return str(node.frontmatter.get("requirement_class", "")) == role

    if type_name == "source":
        return str(node.frontmatter.get("source_kind", "")) == role

    return True


def _is_non_goal_pillar(node: Node) -> bool:
    """Mirror of ``render/mrd.py:_is_non_goal`` so gap detection and the MRD
    renderer agree on which pillars are non-goals.
    """

    tags = node.frontmatter.get("tags") or []
    if isinstance(tags, list) and any(str(t).lower() == "non-goal" for t in tags):
        return True
    title = str(node.frontmatter.get("title", "")).strip().lower()
    return title.startswith("non-goal")


# ---------------------------------------------------------------------------
# JSON serialization for the CLI layer
# ---------------------------------------------------------------------------


def manifest_to_dict(manifest: Manifest) -> dict[str, Any]:
    """Render a manifest as a JSON-friendly dict for CLI emission."""

    return {
        "doc": manifest.doc,
        "title": manifest.title,
        "intro": manifest.intro,
        "sections": [
            {
                "id": s.id,
                "title": s.title,
                "intent": s.intent,
                "profile_required": s.profile_required,
                "feeds_from": [
                    {"type": f.type, "role": f.role, "min": f.min}
                    for f in s.feeds_from
                ],
                "questions": [
                    {"prompt": q.prompt, "captures": list(q.captures)}
                    for q in s.questions
                ],
            }
            for s in manifest.sections
        ],
    }


def gaps_to_dict(gaps: list[SectionGap]) -> dict[str, Any]:
    """Render a gap report as a JSON-friendly dict for CLI emission.

    Includes a ``summary`` block counting sections by status, then a per-
    section breakdown with each slot's match count and satisfied flag.
    """

    summary: dict[str, int] = {"complete": 0, "partial": 0, "empty": 0}
    sections: list[dict[str, Any]] = []
    for gap in gaps:
        summary[gap.status] = summary.get(gap.status, 0) + 1
        sections.append(
            {
                "section_id": gap.section_id,
                "title": gap.title,
                "profile_required": gap.profile_required,
                "status": gap.status,
                "slots": [
                    {
                        "type": s.type,
                        "role": s.role,
                        "min": s.min,
                        "found_ids": list(s.found_ids),
                        "count": s.count,
                        "satisfied": s.satisfied,
                    }
                    for s in gap.slots
                ],
            }
        )
    return {"summary": summary, "sections": sections}


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
