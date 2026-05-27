"""Vault validation.

Loads a company-brain vault from disk, parses every node markdown file's
frontmatter, and runs the checks documented in PRD §14:

* Broken edges (target id does not resolve)
* Missing required frontmatter fields (base + per-type)
* Duplicate node ids
* Unknown / inactive node types for the active profile
* Type vs. folder mismatch
* Filename vs. id mismatch
* Sources missing ``source_kind``
* Requirements missing ``requirement_class``
* Metrics missing ``volatility_class``
* Competitors missing ``legal_name`` / ``canonical_url``
* IFU nodes missing structured fields
* Regulatory-clearance nodes missing structured fields
* Web-snapshot sources missing url/captured_at/attachment
* Time-series facts (with ``metric_id``) whose metric does not resolve
* Nodes in ``risk/`` or ``indications-for-use/`` without
  ``controlled_document: false``
* Edge ``type`` not in the registered edge set
* Edge ``weight`` outside ``[0, 1]``

The companion auto-fix (missing inverse edges, INDEX.md rebuild) lands in
v0.4.0 with the ``maintain`` skill. ``cb validate --fix`` is a stub here.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .schema import (
    EDGE_TYPES,
    NodeTypeSpec,
    get_active_node_types,
    get_node_type,
)
from .vault import Node, Vault, VaultNotFoundError, load_vault


# Re-exported so existing callers (CLI, tests) keep working.
__all__ = [
    "Node",
    "Vault",
    "VaultNotFoundError",
    "ValidationIssue",
    "validate",
    "summarize",
]


@dataclass(frozen=True)
class ValidationIssue:
    """One finding from the validator."""

    severity: str  # "error" | "warning" | "info"
    code: str
    message: str
    node_id: str | None = None
    path: Path | None = None
    fixable: bool = False


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


_BASE_REQUIRED_FIELDS: tuple[str, ...] = (
    "id",
    "title",
    "type",
    "namespace",
    "summary",
    "auto_inject",
    "confidence",
    "verified_at",
    "verified_by",
    "edges",
    "controlled_document",
)


_RISK_OR_IFU_FOLDERS = ("risk", "entities/indications-for-use")


def validate(vault_path: Path, *, strict: bool = False) -> list[ValidationIssue]:
    """Validate the vault at ``vault_path``. Return all issues found.

    Does not raise on validation errors — the caller (CLI) decides exit code.
    Raises :class:`VaultNotFoundError` only when the path does not exist or
    doesn't have the basic shape of a vault.

    When ``strict`` is true, two additional warning checks fire around the
    ``primary`` frontmatter field (see :data:`PRIMARY_SELECTING_GENERATORS`):
    multiple primaries in the same ``(type, namespace)`` pair, and rendered
    output in ``exports/`` for a primary-selecting generator with no primary
    of the relevant type marked in the vault. Neither blocks the render.
    """

    vault = load_vault(vault_path)

    issues: list[ValidationIssue] = []
    issues.extend(_check_profile(vault))
    issues.extend(_check_duplicate_ids(vault))
    for node in vault.nodes:
        issues.extend(_check_node(node, vault))
    if strict:
        issues.extend(_check_multiple_primaries_per_namespace(vault))
        issues.extend(_check_exports_imply_primary(vault))
    return issues


# ---------------------------------------------------------------------------
# Vault-wide checks
# ---------------------------------------------------------------------------


def _check_profile(vault: Vault) -> list[ValidationIssue]:
    if vault.profile_name is None:
        return [
            ValidationIssue(
                "error",
                "profile-missing",
                "Vault's _system/PROFILE.md has no `profile` field.",
                path=vault.path / "_system" / "PROFILE.md",
            )
        ]
    from .schema import get_profile

    if get_profile(vault.profile_name) is None:
        return [
            ValidationIssue(
                "error",
                "profile-unknown",
                f"Vault declares unknown profile '{vault.profile_name}'.",
                path=vault.path / "_system" / "PROFILE.md",
            )
        ]
    return []


def _check_duplicate_ids(vault: Vault) -> list[ValidationIssue]:
    seen: dict[str, list[Node]] = {}
    for node in vault.nodes:
        seen.setdefault(node.id, []).append(node)
    issues: list[ValidationIssue] = []
    for node_id, nodes in seen.items():
        if not node_id:
            continue
        if len(nodes) > 1:
            for node in nodes:
                issues.append(
                    ValidationIssue(
                        "error",
                        "duplicate-id",
                        f"Node id '{node_id}' appears in {len(nodes)} files.",
                        node_id=node_id,
                        path=node.path,
                    )
                )
    return issues


# ---------------------------------------------------------------------------
# Per-node checks
# ---------------------------------------------------------------------------


def _check_node(node: Node, vault: Vault) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues.extend(_check_base_required_fields(node))

    spec = get_node_type(node.type)
    if spec is None:
        issues.append(
            ValidationIssue(
                "error",
                "unknown-type",
                f"Node declares type '{node.type}' which is not a registered node type.",
                node_id=node.id,
                path=node.path,
            )
        )
        # Without a spec, we can't do type-specific checks.
        return issues

    issues.extend(_check_type_active_for_profile(node, spec, vault))
    issues.extend(_check_filename_matches_id(node))
    issues.extend(_check_folder_matches_type(node, spec))
    issues.extend(_check_type_specific_required_fields(node, spec))
    issues.extend(_check_source_kind(node, spec))
    issues.extend(_check_controlled_document_for_risk_or_ifu(node, spec))
    issues.extend(_check_metric_id_resolves(node, spec, vault))
    issues.extend(_check_belongs_to_product_resolves(node, spec, vault))
    issues.extend(_check_edges(node, vault))
    return issues


def _check_base_required_fields(node: Node) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for fname in _BASE_REQUIRED_FIELDS:
        if fname not in node.frontmatter:
            issues.append(
                ValidationIssue(
                    "error",
                    "missing-base-field",
                    f"Node missing required base frontmatter field `{fname}`.",
                    node_id=node.id or None,
                    path=node.path,
                )
            )
    return issues


def _check_type_active_for_profile(
    node: Node, spec: NodeTypeSpec, vault: Vault
) -> list[ValidationIssue]:
    active = {s.name for s in get_active_node_types(vault.profile_name)}
    if spec.name not in active:
        return [
            ValidationIssue(
                "error",
                "type-inactive-for-profile",
                f"Node type '{spec.name}' is not active for the vault's profile '{vault.profile_name}'.",
                node_id=node.id,
                path=node.path,
            )
        ]
    return []


def _check_filename_matches_id(node: Node) -> list[ValidationIssue]:
    expected_stem = node.id
    actual_stem = node.path.stem
    if expected_stem and actual_stem != expected_stem:
        return [
            ValidationIssue(
                "warning",
                "filename-id-mismatch",
                f"Node id '{node.id}' does not match filename '{actual_stem}.md'.",
                node_id=node.id,
                path=node.path,
            )
        ]
    return []


def _check_folder_matches_type(node: Node, spec: NodeTypeSpec) -> list[ValidationIssue]:
    expected_folder = spec.folder.replace("/", "/")
    actual_folder = str(node.path.parent).replace("\\", "/")
    if actual_folder != expected_folder:
        return [
            ValidationIssue(
                "error",
                "folder-type-mismatch",
                (
                    f"Node type '{spec.name}' should live in '{spec.folder}/' "
                    f"but file is in '{actual_folder}/'."
                ),
                node_id=node.id,
                path=node.path,
            )
        ]
    return []


def _check_type_specific_required_fields(
    node: Node, spec: NodeTypeSpec
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for field_spec in spec.extra_required_fields:
        if field_spec.name not in node.frontmatter or node.frontmatter[field_spec.name] in (
            None,
            "",
        ):
            issues.append(
                ValidationIssue(
                    "error",
                    "missing-type-field",
                    f"Node type '{spec.name}' requires frontmatter field `{field_spec.name}`.",
                    node_id=node.id,
                    path=node.path,
                )
            )
    return issues


_VALID_REQUIREMENT_CLASSES = frozenset({"market", "user", "system", "software", "hardware"})
_VALID_VOLATILITY_CLASSES = frozenset({"low", "medium", "high"})


def _check_source_kind(node: Node, spec: NodeTypeSpec) -> list[ValidationIssue]:
    """Constrained-value checks for fields with a fixed vocabulary."""

    issues: list[ValidationIssue] = []
    if spec.name == "source":
        sk = node.frontmatter.get("source_kind")
        # Missing source_kind is caught by type-specific required check;
        # here we only check unknown values.
        if sk is not None:
            from .schema import get_source_kind

            if get_source_kind(str(sk)) is None:
                issues.append(
                    ValidationIssue(
                        "error",
                        "unknown-source-kind",
                        f"source node has unknown source_kind '{sk}'.",
                        node_id=node.id,
                        path=node.path,
                    )
                )
    if spec.name == "requirement":
        rc = node.frontmatter.get("requirement_class")
        if rc is not None and str(rc) not in _VALID_REQUIREMENT_CLASSES:
            issues.append(
                ValidationIssue(
                    "error",
                    "invalid-requirement-class",
                    f"requirement node has invalid requirement_class '{rc}' "
                    f"(must be one of {sorted(_VALID_REQUIREMENT_CLASSES)}).",
                    node_id=node.id,
                    path=node.path,
                )
            )
    if spec.name == "metric":
        vc = node.frontmatter.get("volatility_class")
        if vc is not None and str(vc) not in _VALID_VOLATILITY_CLASSES:
            issues.append(
                ValidationIssue(
                    "error",
                    "invalid-volatility-class",
                    f"metric node has invalid volatility_class '{vc}' "
                    f"(must be one of {sorted(_VALID_VOLATILITY_CLASSES)}).",
                    node_id=node.id,
                    path=node.path,
                )
            )
    return issues


def _check_controlled_document_for_risk_or_ifu(
    node: Node, spec: NodeTypeSpec
) -> list[ValidationIssue]:
    """Risk and IFU nodes must declare controlled_document: false."""

    if not _is_risk_or_ifu(spec):
        return []
    cd = node.frontmatter.get("controlled_document")
    if cd is not False:
        return [
            ValidationIssue(
                "error",
                "risk-or-ifu-must-declare-controlled-document-false",
                (
                    f"Node type '{spec.name}' lives in the planning / controlled-document-boundary "
                    "subtree and must declare `controlled_document: false`."
                ),
                node_id=node.id,
                path=node.path,
            )
        ]
    return []


def _is_risk_or_ifu(spec: NodeTypeSpec) -> bool:
    folder = spec.folder.replace("\\", "/")
    return folder.startswith("risk/") or folder == "entities/indications-for-use"


def _check_metric_id_resolves(
    node: Node, spec: NodeTypeSpec, vault: Vault
) -> list[ValidationIssue]:
    """If a fact carries metric_id, it must resolve to an existing metric node."""

    if spec.name != "fact":
        return []
    metric_id = node.frontmatter.get("metric_id")
    if not metric_id:
        return []
    target = vault.nodes_by_id.get(str(metric_id))
    if target is None:
        return [
            ValidationIssue(
                "error",
                "metric-id-unresolved",
                f"fact references metric_id '{metric_id}' but no node with that id exists.",
                node_id=node.id,
                path=node.path,
            )
        ]
    if target.type != "metric":
        return [
            ValidationIssue(
                "error",
                "metric-id-wrong-type",
                f"fact references metric_id '{metric_id}' but that node is a '{target.type}', not a 'metric'.",
                node_id=node.id,
                path=node.path,
            )
        ]
    return []


def _check_belongs_to_product_resolves(
    node: Node, spec: NodeTypeSpec, vault: Vault
) -> list[ValidationIssue]:
    """IFU nodes' belongs_to_product must point at a product node."""

    if spec.name != "indication-for-use":
        return []
    target_id = node.frontmatter.get("belongs_to_product")
    if not target_id:
        return []
    target = vault.nodes_by_id.get(str(target_id))
    if target is None:
        return [
            ValidationIssue(
                "error",
                "belongs-to-product-unresolved",
                f"indication-for-use belongs_to_product '{target_id}' does not resolve.",
                node_id=node.id,
                path=node.path,
            )
        ]
    if target.type != "product":
        return [
            ValidationIssue(
                "warning",
                "belongs-to-product-wrong-type",
                f"indication-for-use belongs_to_product '{target_id}' points at a '{target.type}', not a 'product'.",
                node_id=node.id,
                path=node.path,
            )
        ]
    return []


