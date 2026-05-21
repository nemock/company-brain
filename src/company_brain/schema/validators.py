"""Validator stubs.

Full validation logic lands in v0.1.0 step 4 (the ``cb validate`` command). For
now this module exposes the function signatures so other modules can import
them, plus a trivial registry-consistency check that the test suite uses.
"""

from __future__ import annotations

from dataclasses import dataclass

from .edge_types import EDGE_TYPES
from .node_types import NODE_TYPES
from .profiles import PROFILES
from .source_kinds import SOURCE_KINDS_BY_VALUE


@dataclass(frozen=True)
class SchemaIssue:
    """A single schema-consistency issue."""

    severity: str  # "error" | "warning"
    where: str
    message: str


def check_registry_consistency() -> tuple[SchemaIssue, ...]:
    """Validate the in-process schema is internally consistent.

    Checks:
      * Edge inverses reference real edge types and are mutually consistent.
      * Profile-conditional node types reference a profile that exists.
      * Folder paths are unique across node types.

    The test suite asserts that this returns no issues. Production code paths
    can also call this on import if we ever ship a runtime self-check.
    """

    issues: list[SchemaIssue] = []

    # Edge inverses.
    for spec in EDGE_TYPES.values():
        if spec.inverse is None:
            continue
        partner = EDGE_TYPES.get(spec.inverse)
        if partner is None:
            issues.append(
                SchemaIssue(
                    "error",
                    f"edge_types/{spec.name}",
                    f"inverse '{spec.inverse}' does not resolve to a registered edge type",
                )
            )
            continue
        if partner.inverse != spec.name:
            issues.append(
                SchemaIssue(
                    "error",
                    f"edge_types/{spec.name}",
                    f"asymmetric inverse: {spec.name}.inverse={spec.inverse} but {partner.name}.inverse={partner.inverse}",
                )
            )

    # Node-type profile references.
    for spec in NODE_TYPES.values():
        if spec.profile is None:
            continue
        if spec.profile not in PROFILES:
            issues.append(
                SchemaIssue(
                    "error",
                    f"node_types/{spec.name}",
                    f"profile '{spec.profile}' does not resolve to a registered profile",
                )
            )

    # Folder path collisions.
    seen_folders: dict[str, str] = {}
    for spec in NODE_TYPES.values():
        if spec.folder in seen_folders:
            issues.append(
                SchemaIssue(
                    "error",
                    f"node_types/{spec.name}",
                    f"folder '{spec.folder}' collides with '{seen_folders[spec.folder]}'",
                )
            )
        else:
            seen_folders[spec.folder] = spec.name

    # Sanity: source kinds non-empty.
    if not SOURCE_KINDS_BY_VALUE:
        issues.append(SchemaIssue("error", "source_kinds", "no source kinds registered"))

    return tuple(issues)
