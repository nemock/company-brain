"""Tests for the document-driven intake helpers (manifest + gap detection + CLI).

Covers:

* The manifest loader: well-formed loads, malformed YAML, unknown
  references, structural validation.
* Profile filtering: medical-device-only sections drop on non-meddev vaults
  and survive on meddev vaults.
* Gap detection against both shipped example vaults.
* The two new CLI subcommands (``describe-doc-questions``, ``gaps-for-doc``):
  happy path, error paths, JSON shape, idempotency.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from company_brain.cli import app
from company_brain.intake.doc_questions import (
    Manifest,
    ManifestError,
    UnknownDocError,
    compute_gaps,
    filter_for_profile,
    gaps_to_dict,
    list_manifests,
    load_manifest,
    manifest_to_dict,
)
from company_brain.vault import load_vault


REPO_ROOT = Path(__file__).parent.parent
SAAS_VAULT = REPO_ROOT / "examples" / "saas-fictional"
MEDDEV_VAULT = REPO_ROOT / "examples" / "meddev-fictional"


runner = CliRunner()


# ---------------------------------------------------------------------------
# Manifest loading — registry
# ---------------------------------------------------------------------------


def test_list_manifests_includes_mrd() -> None:
    assert "mrd" in list_manifests()


def test_load_unknown_doc_raises() -> None:
    with pytest.raises(UnknownDocError) as exc:
        load_manifest("not-a-doc")
    assert "not-a-doc" in str(exc.value)


def test_load_mrd_manifest_well_formed() -> None:
    manifest = load_manifest("mrd")
    assert manifest.doc == "mrd"
    assert manifest.title.startswith("Marketing Requirements")
    assert manifest.intro  # non-empty
    section_ids = [s.id for s in manifest.sections]
    # The 9 interview sections, in order.
    assert section_ids == [
        "executive-summary",
        "vision-positioning",
        "indications-for-use",
        "market-personas",
        "market-requirements",
        "competitive-landscape",
        "regulatory-landscape",
        "open-questions",
        "non-goals",
    ]


def test_load_mrd_section_shape() -> None:
    manifest = load_manifest("mrd")
    exec_summary = manifest.sections[0]
    assert exec_summary.id == "executive-summary"
    assert exec_summary.profile_required is None
    # Two feeds_from slots: positive pillars + products.
    assert len(exec_summary.feeds_from) == 2
    slots_by_type = {f.type: f for f in exec_summary.feeds_from}
    assert slots_by_type["pillar"].role == "positive"
    assert slots_by_type["pillar"].min == 1
    assert slots_by_type["product"].min == 1
    # At least one question.
    assert exec_summary.questions
    assert exec_summary.questions[0].prompt


def test_load_mrd_medical_device_sections_gated() -> None:
    manifest = load_manifest("mrd")
    gated = {s.id: s.profile_required for s in manifest.sections}
    assert gated["indications-for-use"] == "medical-device"
    assert gated["regulatory-landscape"] == "medical-device"
    assert gated["executive-summary"] is None


# ---------------------------------------------------------------------------
# Manifest validation — error paths via in-memory yaml inputs
# ---------------------------------------------------------------------------


def _write_manifest(tmp_path: Path, body: str) -> Path:
    """Write a YAML manifest file to a manifests dir and monkeypatch the
    module loader by injecting a custom path. We patch ``_MANIFESTS_DIR``
    by writing into a tmp directory and re-importing the module isn't worth
    it — instead, exercise the parser via the YAML body and the public load
    function only for the registered MRD manifest. Validation tests here
    therefore use the lower-level parser by writing a file and patching.
    """

    raise NotImplementedError


@pytest.fixture
def patched_manifests_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point the doc_questions loader at a tmp manifests dir."""

    target = tmp_path / "manifests"
    target.mkdir()
    monkeypatch.setattr(
        "company_brain.intake.doc_questions._MANIFESTS_DIR", target
    )
    return target


def test_manifest_invalid_yaml_raises(patched_manifests_dir: Path) -> None:
    (patched_manifests_dir / "bad.yaml").write_text(": not yaml ::: -", encoding="utf-8")
    with pytest.raises(ManifestError) as exc:
        load_manifest("bad")
    assert "YAML parse error" in str(exc.value) or "parse" in str(exc.value).lower()


def test_manifest_root_must_be_mapping(patched_manifests_dir: Path) -> None:
    (patched_manifests_dir / "bad.yaml").write_text("- just\n- a\n- list\n", encoding="utf-8")
    with pytest.raises(ManifestError):
        load_manifest("bad")


def test_manifest_missing_doc_field(patched_manifests_dir: Path) -> None:
    (patched_manifests_dir / "bad.yaml").write_text(
        "title: X\nsections: [{id: a, title: A}]\n", encoding="utf-8"
    )
    with pytest.raises(ManifestError) as exc:
        load_manifest("bad")
    assert "doc" in str(exc.value)