def _check_edges(node: Node, vault: Vault) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for edge in node.edges:
        if edge.type not in EDGE_TYPES:
            issues.append(
                ValidationIssue(
                    "error",
                    "unknown-edge-type",
                    f"Edge from '{node.id}' has unknown type '{edge.type}'.",
                    node_id=node.id,
                    path=node.path,
                )
            )
        if not (0.0 <= edge.weight <= 1.0):
            issues.append(
                ValidationIssue(
                    "error",
                    "edge-weight-out-of-range",
                    f"Edge from '{node.id}' to '{edge.target}' has weight {edge.weight} (must be in [0, 1]).",
                    node_id=node.id,
                    path=node.path,
                )
            )
        if edge.target and edge.target not in vault.nodes_by_id:
            issues.append(
                ValidationIssue(
                    "error",
                    "edge-target-unresolved",
                    f"Edge from '{node.id}' targets '{edge.target}', which is not an id in this vault.",
                    node_id=node.id,
                    path=node.path,
                    fixable=False,
                )
            )
    return issues


# ---------------------------------------------------------------------------
# --strict checks for the `primary` frontmatter field
# ---------------------------------------------------------------------------


# Generators that pick a single representative node of a given type. Keyed by
# the export filename stem; value is the node type whose primary marking the
# generator consults. Sales-battle-card stems may include a competitor suffix
# (e.g. ``sales-battle-card-competitor-gbrain.md``); see _exports_for_stem.
PRIMARY_SELECTING_GENERATORS: dict[str, str] = {
    "one-pager": "persona",
    "mrd": "persona",
    "sales-battle-card": "competitor",
    "press-release": "product",
    "onboarding-doc": "persona",
}


