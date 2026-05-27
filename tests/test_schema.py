"""Schema registry sanity tests.

These tests verify the in-process schema is internally consistent. They run on
every CI build and act as a tripwire when someone edits a registry by hand and
misses a cross-reference.
"""

from __future__ import annotations


from company_brain.schema import (
    BASE_REQUIRED_FIELDS,
    EDGE_TYPE_SPECS,
    NODE_TYPE_SPECS,
    NODE_TYPES,
    PROFILE_SPECS,
    SOURCE_KIND_SPECS,
    FieldType,
    NodeCategory,
    SourceKind,
    base_field_names,
    check_registry_consistency,
    get_active_node_types,
    get_edge_type,
    get_node_type,
    get_profile,
    get_source_kind,
)


# ---------------------------------------------------------------------------
# Registry-wide consistency.
# ---------------------------------------------------------------------------


def test_registry_consistency_returns_no_issues() -> None:
    issues = check_registry_consistency()
    assert issues == (), f"schema is inconsistent: {issues!r}"


# ---------------------------------------------------------------------------
# Node types.
# ---------------------------------------------------------------------------


def test_node_type_names_are_unique() -> None:
    names = [spec.name for spec in NODE_TYPE_SPECS]
    assert len(names) == len(set(names)), "duplicate node type names"


def test_node_type_folders_are_unique() -> None:
    folders = [spec.folder for spec in NODE_TYPE_SPECS]
    assert len(folders) == len(set(folders)), "duplicate node type folders"


def test_every_node_type_in_registry_is_in_specs() -> None:
    assert set(NODE_TYPES.keys()) == {s.name for s in NODE_TYPE_SPECS}


def test_get_node_type_returns_none_for_unknown() -> None:
    assert get_node_type("nonexistent") is None


def test_get_node_type_round_trip() -> None:
    spec = get_node_type("pillar")
    assert spec is not None
    assert spec.name == "pillar"
    assert spec.category == NodeCategory.EPISTEMIC


def test_profile_conditional_types_declare_their_profile() -> None:
    for spec in NODE_TYPE_SPECS:
        if spec.category == NodeCategory.PROFILE_CONDITIONAL:
            assert spec.profile is not None, f"{spec.name} is profile-conditional but declares no profile"


def test_non_profile_conditional_types_have_no_profile() -> None:
    for spec in NODE_TYPE_SPECS:
        if spec.category != NodeCategory.PROFILE_CONDITIONAL:
            assert spec.profile is None, f"{spec.name} should not declare a profile"


def test_medical_device_profile_activates_expected_types() -> None:
    expected = {
        "indication-for-use",
        "regulatory-clearance",
        "risk-insight",
        "hazard",
        "hazardous-situation",
        "harm",
        "risk-control-idea",
        "regulation",
        "standard",
    }
    actual = {s.name for s in NODE_TYPE_SPECS if s.profile == "medical-device"}
    assert actual == expected


# ---------------------------------------------------------------------------
# get_active_node_types
# ---------------------------------------------------------------------------


def test_get_active_node_types_default_excludes_meddev() -> None:
    active = {s.name for s in get_active_node_types(None)}
    assert "indication-for-use" not in active
    assert "regulatory-clearance" not in active
    # But always-available types are present.
    assert "pillar" in active
    assert "product" in active


def test_get_active_node_types_medical_device_includes_meddev() -> None:
    active = {s.name for s in get_active_node_types("medical-device")}
    assert "indication-for-use" in active
    assert "regulatory-clearance" in active
    assert "hazard" in active
    assert "pillar" in active  # epistemic still there


def test_get_active_node_types_unknown_profile_acts_like_default() -> None:
    active = {s.name for s in get_active_node_types("not-a-real-profile")}
    assert "indication-for-use" not in active
    assert "pillar" in active


# ---------------------------------------------------------------------------
# Edge types.
# ---------------------------------------------------------------------------


def test_edge_type_count_is_ten() -> None:
    assert len(EDGE_TYPE_SPECS) == 10


def test_edge_type_names_are_unique() -> None:
    names = [spec.name for spec in EDGE_TYPE_SPECS]
    assert len(names) == len(set(names))


