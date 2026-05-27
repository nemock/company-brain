"""Tests for the vault validator.

Two layers:

1. Regression: the committed example vault must validate with zero errors.
2. Unit-ish: scaffold a fresh vault, plant a deliberately-broken node, and
   assert the expected ValidationIssue.code shows up.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from company_brain.scaffold import scaffold
from company_brain.validator import (
    VaultNotFoundError,
    summarize,
    validate,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
MEDDEV_EXAMPLE = REPO_ROOT / "examples" / "meddev-fictional"


# ---------------------------------------------------------------------------
# Regression: example vault must validate
# ---------------------------------------------------------------------------


def test_meddev_fictional_example_validates_clean() -> None:
    """The committed example vault is the v0.1.0 step-4 done-when criterion."""

    issues = validate(MEDDEV_EXAMPLE)
    errors = [i for i in issues if i.severity == "error"]
    assert errors == [], f"example vault has errors: {errors!r}"


def test_meddev_fictional_summarize_zero_errors() -> None:
    counts = summarize(validate(MEDDEV_EXAMPLE))
    assert counts["error"] == 0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_empty_vault(tmp_path: Path, profile: str = "medical-device") -> Path:
    result = scaffold(tmp_path / "v", profile, init_git=False)
    return result.vault_path


def _write_pillar(
    vault: Path,
    *,
    node_id: str = "pillar-test-one",
    title: str = "Test Pillar",
    extra_frontmatter: str = "",
    edges: str = "edges: []",
    body: str = "\n# Test Pillar\n",
    folder: str = "pillars",
) -> Path:
    """Write a minimal-but-valid pillar node, with hooks to deliberately break it."""

    fm = f"""---
id: {node_id}
title: "{title}"
type: pillar
namespace: test
summary: "A pillar used to exercise the validator in tests."
auto_inject: false
applicable_when: null
confidence: 0.9
verified_at: 2026-05-21
verified_by: test
staleness_signal: null
tags: [test]
{edges}
related: []
source_url: null
controlled_document: false
{extra_frontmatter}---
"""
    path = vault / folder / f"{node_id}.md"
    path.write_text(fm + body, encoding="utf-8")
    return path


def _issue_codes(issues) -> set[str]:
    return {i.code for i in issues if i.severity == "error"}


# ---------------------------------------------------------------------------
# Vault-not-found and profile checks
# ---------------------------------------------------------------------------


def test_validate_raises_when_path_missing(tmp_path: Path) -> None:
    with pytest.raises(VaultNotFoundError):
        validate(tmp_path / "does-not-exist")


def test_validate_raises_when_no_profile_md(tmp_path: Path) -> None:
    bare = tmp_path / "bare"
    bare.mkdir()
    with pytest.raises(VaultNotFoundError):
        validate(bare)


# ---------------------------------------------------------------------------
# Per-node checks
# ---------------------------------------------------------------------------


def test_clean_pillar_produces_no_errors(tmp_path: Path) -> None:
    vault = _make_empty_vault(tmp_path)
    _write_pillar(vault)
    issues = validate(vault)
    assert _issue_codes(issues) == set()


def test_duplicate_id_is_error(tmp_path: Path) -> None:
    vault = _make_empty_vault(tmp_path)
    _write_pillar(vault, node_id="pillar-one")
    # Second file with the same id, different name. Will trigger
    # filename-id-mismatch on the second file but also duplicate-id.
    second = vault / "pillars" / "pillar-one-copy.md"
    second.write_text(
        (vault / "pillars" / "pillar-one.md").read_text(),
        encoding="utf-8",
    )
    issues = validate(vault)
    assert "duplicate-id" in _issue_codes(issues)


def test_unknown_node_type_is_error(tmp_path: Path) -> None:
    vault = _make_empty_vault(tmp_path)
    bad = vault / "pillars" / "pillar-bogus.md"
    bad.write_text(
        """---