def _is_primary(node: Node) -> bool:
    return bool(node.frontmatter.get("primary"))


def _check_multiple_primaries_per_namespace(vault: Vault) -> list[ValidationIssue]:
    """Warn when more than one node of the same (type, namespace) is primary.

    The render still produces deterministic output (alphabetical among the
    primaries) with a footer note; this is a soft signal that the vault
    author probably means to demote one of them.
    """

    buckets: dict[tuple[str, str], list[Node]] = {}
    for node in vault.nodes:
        if not _is_primary(node):
            continue
        key = (node.type, str(node.frontmatter.get("namespace", "")))
        buckets.setdefault(key, []).append(node)

    issues: list[ValidationIssue] = []
    for (type_name, namespace), nodes in buckets.items():
        if len(nodes) < 2:
            continue
        ids = sorted(n.id for n in nodes)
        for node in nodes:
            issues.append(
                ValidationIssue(
                    "warning",
                    "multiple-primaries",
                    (
                        f"{len(nodes)} '{type_name}' nodes in namespace "
                        f"'{namespace}' are marked primary ({', '.join(ids)}). "
                        "Generators will pick the alphabetically-first id; "
                        "demote the others to silence this warning."
                    ),
                    node_id=node.id,
                    path=node.path,
                )
            )
    return issues


