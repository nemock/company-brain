"""Tests for the maintain skill (v0.4.0 step 1).

Covers the four capabilities:

* repair (filename-id, inverse edges, controlled_document, INDEX.md regen)
* decay (confidence decay on volatile fact snapshots)
* audit (read-only health summary)
* rebuild_index (just regenerate INDEX.md)

Plus the `cb validate --fix` wiring (the validator integration).
"""

from __future__ import annotations

import shutil
from datetime import date
from pathlib import Path

import pytest
import yaml

from company_brain.maintain import (
    audit,
    decay,
    rebuild_index,
    rebuild_readme,
    repair,
)
from company_brain.scaffold import AUTO_README_END, AUTO_README_START, scaffold
from company_brain.validator import validate
from company_brain.vault import VaultNotFoundError, load_vault, split_frontmatter


REPO_ROOT = Path(__file__).parent.parent
MEDDEV_VAULT = REPO_ROOT / "examples" / "meddev-fictional"


@pytest.fixture
def cloned_meddev(tmp_path: Path) -> Path:
    """A fresh copy of the meddev-fictional vault for write-tests."""

    dest = tmp_path / "vault"
    shutil.copytree(MEDDEV_VAULT, dest)
    return dest


@pytest.fixture
def broken_meddev(cloned_meddev: Path) -> Path:
    """Cloned meddev vault with the inverse `followed_by` edges stripped.

    The committed example vault is already repaired (ships in the
    post-repair state for adopters). To exercise the repair pass we have
    to put it back into a broken state — strip every `followed_by` edge
    so the surviving `preceded_by` edges have no inverse.
    """

    for md in cloned_meddev.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        fm_text, body = split_frontmatter(text)
        if fm_text is None:
            continue
        data = yaml.safe_load(fm_text) or {}
        if not isinstance(data, dict):
            continue
        edges = data.get("edges") or []
        if not isinstance(edges, list):
            continue
        filtered = [e for e in edges if isinstance(e, dict) and e.get("type") != "followed_by"]
        if len(filtered) == len(edges):
            continue
        data["edges"] = filtered
        new_fm = yaml.safe_dump(data, sort_keys=False, allow_unicode=True).strip()
        md.write_text(f"---\n{new_fm}\n---\n{body}", encoding="utf-8")
    return cloned_meddev


def _read_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fm, _ = split_frontmatter(text)
    assert fm is not None
    return yaml.safe_load(fm) or {}


# ---------------------------------------------------------------------------
# repair
# ---------------------------------------------------------------------------


def test_repair_adds_inverse_followed_by_edges(broken_meddev: Path) -> None:
    result = repair(broken_meddev, dry_run=False)
    assert any(a.code == "added-inverse-edge" for a in result.actions)
    # After repair, every preceded_by has its inverse.
    vault = load_vault(broken_meddev)
    nodes_by_id = vault.nodes_by_id
    for node in vault.nodes:
        for edge in node.edges:
            if edge.type != "preceded_by":
                continue
            target = nodes_by_id.get(edge.target)
            assert target is not None
            assert any(
                e.target == node.id and e.type == "followed_by"
                for e in target.edges
            ), f"missing inverse from {target.id} → {node.id}"


def test_repair_is_idempotent(broken_meddev: Path) -> None:
    first = repair(broken_meddev, dry_run=False)
    assert first.actions  # something happened
    second = repair(broken_meddev, dry_run=False)
    assert second.actions == []  # nothing left to do
    # INDEX.md is always rebuilt, even on a no-op pass.
    assert second.index_rebuilt is True


def test_repair_leaves_validate_clean(broken_meddev: Path) -> None:
    repair(broken_meddev, dry_run=False)
    issues = validate(broken_meddev)
    errors = [i for i in issues if i.severity == "error"]
    assert errors == []


def test_repair_dry_run_does_not_write(broken_meddev: Path) -> None:
    # Snapshot every node file's content first.
    files_before = {
        p: p.read_bytes() for p in broken_meddev.rglob("*.md")
    }
    result = repair(broken_meddev, dry_run=True)
    assert result.dry_run is True
    assert result.actions  # there are repairs available
    for path, content in files_before.items():
        # All files must be byte-identical after a dry-run.
        assert path.read_bytes() == content, f"dry-run wrote {path}"


def test_repair_on_already_clean_vault_is_noop(cloned_meddev: Path) -> None:
    """The committed example vault ships repaired, so a fresh clone has
    no repair actions to take (only the INDEX.md regen happens)."""

    result = repair(cloned_meddev, dry_run=False)
    assert result.actions == []
    assert result.index_rebuilt is True