id: pillar-bogus
title: "Bogus"
type: not-a-real-type
namespace: test
summary: "x"
auto_inject: false
confidence: 0.9
verified_at: 2026-05-21
verified_by: test
edges: []
controlled_document: false
---
""",
        encoding="utf-8",
    )
    issues = validate(vault)
    assert "unknown-type" in _issue_codes(issues)


def test_missing_base_field_is_error(tmp_path: Path) -> None:
    vault = _make_empty_vault(tmp_path)
    # Pillar without 'verified_at'.
    bad = vault / "pillars" / "pillar-incomplete.md"
    bad.write_text(
        """---
id: pillar-incomplete
title: "Incomplete"
type: pillar
namespace: test
summary: "x"
auto_inject: false
confidence: 0.9
verified_by: test
edges: []
controlled_document: false
---
""",
        encoding="utf-8",
    )
    issues = validate(vault)
    assert "missing-base-field" in _issue_codes(issues)


def test_filename_id_mismatch_is_warning(tmp_path: Path) -> None:
    vault = _make_empty_vault(tmp_path)
    # Write a pillar but to the wrong filename.
    _write_pillar(vault, node_id="pillar-mismatch")
    (vault / "pillars" / "pillar-mismatch.md").rename(
        vault / "pillars" / "pillar-different-name.md"
    )
    issues = validate(vault)
    warnings = [i for i in issues if i.severity == "warning"]
    codes = {i.code for i in warnings}
    assert "filename-id-mismatch" in codes


def test_folder_type_mismatch_is_error(tmp_path: Path) -> None:
    vault = _make_empty_vault(tmp_path)
    # A pillar file placed in the decisions/ folder.
    _write_pillar(vault, node_id="pillar-misplaced", folder="decisions")
    issues = validate(vault)
    assert "folder-type-mismatch" in _issue_codes(issues)


def test_type_inactive_for_profile_is_error(tmp_path: Path) -> None:
    vault = _make_empty_vault(tmp_path, profile="default")
    # indication-for-use is medical-device-only, but we'll place one anyway.
    # First we need to create the folder (default profile doesn't scaffold it).
    folder = vault / "entities" / "indications-for-use"
    folder.mkdir(parents=True)
    (folder / "indication-for-use-orphan.md").write_text(
        """---
id: indication-for-use-orphan
title: "Orphan IFU"
type: indication-for-use
namespace: test
summary: "Should not exist under default profile."
auto_inject: false
confidence: 0.9
verified_at: 2026-05-21
verified_by: test
edges: []
controlled_document: false
population: "x"
condition: "x"
intervention: "x"
setting: "x"
belongs_to_product: nonexistent
---
""",
        encoding="utf-8",
    )
    issues = validate(vault)
    assert "type-inactive-for-profile" in _issue_codes(issues)


def test_source_without_source_kind_is_error(tmp_path: Path) -> None:
    vault = _make_empty_vault(tmp_path)
    (vault / "sources" / "source-no-kind.md").write_text(
        """---
id: source-no-kind
title: "Source"
type: source
namespace: test
summary: "Source missing source_kind."
auto_inject: false
confidence: 0.9
verified_at: 2026-05-21
verified_by: test
edges: []
controlled_document: false
---
""",
        encoding="utf-8",
    )
    issues = validate(vault)
    assert "missing-type-field" in _issue_codes(issues)


def test_source_with_unknown_source_kind_is_error(tmp_path: Path) -> None:
    vault = _make_empty_vault(tmp_path)
    (vault / "sources" / "source-bad-kind.md").write_text(
        """---
id: source-bad-kind
title: "Source"
type: source
namespace: test
summary: "Source with unknown kind."
auto_inject: false
confidence: 0.9
verified_at: 2026-05-21
verified_by: test
edges: []
controlled_document: false
source_kind: not-a-real-kind
---
""",
        encoding="utf-8",
    )
    issues = validate(vault)
    assert "unknown-source-kind" in _issue_codes(issues)


def test_requirement_with_invalid_class_is_error(tmp_path: Path) -> None:
    vault = _make_empty_vault(tmp_path)
    (vault / "entities" / "requirements" / "requirement-bad.md").write_text(
        """---
