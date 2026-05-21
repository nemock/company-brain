"""company-brain schema.

Single-sourced definitions for node types, edge types, source kinds, industry
profiles, and frontmatter. The vault-architect skill scaffolds folder trees
from this data; the validator (v0.1.0 step 4) checks vaults against it; the
doc-generate skill uses it for source-kind labeling.

Nothing in this package does I/O. Everything is data.
"""

from __future__ import annotations

from .edge_types import EDGE_TYPE_SPECS, EDGE_TYPES, EdgeTypeSpec, get_edge_type
from .frontmatter import BASE_REQUIRED_FIELDS, FieldSpec, FieldType, base_field_names
from .node_types import (
    NODE_TYPE_SPECS,
    NODE_TYPES,
    NodeCategory,
    NodeTypeSpec,
    get_active_node_types,
    get_node_type,
)
from .profiles import PROFILE_SPECS, PROFILES, Profile, get_profile
from .source_kinds import (
    SOURCE_KIND_SPECS,
    SOURCE_KINDS_BY_VALUE,
    SourceKind,
    SourceKindSpec,
    get_source_kind,
)
from .validators import SchemaIssue, check_registry_consistency

__all__ = [
    # Frontmatter
    "BASE_REQUIRED_FIELDS",
    "FieldSpec",
    "FieldType",
    "base_field_names",
    # Node types
    "NODE_TYPE_SPECS",
    "NODE_TYPES",
    "NodeCategory",
    "NodeTypeSpec",
    "get_active_node_types",
    "get_node_type",
    # Edge types
    "EDGE_TYPE_SPECS",
    "EDGE_TYPES",
    "EdgeTypeSpec",
    "get_edge_type",
    # Source kinds
    "SOURCE_KIND_SPECS",
    "SOURCE_KINDS_BY_VALUE",
    "SourceKind",
    "SourceKindSpec",
    "get_source_kind",
    # Profiles
    "PROFILE_SPECS",
    "PROFILES",
    "Profile",
    "get_profile",
    # Validators
    "SchemaIssue",
    "check_registry_consistency",
]