def test_repair_renames_file_when_id_mismatches(tmp_path: Path) -> None:
    scaffold(tmp_path / "v", "default", init_git=False)
    node_file = tmp_path / "v" / "pillars" / "pillar-test-wrong-name.md"
    node_file.write_text(
        """---
id: pillar-renamed-correctly
title: "Test pillar"
type: pillar
namespace: test
summary: "A test pillar whose filename doesn't match its id."
auto_inject: false
applicable_when: null
confidence: 0.8
verified_at: 2026-01-01
verified_by: tester
staleness_signal: null
tags: []
edges: []
related: []
source_url: null
controlled_document: false
---

# Test pillar
""",
        encoding="utf-8",
    )
    result = repair(tmp_path / "v", dry_run=False)
    rename_actions = [a for a in result.actions if a.code == "renamed-to-match-id"]
    assert len(rename_actions) == 1
    assert not node_file.exists()
    assert (tmp_path / "v" / "pillars" / "pillar-renamed-correctly.md").exists()


def test_repair_does_not_clobber_existing_target_when_renaming(
    tmp_path: Path,
) -> None:
    scaffold(tmp_path / "v", "default", init_git=False)
    # Write the "wrong name" file AND a real file at the correct id name —
    # we must not overwrite the real one.
    (tmp_path / "v" / "pillars" / "pillar-a.md").write_text(
        """---
id: pillar-real
title: "Real pillar"
type: pillar
namespace: test
summary: "Real."
auto_inject: false
applicable_when: null
confidence: 0.9
verified_at: 2026-01-01
verified_by: tester
staleness_signal: null
tags: []
edges: []
related: []
source_url: null
controlled_document: false
---

# Real pillar
""",
        encoding="utf-8",
    )
    (tmp_path / "v" / "pillars" / "pillar-real.md").write_text(
        """---
id: pillar-something-else
title: "Other pillar"
type: pillar
namespace: test
summary: "Other."
auto_inject: false
applicable_when: null
confidence: 0.9
verified_at: 2026-01-01
verified_by: tester
staleness_signal: null
tags: []
edges: []
related: []
source_url: null
controlled_document: false
---

# Other pillar
""",
        encoding="utf-8",
    )
    result = repair(tmp_path / "v", dry_run=False)
    rename_actions = [a for a in result.actions if a.code == "renamed-to-match-id"]
    # `pillar-a.md` wanted to rename to `pillar-real.md` but that name was
    # taken → blocked. `pillar-real.md` wanted to rename to
    # `pillar-something-else.md` which was free → succeeded. Net: 1 rename.
    assert len(rename_actions) == 1
    assert {a.node_id for a in rename_actions} == {"pillar-something-else"}
    # `pillar-a.md` survives the pass.
    assert (tmp_path / "v" / "pillars" / "pillar-a.md").exists()
    # The original `pillar-real.md` got renamed (its id was pillar-something-else).
    assert (
        tmp_path / "v" / "pillars" / "pillar-something-else.md"
    ).exists()


def test_repair_sets_controlled_document_false_only_when_missing(
    tmp_path: Path,
) -> None:
    scaffold(tmp_path / "v", "medical-device", init_git=False)
    # A risk-insight node missing the controlled_document field.
    target = (
        tmp_path
        / "v"
        / "risk"
        / "risk-insights"
        / "risk-insight-test.md"
    )
    target.write_text(
        """---
id: risk-insight-test
title: "Test risk insight"
type: risk-insight
namespace: risk
summary: "Test."
auto_inject: false
applicable_when: null
confidence: 0.7
verified_at: 2026-01-01
verified_by: tester
staleness_signal: null
tags: []
edges: []
related: []
source_url: null
---

# Test
""",
        encoding="utf-8",
    )
    result = repair(tmp_path / "v", dry_run=False)
    actions = [a for a in result.actions if a.code == "set-controlled-document-false"]
    assert len(actions) == 1
    fm = _read_frontmatter(target)
    assert fm["controlled_document"] is False


# ---------------------------------------------------------------------------
# decay
# ---------------------------------------------------------------------------


def test_decay_applies_half_life_to_high_volatility_fact(
    cloned_meddev: Path,
) -> None:
    # The example vault has two fact snapshots tied to a high-volatility
    # metric ("pad attach rate at day 1"). Verified date is 2026-05-21.
    # A year later, with high volatility (1-month half-life), confidence
    # should be close to 0.
    result = decay(cloned_meddev, today=date(2027, 5, 21), dry_run=False)
    fact_decays = [
        a for a in result.actions if "pad-attach" in a.metric_id
    ]
    assert fact_decays, "expected at least one pad-attach decay"
    for action in fact_decays:
        assert action.volatility_class == "high"
        # 12 months / 1-month half-life → 2^-12 ≈ 0.000244
        assert action.confidence_after < 0.01


