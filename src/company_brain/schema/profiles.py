"""Industry profiles.

A profile is declared in ``_system/PROFILE.md`` of a vault and controls:

* which node-type folders the architect creates,
* which intake sub-modes are exposed,
* which scaffolds doc-generate makes available,
* which document sections are rendered (profile-conditional sections are
  omitted entirely when the profile doesn't enable them),
* whether the controlled-document footer is appended to generated documents.

v1 ships ``medical-device``. ``saas``, ``hardware``, ``services`` slots are
reserved (empty implementations).
"""

from __future__ import annotations

from dataclasses import dataclass

from .node_types import NODE_TYPE_SPECS


@dataclass(frozen=True)
class Profile:
    name: str
    description: str
    appends_controlled_document_footer: bool
    notes: tuple[str, ...] = ()

    @property
    def activated_node_type_names(self) -> tuple[str, ...]:
        """Names of profile-conditional node types this profile activates.

        Derived from :data:`NODE_TYPE_SPECS` so the schema stays single-sourced.
        """

        return tuple(spec.name for spec in NODE_TYPE_SPECS if spec.profile == self.name)


PROFILE_SPECS: tuple[Profile, ...] = (
    Profile(
        name="default",
        description="Industry-agnostic. Only the epistemic and entity node types are active.",
        appends_controlled_document_footer=False,
    ),
    Profile(
        name="medical-device",
        description=(
            "Adds indications-for-use, regulatory clearances, and ISO-14971-vocabulary risk node "
            "types. Every generated document carries the controlled-document-boundary footer."
        ),
        appends_controlled_document_footer=True,
        notes=(
            "All risk/ and indications-for-use nodes carry controlled_document: false.",
            "Predicate chains and IFU history use preceded_by / followed_by edges.",
        ),
    ),
    # Reserved slots. Activate-no-extra-types; intended for v1.x / v2 content.
    Profile(
        name="saas",
        description="Reserved. No additional node types in v1.",
        appends_controlled_document_footer=False,
        notes=("Content for this profile lands in v2.",),
    ),
    Profile(
        name="hardware",
        description="Reserved. No additional node types in v1.",
        appends_controlled_document_footer=False,
        notes=("Content for this profile lands in v2.",),
    ),
    Profile(
        name="services",
        description="Reserved. No additional node types in v1.",
        appends_controlled_document_footer=False,
        notes=("Content for this profile lands in v2.",),
    ),
)


PROFILES: dict[str, Profile] = {p.name: p for p in PROFILE_SPECS}


def get_profile(name: str) -> Profile | None:
    """Look up a profile by name."""

    return PROFILES.get(name)