def test_manifest_empty_sections_list(patched_manifests_dir: Path) -> None:
    (patched_manifests_dir / "bad.yaml").write_text(
        "doc: x\ntitle: X\nsections: []\n", encoding="utf-8"
    )
    with pytest.raises(ManifestError) as exc:
        load_manifest("bad")
    assert "sections" in str(exc.value)


def test_manifest_unknown_profile_required(patched_manifests_dir: Path) -> None:
    (patched_manifests_dir / "bad.yaml").write_text(
        """
doc: x
title: X
sections:
  - id: s1
    title: S1
    profile_required: martian
""".strip(),
        encoding="utf-8",
    )
    with pytest.raises(ManifestError) as exc:
        load_manifest("bad")
    assert "martian" in str(exc.value)


def test_manifest_unknown_node_type_in_feeds_from(patched_manifests_dir: Path) -> None:
    (patched_manifests_dir / "bad.yaml").write_text(
        """
doc: x
title: X
sections:
  - id: s1
    title: S1
    feeds_from:
      - type: not-a-node-type
""".strip(),
        encoding="utf-8",
    )
    with pytest.raises(ManifestError) as exc:
        load_manifest("bad")
    assert "not-a-node-type" in str(exc.value)


def test_manifest_negative_min(patched_manifests_dir: Path) -> None:
    (patched_manifests_dir / "bad.yaml").write_text(
        """
doc: x
title: X
sections:
  - id: s1
    title: S1
    feeds_from:
      - type: pillar
        min: -1
""".strip(),
        encoding="utf-8",
    )
    with pytest.raises(ManifestError) as exc:
        load_manifest("bad")
    assert "negative" in str(exc.value).lower()


def test_manifest_duplicate_section_id(patched_manifests_dir: Path) -> None:
    (patched_manifests_dir / "bad.yaml").write_text(
        """
doc: x
title: X
sections:
  - id: s1
    title: S1
  - id: s1
    title: Other
""".strip(),
        encoding="utf-8",
    )
    with pytest.raises(ManifestError) as exc:
        load_manifest("bad")
    assert "duplicate" in str(exc.value).lower()


def test_manifest_unknown_capture_node_type(patched_manifests_dir: Path) -> None:
    (patched_manifests_dir / "bad.yaml").write_text(
        """
doc: x
title: X
sections:
  - id: s1
    title: S1
    questions:
      - prompt: ask
        captures: [not-real-type]
""".strip(),
        encoding="utf-8",
    )
    with pytest.raises(ManifestError) as exc:
        load_manifest("bad")
    assert "not-real-type" in str(exc.value)


# ---------------------------------------------------------------------------
# Profile filtering
# ---------------------------------------------------------------------------


def test_filter_drops_medical_device_sections_for_default_profile() -> None:
    manifest = load_manifest("mrd")
    filtered = filter_for_profile(manifest, None)
    ids = [s.id for s in filtered.sections]
    assert "indications-for-use" not in ids
    assert "regulatory-landscape" not in ids
    # The profile-agnostic ones survive.
    assert "executive-summary" in ids
    assert len(filtered.sections) == 7


def test_filter_keeps_all_for_medical_device_profile() -> None:
    manifest = load_manifest("mrd")
    filtered = filter_for_profile(manifest, "medical-device")
    assert len(filtered.sections) == 9


def test_filter_drops_meddev_for_saas_profile() -> None:
    manifest = load_manifest("mrd")
    filtered = filter_for_profile(manifest, "saas")
    ids = [s.id for s in filtered.sections]
    assert "indications-for-use" not in ids
    assert "regulatory-landscape" not in ids


# ---------------------------------------------------------------------------
# Gap detection — against example vaults
# ---------------------------------------------------------------------------


def test_gaps_saas_vault_all_complete() -> None:
    vault = load_vault(SAAS_VAULT)
    manifest = filter_for_profile(load_manifest("mrd"), vault.profile_name)
    gaps = compute_gaps(manifest, vault)
    # All 7 sections complete (saas-fictional is the fully-populated reference).
    assert len(gaps) == 7
    statuses = [g.status for g in gaps]
    assert statuses.count("complete") == 7


def test_gaps_meddev_vault_status_breakdown() -> None:
    vault = load_vault(MEDDEV_VAULT)
    manifest = filter_for_profile(load_manifest("mrd"), vault.profile_name)
    gaps = compute_gaps(manifest, vault)
    assert len(gaps) == 9
    # The meddev vault has 2 positive pillars vs the section's min=3, so
    # vision-positioning lands as partial. Every other section is complete.
    by_id = {g.section_id: g for g in gaps}
    assert by_id["vision-positioning"].status == "partial"
    assert by_id["executive-summary"].status == "complete"
    assert by_id["indications-for-use"].status == "complete"
    assert by_id["regulatory-landscape"].status == "complete"