def test_decay_preserves_original_via_confidence_original(
    cloned_meddev: Path,
) -> None:
    decay(cloned_meddev, today=date(2027, 1, 1), dry_run=False)
    fact_file = (
        cloned_meddev / "facts" / "fact-pad-attach-rate-2026-q1.md"
    )
    fm = _read_frontmatter(fact_file)
    assert "confidence_original" in fm
    assert fm["confidence_original"] == 0.95


def test_decay_is_idempotent_for_same_today(cloned_meddev: Path) -> None:
    first = decay(cloned_meddev, today=date(2027, 1, 1), dry_run=False)
    assert first.actions
    second = decay(cloned_meddev, today=date(2027, 1, 1), dry_run=False)
    assert second.actions == []


def test_decay_advances_when_today_advances(cloned_meddev: Path) -> None:
    first = decay(cloned_meddev, today=date(2026, 7, 1), dry_run=False)
    assert first.actions
    second = decay(cloned_meddev, today=date(2027, 1, 1), dry_run=False)
    # The confidence values should change further as time advances.
    assert second.actions


def test_decay_skips_facts_without_metric_id(tmp_path: Path) -> None:
    scaffold(tmp_path / "v", "default", init_git=False)
    fact_file = tmp_path / "v" / "facts" / "fact-test.md"
    fact_file.write_text(
        """---
id: fact-test
title: "Standalone fact"
type: fact
namespace: test
summary: "A fact with no metric_id."
auto_inject: false
applicable_when: null
confidence: 0.9
verified_at: 2020-01-01
verified_by: tester
staleness_signal: null
tags: []
edges: []
related: []
source_url: null
controlled_document: false
---

# Standalone fact
""",
        encoding="utf-8",
    )
    result = decay(tmp_path / "v", today=date(2027, 1, 1), dry_run=False)
    assert result.actions == []


def test_decay_dry_run_does_not_write(cloned_meddev: Path) -> None:
    fact_file = (
        cloned_meddev / "facts" / "fact-pad-attach-rate-2026-q1.md"
    )
    before = fact_file.read_bytes()
    result = decay(cloned_meddev, today=date(2027, 1, 1), dry_run=True)
    assert result.actions
    assert result.dry_run is True
    assert fact_file.read_bytes() == before


# ---------------------------------------------------------------------------
# rebuild_index
# ---------------------------------------------------------------------------


def test_rebuild_index_writes_node_tables(cloned_meddev: Path) -> None:
    target = rebuild_index(cloned_meddev)
    content = target.read_text()
    assert "# Master Node Index" in content
    assert "**Active profile**: `medical-device`." in content
    # Every node type bucket gets a heading.
    assert "### `pillar`" in content
    assert "### `competitor`" in content
    assert "### `indication-for-use`" in content
    # And each node id shows up.
    assert "pillar-icp-ambulatory-cardiac-patients" in content


def test_rebuild_index_handles_empty_vault(tmp_path: Path) -> None:
    scaffold(tmp_path / "v", "default", init_git=False)
    target = rebuild_index(tmp_path / "v")
    content = target.read_text()
    assert "Total nodes**: 0" in content
    assert "No nodes yet" in content


def test_rebuild_index_is_idempotent(cloned_meddev: Path) -> None:
    rebuild_index(cloned_meddev)
    first = (cloned_meddev / "_system" / "INDEX.md").read_bytes()
    rebuild_index(cloned_meddev)
    second = (cloned_meddev / "_system" / "INDEX.md").read_bytes()
    assert first == second


# ---------------------------------------------------------------------------
# audit
# ---------------------------------------------------------------------------


def test_audit_returns_repair_and_decay_candidates(broken_meddev: Path) -> None:
    report = audit(broken_meddev)
    # The synthetic-broken vault has missing inverse edges.
    assert len(report.repair_candidates) > 0
    # Findings include at least the vault-size info line.
    assert any(f.code == "vault-size" for f in report.findings)


def test_audit_on_clean_vault_has_no_repair_candidates(cloned_meddev: Path) -> None:
    report = audit(cloned_meddev)
    assert report.repair_candidates == []
    assert any(f.code == "vault-size" for f in report.findings)


def test_audit_flags_no_sources_in_empty_vault(tmp_path: Path) -> None:
    scaffold(tmp_path / "v", "default", init_git=False)
    report = audit(tmp_path / "v")
    codes = {f.code for f in report.findings}
    assert "no-sources" in codes
    assert "no-pillars" in codes


# ---------------------------------------------------------------------------
# rebuild_readme
# ---------------------------------------------------------------------------