id: requirement-bad
title: "Req"
type: requirement
namespace: test
summary: "Bad class."
auto_inject: false
confidence: 0.9
verified_at: 2026-05-21
verified_by: test
edges: []
controlled_document: false
requirement_class: bogus
---
""",
        encoding="utf-8",
    )
    issues = validate(vault)
    assert "invalid-requirement-class" in _issue_codes(issues)


@pytest.mark.parametrize(
    "valid_class", ["market", "user", "system", "software", "hardware"]
)
def test_requirement_class_accepts_all_five_values(tmp_path: Path, valid_class: str) -> None:
    """All five requirement_class values are accepted; SRS/HRS need software/hardware."""

    vault = _make_empty_vault(tmp_path)
    (vault / "entities" / "requirements" / f"requirement-{valid_class}.md").write_text(
        f"""---
id: requirement-{valid_class}
title: "Req"
type: requirement
namespace: test
summary: "Valid class: {valid_class}"
auto_inject: false
confidence: 0.9
verified_at: 2026-05-21
verified_by: test
edges: []
controlled_document: false
requirement_class: {valid_class}
---
""",
        encoding="utf-8",
    )
    issues = validate(vault)
    assert "invalid-requirement-class" not in _issue_codes(issues)


def test_risk_node_without_controlled_document_false_is_error(tmp_path: Path) -> None:
    vault = _make_empty_vault(tmp_path)
    (vault / "risk" / "hazards" / "hazard-naughty.md").write_text(
        """---
id: hazard-naughty
title: "Hazard"
type: hazard
namespace: test
summary: "Hazard pretending to be controlled."
auto_inject: false
confidence: 0.9
verified_at: 2026-05-21
verified_by: test
edges: []
controlled_document: true
---
""",
        encoding="utf-8",
    )
    issues = validate(vault)
    assert (
        "risk-or-ifu-must-declare-controlled-document-false" in _issue_codes(issues)
    )


def test_ifu_node_without_controlled_document_false_is_error(tmp_path: Path) -> None:
    vault = _make_empty_vault(tmp_path)
    (vault / "entities" / "indications-for-use" / "indication-for-use-naughty.md").write_text(
        """---
id: indication-for-use-naughty
title: "IFU"
type: indication-for-use
namespace: test
summary: "IFU pretending to be controlled."
auto_inject: false
confidence: 0.9
verified_at: 2026-05-21
verified_by: test
edges: []
controlled_document: true
population: "x"
condition: "x"
intervention: "x"
setting: "x"
belongs_to_product: nonexistent
---
""",
        encoding="utf-8",
    )
    issues = validate(vault)
    assert (
        "risk-or-ifu-must-declare-controlled-document-false" in _issue_codes(issues)
    )


def test_broken_edge_target_is_error(tmp_path: Path) -> None:
    vault = _make_empty_vault(tmp_path)
    _write_pillar(
        vault,
        node_id="pillar-with-broken-edge",
        edges="""edges:
  - target: pillar-does-not-exist
    type: supports
    weight: 0.8
""",
    )
    issues = validate(vault)
    assert "edge-target-unresolved" in _issue_codes(issues)


def test_unknown_edge_type_is_error(tmp_path: Path) -> None:
    vault = _make_empty_vault(tmp_path)
    _write_pillar(vault, node_id="pillar-source-of-edge")
    _write_pillar(
        vault,
        node_id="pillar-with-bad-edge-type",
        edges="""edges:
  - target: pillar-source-of-edge
    type: not-a-real-edge-type
    weight: 0.5
""",
    )
    issues = validate(vault)
    assert "unknown-edge-type" in _issue_codes(issues)


def test_edge_weight_out_of_range_is_error(tmp_path: Path) -> None:
    vault = _make_empty_vault(tmp_path)
    _write_pillar(vault, node_id="pillar-target")
    _write_pillar(
        vault,
        node_id="pillar-with-bad-weight",
        edges="""edges:
  - target: pillar-target
    type: supports
    weight: 1.5