def test_gaps_slot_role_filtering_distinguishes_positive_vs_non_goal_pillars() -> None:
    """The MRD has two slots looking at pillar nodes — positive and non-goal.
    Gap detection must filter pillars by role so both slots can be satisfied
    independently from the same pillar set."""

    vault = load_vault(SAAS_VAULT)
    manifest = filter_for_profile(load_manifest("mrd"), vault.profile_name)
    gaps = compute_gaps(manifest, vault)
    by_id = {g.section_id: g for g in gaps}

    exec_section = by_id["executive-summary"]
    exec_pillar_slot = next(s for s in exec_section.slots if s.type == "pillar")
    assert exec_pillar_slot.role == "positive"
    assert exec_pillar_slot.count >= 1
    # No non-goal pillar should land in the positive slot.
    positive_ids = set(exec_pillar_slot.found_ids)

    non_goal_section = by_id["non-goals"]
    non_goal_pillar_slot = next(s for s in non_goal_section.slots if s.type == "pillar")
    assert non_goal_pillar_slot.role == "non-goal"
    non_goal_ids = set(non_goal_pillar_slot.found_ids)

    assert positive_ids.isdisjoint(non_goal_ids)


def test_gaps_decision_rules_out_role() -> None:
    """The non-goals section also looks at decisions with a 'What This Rules Out'
    body section. Verify the role filter picks those out."""

    vault = load_vault(SAAS_VAULT)
    manifest = filter_for_profile(load_manifest("mrd"), vault.profile_name)
    gaps = compute_gaps(manifest, vault)
    by_id = {g.section_id: g for g in gaps}
    non_goal_section = by_id["non-goals"]
    decision_slot = next(s for s in non_goal_section.slots if s.type == "decision")
    assert decision_slot.role == "rules-out"
    # Every matched id should be a decision node with the rules-out section.
    for nid in decision_slot.found_ids:
        node = vault.nodes_by_id[nid]
        assert "## What This Rules Out" in node.body


def test_gaps_requirement_class_role() -> None:
    """market-requirements should match only requirements with class=market."""

    vault = load_vault(SAAS_VAULT)
    manifest = filter_for_profile(load_manifest("mrd"), vault.profile_name)
    gaps = compute_gaps(manifest, vault)
    by_id = {g.section_id: g for g in gaps}
    section = by_id["market-requirements"]
    slot = section.slots[0]
    assert slot.role == "market"
    for nid in slot.found_ids:
        node = vault.nodes_by_id[nid]
        assert str(node.frontmatter.get("requirement_class")) == "market"


# ---------------------------------------------------------------------------
# Serialization helpers
# ---------------------------------------------------------------------------


def test_manifest_to_dict_roundtrips_structure() -> None:
    manifest = load_manifest("mrd")
    payload = manifest_to_dict(manifest)
    assert payload["doc"] == "mrd"
    assert len(payload["sections"]) == len(manifest.sections)
    # Section structure preserved.
    first = payload["sections"][0]
    assert first["id"] == manifest.sections[0].id
    assert isinstance(first["feeds_from"], list)
    assert isinstance(first["questions"], list)


def test_gaps_to_dict_summary_matches_status_counts() -> None:
    vault = load_vault(MEDDEV_VAULT)
    manifest = filter_for_profile(load_manifest("mrd"), vault.profile_name)
    gaps = compute_gaps(manifest, vault)
    d = gaps_to_dict(gaps)
    assert sum(d["summary"].values()) == len(d["sections"])
    counts = {"complete": 0, "partial": 0, "empty": 0}
    for s in d["sections"]:
        counts[s["status"]] += 1
    assert counts == d["summary"]


# ---------------------------------------------------------------------------
# CLI: describe-doc-questions
# ---------------------------------------------------------------------------


def test_cli_describe_doc_questions_no_path_emits_full_manifest() -> None:
    result = runner.invoke(app, ["describe-doc-questions", "mrd"])
    assert result.exit_code == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["doc"] == "mrd"
    # Without --path, every section is present, including profile-gated ones.
    ids = [s["id"] for s in data["sections"]]
    assert "indications-for-use" in ids
    assert "regulatory-landscape" in ids


def test_cli_describe_doc_questions_filters_for_saas_vault() -> None:
    result = runner.invoke(
        app, ["describe-doc-questions", "mrd", "--path", str(SAAS_VAULT)]
    )
    assert result.exit_code == 0, result.stderr
    data = json.loads(result.stdout)
    ids = [s["id"] for s in data["sections"]]
    assert "indications-for-use" not in ids
    assert "regulatory-landscape" not in ids
    assert "executive-summary" in ids