def _check_exports_imply_primary(vault: Vault) -> list[ValidationIssue]:
    """Warn when a generator with primary-entity selection has rendered output
    in ``exports/`` but no entity of the relevant type is marked primary.

    Inferred by filename stem. Sales-battle-card may carry a competitor id
    suffix; we strip it before matching.
    """

    exports_dir = vault.path / "exports"
    if not exports_dir.is_dir():
        return []

    # Collect stems of rendered docs. We only care about the markdown source
    # of truth; the html/docx mirrors carry the same selection signal.
    rendered_stems: set[str] = set()
    for export in exports_dir.iterdir():
        if not export.is_file() or export.suffix != ".md":
            continue
        rendered_stems.add(export.stem)

    # Per-type set of namespaces with a primary marked. Empty set means no
    # primary anywhere for that type.
    primary_namespaces_by_type: dict[str, set[str]] = {}
    for node in vault.nodes:
        if not _is_primary(node):
            continue
        primary_namespaces_by_type.setdefault(node.type, set()).add(
            str(node.frontmatter.get("namespace", ""))
        )

    issues: list[ValidationIssue] = []
    for stem in sorted(rendered_stems):
        generator = _generator_for_stem(stem)
        if generator is None:
            continue
        type_name = PRIMARY_SELECTING_GENERATORS[generator]
        # Skip if the vault has no entity of this type at all — the
        # generator will have produced a "no <type>" stub rather than
        # alphabetically picking the wrong one.
        candidates = [n for n in vault.nodes if n.type == type_name]
        if not candidates:
            continue
        if primary_namespaces_by_type.get(type_name):
            continue
        issues.append(
            ValidationIssue(
                "warning",
                "exports-no-primary",
                (
                    f"'{stem}.md' is rendered in exports/ but no '{type_name}' "
                    "node is marked primary; the generator fell back to "
                    "alphabetical-by-id. Mark one and re-render to silence."
                ),
                path=exports_dir / f"{stem}.md",
            )
        )
    return issues


def _generator_for_stem(stem: str) -> str | None:
    """Map an export filename stem back to a primary-selecting generator name.

    Handles the sales-battle-card-<competitor-id> filename convention.
    """

    if stem in PRIMARY_SELECTING_GENERATORS:
        return stem
    # sales-battle-card-<competitor-id>.md
    if stem.startswith("sales-battle-card-"):
        return "sales-battle-card"
    return None


# ---------------------------------------------------------------------------
# Convenience aggregations for the CLI
# ---------------------------------------------------------------------------


def summarize(issues: list[ValidationIssue]) -> dict[str, int]:
    """Return a per-severity count of issues."""

    out = {"error": 0, "warning": 0, "info": 0}
    for issue in issues:
        out[issue.severity] = out.get(issue.severity, 0) + 1
    return out