""",
    )
    issues = validate(vault)
    assert "edge-weight-out-of-range" in _issue_codes(issues)


def test_metric_id_unresolved_is_error(tmp_path: Path) -> None:
    vault = _make_empty_vault(tmp_path)
    (vault / "facts" / "fact-orphan-snapshot.md").write_text(
        """---
id: fact-orphan-snapshot
title: "Orphan snapshot"
type: fact
namespace: test
summary: "Fact pointing at a metric that doesn't exist."
auto_inject: false
confidence: 0.9
verified_at: 2026-05-21
verified_by: test
edges: []
controlled_document: false
metric_id: metric-that-does-not-exist
---
""",
        encoding="utf-8",
    )
    issues = validate(vault)
    assert "metric-id-unresolved" in _issue_codes(issues)


# ---------------------------------------------------------------------------
# Summarize
# ---------------------------------------------------------------------------


def test_summarize_counts_by_severity() -> None:
    from company_brain.validator import ValidationIssue

    issues = [
        ValidationIssue("error", "a", "x"),
        ValidationIssue("error", "b", "x"),
        ValidationIssue("warning", "c", "x"),
    ]
    assert summarize(issues) == {"error": 2, "warning": 1, "info": 0}


# ---------------------------------------------------------------------------
# --strict checks for the `primary` frontmatter field
# ---------------------------------------------------------------------------


def _write_persona(
    vault: Path,
    *,
    node_id: str,
    namespace: str = "market",
    primary: bool = False,
) -> Path:
    """Minimal valid persona node, with a primary-flag hook."""

    fm = f"""---
id: {node_id}
title: "Persona {node_id}"
type: persona
namespace: {namespace}
summary: "A persona used to exercise --strict primary checks."
auto_inject: false
primary: {"true" if primary else "false"}
confidence: 0.8
verified_at: 2026-05-26
verified_by: test
tags: []
edges: []
related: []
controlled_document: false
---
# Persona {node_id}
"""
    path = vault / "entities" / "personas" / f"{node_id}.md"
    path.write_text(fm, encoding="utf-8")
    return path


def _write_competitor(
    vault: Path,
    *,
    node_id: str,
    namespace: str = "market",
    primary: bool = False,
) -> Path:
    fm = f"""---