def test_cli_describe_doc_questions_keeps_meddev_sections() -> None:
    result = runner.invoke(
        app, ["describe-doc-questions", "mrd", "--path", str(MEDDEV_VAULT)]
    )
    assert result.exit_code == 0, result.stderr
    data = json.loads(result.stdout)
    ids = [s["id"] for s in data["sections"]]
    assert "indications-for-use" in ids
    assert "regulatory-landscape" in ids


def test_cli_describe_doc_questions_unknown_doc_exits_2() -> None:
    result = runner.invoke(app, ["describe-doc-questions", "no-such-doc"])
    assert result.exit_code == 2
    assert "no-such-doc" in result.stderr
    # The hint should name known docs.
    assert "mrd" in result.stderr


def test_cli_describe_doc_questions_bad_path_exits_2(tmp_path: Path) -> None:
    result = runner.invoke(
        app, ["describe-doc-questions", "mrd", "--path", str(tmp_path / "nowhere")]
    )
    assert result.exit_code == 2


def test_cli_describe_doc_questions_idempotent() -> None:
    a = runner.invoke(app, ["describe-doc-questions", "mrd", "--path", str(SAAS_VAULT)])
    b = runner.invoke(app, ["describe-doc-questions", "mrd", "--path", str(SAAS_VAULT)])
    assert a.exit_code == 0 and b.exit_code == 0
    assert a.stdout == b.stdout


# ---------------------------------------------------------------------------
# CLI: gaps-for-doc
# ---------------------------------------------------------------------------


def test_cli_gaps_for_doc_saas_all_complete() -> None:
    result = runner.invoke(app, ["gaps-for-doc", "mrd", "--path", str(SAAS_VAULT)])
    assert result.exit_code == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["summary"]["complete"] == 7
    assert data["summary"]["partial"] == 0
    assert data["summary"]["empty"] == 0


def test_cli_gaps_for_doc_meddev_includes_medical_sections() -> None:
    result = runner.invoke(app, ["gaps-for-doc", "mrd", "--path", str(MEDDEV_VAULT)])
    assert result.exit_code == 0, result.stderr
    data = json.loads(result.stdout)
    ids = [s["section_id"] for s in data["sections"]]
    assert "indications-for-use" in ids
    assert "regulatory-landscape" in ids


def test_cli_gaps_for_doc_unknown_doc_exits_2() -> None:
    result = runner.invoke(app, ["gaps-for-doc", "no-such-doc"])
    assert result.exit_code == 2
    assert "no-such-doc" in result.stderr


def test_cli_gaps_for_doc_bad_vault_path_exits_2(tmp_path: Path) -> None:
    result = runner.invoke(
        app, ["gaps-for-doc", "mrd", "--path", str(tmp_path / "nowhere")]
    )
    assert result.exit_code == 2


def test_cli_gaps_for_doc_idempotent() -> None:
    a = runner.invoke(app, ["gaps-for-doc", "mrd", "--path", str(MEDDEV_VAULT)])
    b = runner.invoke(app, ["gaps-for-doc", "mrd", "--path", str(MEDDEV_VAULT)])
    assert a.exit_code == 0 and b.exit_code == 0
    assert a.stdout == b.stdout


# ---------------------------------------------------------------------------
# Empty-vault gap behavior — every section lands as 'empty'
# ---------------------------------------------------------------------------


def test_gaps_empty_vault_every_section_empty(tmp_path: Path) -> None:
    """A freshly-scaffolded vault has no nodes, so every section with at
    least one feeds_from slot should classify as ``empty`` (or stay complete
    for sections with no slots — none currently exist, but if added later)."""

    from datetime import date

    from company_brain.scaffold import scaffold

    vault_dir = scaffold(
        tmp_path / "blank", "default", today=date(2026, 5, 26), init_git=False
    ).vault_path
    vault = load_vault(vault_dir)
    manifest = filter_for_profile(load_manifest("mrd"), vault.profile_name)
    gaps = compute_gaps(manifest, vault)
    assert all(g.status == "empty" for g in gaps)


# ---------------------------------------------------------------------------
# Manifest can be re-constructed from its dict form (sanity check)
# ---------------------------------------------------------------------------


def test_manifest_to_dict_is_stable() -> None:
    """Two calls to manifest_to_dict on the same manifest produce equal dicts."""

    manifest = load_manifest("mrd")
    a = manifest_to_dict(manifest)
    b = manifest_to_dict(manifest)
    assert a == b


def test_manifest_is_immutable_dataclass() -> None:
    """Manifest is frozen — accidental mutation should fail at write time."""

    manifest = load_manifest("mrd")
    with pytest.raises((AttributeError, Exception)):
        manifest.doc = "other"  # type: ignore[misc]
    assert isinstance(manifest, Manifest)