def test_rebuild_readme_regenerates_auto_section(cloned_meddev: Path) -> None:
    result = rebuild_readme(cloned_meddev, strict=True)
    assert result.status == "rebuilt"
    readme = (cloned_meddev / "README.md").read_text()
    assert AUTO_README_START in readme
    assert AUTO_README_END in readme
    # Real vault state shows up.
    assert "**Vault state:**" in readme
    # Pillars from the meddev vault appear.
    assert "pillar-icp-ambulatory-cardiac-patients" in readme
    assert "pillar-no-pediatric-use" in readme
    # Products and competitors too.
    assert "product-vitalisens-cardio" in readme
    assert "competitor-cardiotrace-inc" in readme
    # Latest-exports section.
    assert "### Latest exports" in readme


def test_rebuild_readme_is_idempotent(cloned_meddev: Path) -> None:
    rebuild_readme(cloned_meddev, strict=True)
    first = (cloned_meddev / "README.md").read_bytes()
    rebuild_readme(cloned_meddev, strict=True)
    second = (cloned_meddev / "README.md").read_bytes()
    assert first == second


def test_rebuild_readme_preserves_content_outside_markers(cloned_meddev: Path) -> None:
    readme_path = cloned_meddev / "README.md"
    text = readme_path.read_text()
    # Hand-edit a section OUTSIDE the markers.
    text = text.replace("## Layout", "## Layout (custom hand-edit marker)")
    # Append something at the very end too.
    text = text.rstrip() + "\n\n## Custom appendix\n\nThis was added by hand.\n"
    readme_path.write_text(text, encoding="utf-8")

    rebuild_readme(cloned_meddev, strict=True)
    after = readme_path.read_text()
    assert "## Layout (custom hand-edit marker)" in after
    assert "## Custom appendix" in after
    assert "This was added by hand." in after


def test_rebuild_readme_dry_run_does_not_write(cloned_meddev: Path) -> None:
    readme_path = cloned_meddev / "README.md"
    before = readme_path.read_bytes()
    result = rebuild_readme(cloned_meddev, strict=True, dry_run=True)
    assert result.status == "skipped-dry-run"
    assert readme_path.read_bytes() == before


def test_rebuild_readme_strict_raises_when_markers_missing(tmp_path: Path) -> None:
    scaffold(tmp_path / "v", "default", init_git=False)
    readme_path = tmp_path / "v" / "README.md"
    # Strip the markers entirely.
    text = readme_path.read_text()
    text = text.replace(AUTO_README_START, "").replace(AUTO_README_END, "")
    readme_path.write_text(text, encoding="utf-8")

    with pytest.raises(ValueError, match="cb:auto markers"):
        rebuild_readme(tmp_path / "v", strict=True)


def test_rebuild_readme_non_strict_returns_no_markers_status(tmp_path: Path) -> None:
    scaffold(tmp_path / "v", "default", init_git=False)
    readme_path = tmp_path / "v" / "README.md"
    text = readme_path.read_text()
    text = text.replace(AUTO_README_START, "").replace(AUTO_README_END, "")
    readme_path.write_text(text, encoding="utf-8")

    result = rebuild_readme(tmp_path / "v", strict=False)
    assert result.status == "no-markers"


def test_rebuild_readme_strict_raises_when_no_readme(tmp_path: Path) -> None:
    scaffold(tmp_path / "v", "default", init_git=False)
    (tmp_path / "v" / "README.md").unlink()
    with pytest.raises(FileNotFoundError, match="does not exist"):
        rebuild_readme(tmp_path / "v", strict=True)


def test_rebuild_readme_non_strict_returns_no_readme_status(tmp_path: Path) -> None:
    scaffold(tmp_path / "v", "default", init_git=False)
    (tmp_path / "v" / "README.md").unlink()
    result = rebuild_readme(tmp_path / "v", strict=False)
    assert result.status == "no-readme"


def test_repair_also_refreshes_readme_auto_section(cloned_meddev: Path) -> None:
    """`cb maintain repair` should regenerate the README auto-section."""

    # Manually scribble inside the markers so we can verify it gets overwritten.
    readme_path = cloned_meddev / "README.md"
    text = readme_path.read_text()
    start = text.find(AUTO_README_START)
    end = text.find(AUTO_README_END)
    text = (
        text[: start + len(AUTO_README_START)]
        + "\nSCRIBBLE that maintain should overwrite\n"
        + text[end:]
    )
    readme_path.write_text(text, encoding="utf-8")

    result = repair(cloned_meddev, dry_run=False)
    assert result.readme_status == "rebuilt"
    assert "SCRIBBLE" not in readme_path.read_text()


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------


def test_repair_raises_on_missing_vault(tmp_path: Path) -> None:
    with pytest.raises(VaultNotFoundError):
        repair(tmp_path / "does-not-exist")


def test_decay_raises_on_missing_vault(tmp_path: Path) -> None:
    with pytest.raises(VaultNotFoundError):
        decay(tmp_path / "does-not-exist")
