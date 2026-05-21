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