id: {node_id}
title: "Competitor {node_id}"
type: competitor
namespace: {namespace}
summary: "A competitor used to exercise --strict primary checks."
auto_inject: false
primary: {"true" if primary else "false"}
confidence: 0.7
verified_at: 2026-05-26
verified_by: test
tags: []
edges: []
related: []
controlled_document: false
legal_name: "{node_id} Inc."
canonical_url: "https://example.com/{node_id}"
---
# Competitor {node_id}
"""
    path = vault / "entities" / "competitors" / f"{node_id}.md"
    path.write_text(fm, encoding="utf-8")
    return path


def _warning_codes(issues) -> set[str]:
    return {i.code for i in issues if i.severity == "warning"}


def test_strict_off_does_not_warn_on_multiple_primaries(tmp_path: Path) -> None:
    """Default (non-strict) validation is silent on primary-marking issues —
    the field is optional and never blocks a render."""

    vault = _make_empty_vault(tmp_path)
    _write_persona(vault, node_id="persona-one", primary=True)
    _write_persona(vault, node_id="persona-two", primary=True)
    issues = validate(vault)
    assert "multiple-primaries" not in _warning_codes(issues)


def test_strict_warns_on_multiple_primaries_in_same_namespace(tmp_path: Path) -> None:
    vault = _make_empty_vault(tmp_path)
    _write_persona(vault, node_id="persona-one", namespace="market", primary=True)
    _write_persona(vault, node_id="persona-two", namespace="market", primary=True)
    issues = validate(vault, strict=True)
    warnings = [i for i in issues if i.code == "multiple-primaries"]
    assert len(warnings) == 2, f"expected 2 warnings, got {warnings!r}"
    # Both nodes named in every warning, so a vault author skimming output
    # sees the conflict from either file.
    for w in warnings:
        assert "persona-one" in w.message
        assert "persona-two" in w.message


def test_strict_does_not_warn_on_primaries_in_different_namespaces(
    tmp_path: Path,
) -> None:
    """Per spec §2.5: namespace scoping. A primary persona in `market` and a
    primary persona in `partners` is a legitimate configuration."""

    vault = _make_empty_vault(tmp_path)
    _write_persona(vault, node_id="persona-buyer", namespace="market", primary=True)
    _write_persona(vault, node_id="persona-partner", namespace="partners", primary=True)
    issues = validate(vault, strict=True)
    assert "multiple-primaries" not in _warning_codes(issues)


def test_strict_warns_when_exports_exist_but_no_primary_marked(
    tmp_path: Path,
) -> None:
    """Spec §2.3 second warning: a primary-selecting generator has produced
    output in exports/ but no entity of the relevant type is primary."""

    vault = _make_empty_vault(tmp_path)
    _write_persona(vault, node_id="persona-one")  # primary defaults to false
    _write_persona(vault, node_id="persona-two")
    # Pretend one-pager was rendered earlier (the generator itself doesn't
    # run in this test; we only assert the validator notices the artifact).
    (vault / "exports" / "one-pager.md").write_text("# stub", encoding="utf-8")

    issues = validate(vault, strict=True)
    warnings = [i for i in issues if i.code == "exports-no-primary"]
    assert len(warnings) == 1
    assert "one-pager.md" in warnings[0].message
    assert "'persona'" in warnings[0].message


def test_strict_silent_when_export_exists_and_primary_marked(tmp_path: Path) -> None:
    vault = _make_empty_vault(tmp_path)
    _write_persona(vault, node_id="persona-one", primary=True)
    _write_persona(vault, node_id="persona-two")
    (vault / "exports" / "one-pager.md").write_text("# stub", encoding="utf-8")

    issues = validate(vault, strict=True)
    assert "exports-no-primary" not in _warning_codes(issues)


def test_strict_recognizes_sales_battle_card_competitor_suffix(tmp_path: Path) -> None:
    """sales-battle-card filenames embed the competitor id (see scaffolds.py
    `_b_sales_battle_card`); the validator must strip that to map back to
    the generator."""

    vault = _make_empty_vault(tmp_path)
    _write_competitor(vault, node_id="competitor-one")
    _write_competitor(vault, node_id="competitor-two")
    (vault / "exports" / "sales-battle-card-competitor-one.md").write_text(
        "# stub", encoding="utf-8"
    )

    issues = validate(vault, strict=True)
    warnings = [i for i in issues if i.code == "exports-no-primary"]
    assert len(warnings) == 1
    assert "'competitor'" in warnings[0].message


def test_strict_skips_export_warning_when_vault_has_no_candidates(
    tmp_path: Path,
) -> None:
    """If the vault has zero personas, a rendered one-pager is a different
    problem (handled elsewhere). Don't fire this warning."""

    vault = _make_empty_vault(tmp_path)
    (vault / "exports" / "one-pager.md").write_text("# stub", encoding="utf-8")

    issues = validate(vault, strict=True)
    assert "exports-no-primary" not in _warning_codes(issues)


def test_strict_does_not_promote_warnings_to_errors(tmp_path: Path) -> None:
    """Per design decision 3: --strict never blocks a render. Warnings only."""

    vault = _make_empty_vault(tmp_path)
    _write_persona(vault, node_id="persona-one", primary=True)
    _write_persona(vault, node_id="persona-two", primary=True)
    (vault / "exports" / "one-pager.md").write_text("# stub", encoding="utf-8")

    issues = validate(vault, strict=True)
    errors = [i for i in issues if i.severity == "error"]
    assert errors == [], f"--strict promoted warnings to errors: {errors!r}"