def test_preceded_by_and_followed_by_are_inverse() -> None:
    p = get_edge_type("preceded_by")
    f = get_edge_type("followed_by")
    assert p is not None and f is not None
    assert p.inverse == "followed_by"
    assert f.inverse == "preceded_by"


def test_edge_weights_in_range() -> None:
    for spec in EDGE_TYPE_SPECS:
        assert 0.0 <= spec.default_weight <= 1.0, f"{spec.name} weight out of range"


def test_get_edge_type_returns_none_for_unknown() -> None:
    assert get_edge_type("imaginary_edge") is None


# ---------------------------------------------------------------------------
# Source kinds.
# ---------------------------------------------------------------------------


def test_source_kind_count_is_fourteen() -> None:
    assert len(SOURCE_KIND_SPECS) == 14


def test_source_kind_values_match_enum() -> None:
    enum_values = {k.value for k in SourceKind}
    spec_values = {s.kind.value for s in SOURCE_KIND_SPECS}
    assert enum_values == spec_values


def test_get_source_kind_round_trip() -> None:
    spec = get_source_kind("founder-vision")
    assert spec is not None
    assert spec.kind == SourceKind.FOUNDER_VISION


def test_get_source_kind_returns_none_for_unknown() -> None:
    assert get_source_kind("not-a-kind") is None


# ---------------------------------------------------------------------------
# Profiles.
# ---------------------------------------------------------------------------


def test_profile_names_are_unique() -> None:
    names = [p.name for p in PROFILE_SPECS]
    assert len(names) == len(set(names))


def test_default_profile_exists() -> None:
    p = get_profile("default")
    assert p is not None
    assert not p.appends_controlled_document_footer


def test_medical_device_profile_appends_footer() -> None:
    p = get_profile("medical-device")
    assert p is not None
    assert p.appends_controlled_document_footer is True


def test_medical_device_profile_activates_node_types() -> None:
    p = get_profile("medical-device")
    assert p is not None
    assert "indication-for-use" in p.activated_node_type_names
    assert "regulatory-clearance" in p.activated_node_type_names


def test_reserved_profiles_have_no_activated_types() -> None:
    for name in ("saas", "hardware", "services"):
        p = get_profile(name)
        assert p is not None, f"{name} profile slot missing"
        assert p.activated_node_type_names == (), f"{name} should activate no types in v1"


# ---------------------------------------------------------------------------
# Frontmatter.
# ---------------------------------------------------------------------------


def test_base_required_fields_include_core_set() -> None:
    names = base_field_names()
    for required in (
        "id",
        "title",
        "type",
        "namespace",
        "summary",
        "confidence",
        "verified_at",
        "edges",
        "controlled_document",
    ):
        assert required in names, f"{required} missing from base required fields"


def test_primary_is_an_optional_base_boolean_field() -> None:
    # `primary` flags the representative node of a (type, namespace) set for
    # the doc-generate selection logic. It is optional so pre-v0.8.0 vaults
    # render unchanged.
    primary_spec = next((f for f in BASE_REQUIRED_FIELDS if f.name == "primary"), None)
    assert primary_spec is not None, "primary missing from BASE_REQUIRED_FIELDS"
    assert primary_spec.type == FieldType.BOOLEAN
    assert primary_spec.required is False
    assert primary_spec.default is False


def test_extra_required_field_names_dont_collide_with_base() -> None:
    base = base_field_names()
    for spec in NODE_TYPE_SPECS:
        for field_spec in spec.extra_required_fields:
            assert (
                field_spec.name not in base
            ), f"node type {spec.name} declares extra field {field_spec.name} that shadows base"


# ---------------------------------------------------------------------------
# Convenience: schema counts smoke test, to catch accidental deletions.
# ---------------------------------------------------------------------------


def test_node_type_category_counts() -> None:
    counts = {category: 0 for category in NodeCategory}
    for spec in NODE_TYPE_SPECS:
        counts[spec.category] += 1
    assert counts[NodeCategory.EPISTEMIC] == 10
    assert counts[NodeCategory.ENTITY] == 11
    assert counts[NodeCategory.PROFILE_CONDITIONAL] == 9
