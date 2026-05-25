"""Vault maintenance.

Read+write companion to the validator. Five capabilities:

1. **Auto-repair** — fix what can be fixed without ambiguity:
   missing inverse edges (only the declared pair ``preceded_by`` ↔
   ``followed_by``), filename-id mismatch (rename file to match id),
   missing ``controlled_document: false`` in risk/IFU folders when the
   field is absent (never overwrite an explicit value).
2. **Confidence decay** — fact nodes with a ``metric_id`` get their
   confidence reduced based on age and the metric's ``volatility_class``.
   Half-life by class: low = 24 months, medium = 6 months, high = 1
   month. Preserves the original via ``confidence_original`` on first
   decay so re-runs are idempotent.
3. **INDEX.md regeneration** — writes ``_system/INDEX.md`` listing every
   node by category.
4. **Audit report** — read-only summary of vault health.
5. **`cb validate --fix`** wires into the auto-repair pass.

What this module deliberately does NOT do:

- Resolve duplicate ids, unknown types, folder-type mismatches, broken
  edge targets, missing required fields, profile mismatches. Those all
  need a human call.
- Overwrite an explicit ``controlled_document: true`` (it shouldn't be
  there per the boundary, but maintain doesn't get to silently flip it).
- Remove or comment out edges.
- Touch schema-drift fields (frontmatter keys not in the spec) — could
  be a forward-compat experiment.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

from .scaffold import AUTO_README_END, AUTO_README_START
from .schema import (
    EDGE_TYPES,
    NodeCategory,
    get_active_node_types,
    get_node_type,
)
from .vault import Node, Vault, VaultNotFoundError, load_vault, split_frontmatter


# ---------------------------------------------------------------------------
# Public dataclasses
# ---------------------------------------------------------------------------


@dataclass
class RepairAction:
    """One change the repair pass made (or would make in dry-run)."""

    code: str
    node_id: str
    path: Path
    detail: str


@dataclass
class RepairResult:
    actions: list[RepairAction] = field(default_factory=list)
    index_rebuilt: bool = False
    readme_status: str = "skipped"  # see ReadmeRegenResult.status
    dry_run: bool = False

    @property
    def count(self) -> int:
        return len(self.actions) + (1 if self.index_rebuilt else 0)


@dataclass
class DecayAction:
    """One confidence-decay update applied (or would be applied in dry-run)."""

    node_id: str
    path: Path
    metric_id: str
    volatility_class: str
    age_months: float
    confidence_before: float
    confidence_after: float


@dataclass
class DecayResult:
    actions: list[DecayAction] = field(default_factory=list)
    dry_run: bool = False


@dataclass
class ReadmeRegenResult:
    """Outcome of regenerating the README auto-section."""

    path: Path | None
    status: str  # "rebuilt" | "no-readme" | "no-markers" | "skipped-dry-run"
    detail: str = ""


@dataclass
class AuditFinding:
    severity: str  # "info" | "notice"
    code: str
    message: str


@dataclass
class AuditReport:
    repair_candidates: list[RepairAction]
    decay_candidates: list[DecayAction]
    findings: list[AuditFinding]


# ---------------------------------------------------------------------------
# Decay constants
# ---------------------------------------------------------------------------


# Half-life in months per volatility_class. PRD §14 numbers.
_HALF_LIFE_MONTHS = {
    "low": 24.0,
    "medium": 6.0,
    "high": 1.0,
}

# Edge inverse pairs known in the schema. Maintain only auto-fills the
# `preceded_by` ↔ `followed_by` pair — others may be added if the
# EdgeTypeSpec.inverse field is set in the future.
def _inverse_pairs() -> dict[str, str]:
    pairs: dict[str, str] = {}
    for name, spec in EDGE_TYPES.items():
        if spec.inverse:
            pairs[name] = spec.inverse
    return pairs


# ---------------------------------------------------------------------------
# Public entry points
# ---------------------------------------------------------------------------


def repair(vault_path: Path, *, dry_run: bool = False) -> RepairResult:
    """Run the auto-repair pass on ``vault_path``.

    Idempotent: re-running on an already-repaired vault is a no-op.
    """

    vault = load_vault(vault_path)
    result = RepairResult(dry_run=dry_run)

    # 1. Filename-id mismatch.
    for node in vault.nodes:
        actions = _repair_filename_mismatch(node, vault_path, dry_run=dry_run)
        result.actions.extend(actions)

    # Reload vault after potential file renames so subsequent passes see
    # the new paths.
    if any(a.code == "renamed-to-match-id" for a in result.actions) and not dry_run:
        vault = load_vault(vault_path)

    # 2. Missing controlled_document: false in risk/IFU folders.
    for node in vault.nodes:
        actions = _repair_missing_controlled_document(node, vault_path, dry_run=dry_run)
        result.actions.extend(actions)

    # 3. Missing inverse edges.
    for node in vault.nodes:
        actions = _repair_missing_inverse_edges(node, vault, vault_path, dry_run=dry_run)
        result.actions.extend(actions)

    # 4. INDEX.md regeneration — always done at the end of a repair.
    if not dry_run:
        # Reload one last time so the index reflects any newly-fixed nodes.
        vault = load_vault(vault_path)
        _write_index(vault, vault_path)
    result.index_rebuilt = True

    # 5. README auto-section regeneration — silent skip if no README or no
    # markers. Failing here for a missing/clean README would be unfriendly;
    # the dedicated `cb maintain rebuild-readme` command is the loud path.
    readme_outcome = rebuild_readme(vault_path, strict=False, dry_run=dry_run)
    result.readme_status = readme_outcome.status

    return result


def decay(
    vault_path: Path, *, today: date | None = None, dry_run: bool = False
) -> DecayResult:
    """Apply confidence decay to fact snapshots.

    ``today`` lets tests pin the reference date. Defaults to the current
    system date.
    """

    vault = load_vault(vault_path)
    today = today or date.today()
    result = DecayResult(dry_run=dry_run)
    nodes_by_id = vault.nodes_by_id

    for node in sorted(vault.nodes, key=lambda n: n.id):
        action = _maybe_decay(node, vault_path, nodes_by_id, today, dry_run=dry_run)
        if action is not None:
            result.actions.append(action)
    return result


def audit(vault_path: Path) -> AuditReport:
    """Read-only health summary."""

    repair_preview = repair(vault_path, dry_run=True)
    decay_preview = decay(vault_path, dry_run=True)
    findings = _audit_findings(load_vault(vault_path))
    return AuditReport(
        repair_candidates=repair_preview.actions,
        decay_candidates=decay_preview.actions,
        findings=findings,
    )


def rebuild_index(vault_path: Path) -> Path:
    """Regenerate ``<vault>/_system/INDEX.md`` from the current nodes.

    Returns the absolute path of the written file.
    """

    vault = load_vault(vault_path)
    return _write_index(vault, vault_path)


def rebuild_readme(
    vault_path: Path, *, strict: bool = True, dry_run: bool = False
) -> ReadmeRegenResult:
    """Regenerate the auto-section of ``<vault>/README.md`` in place.

    The auto-section is the markdown block between ``AUTO_README_START``
    and ``AUTO_README_END`` markers (declared in
    :mod:`company_brain.scaffold`). Everything outside the markers is
    preserved.

    ``strict`` controls behavior when the README is missing or has no
    markers:

    * ``strict=True`` (default; the user-facing CLI path) — raises
      ``FileNotFoundError`` or ``ValueError``.
    * ``strict=False`` (what ``repair`` calls) — returns a
      :class:`ReadmeRegenResult` with a non-rebuilt ``status`` and does
      not raise.

    Returns a :class:`ReadmeRegenResult` describing the outcome.
    """

    readme = vault_path / "README.md"
    if not readme.is_file():
        if strict:
            raise FileNotFoundError(
                f"{readme} does not exist; run `cb scaffold --force` to create it."
            )
        return ReadmeRegenResult(path=None, status="no-readme")

    text = readme.read_text(encoding="utf-8")
    start = text.find(AUTO_README_START)
    end = text.find(AUTO_README_END)
    if start == -1 or end == -1 or end < start:
        if strict:
            raise ValueError(
                f"{readme} does not contain the cb:auto markers "
                f"({AUTO_README_START!r} / {AUTO_README_END!r}); "
                "run `cb scaffold --force` to regenerate."
            )
        return ReadmeRegenResult(
            path=readme,
            status="no-markers",
            detail="auto-section markers missing",
        )

    vault = load_vault(vault_path)
    new_inner = _render_readme_auto_section(vault, vault_path)

    new_text = (
        text[: start + len(AUTO_README_START)]
        + "\n"
        + new_inner
        + text[end:]
    )

    if dry_run:
        return ReadmeRegenResult(
            path=readme,
            status="skipped-dry-run",
            detail=f"would rewrite {len(new_inner)} chars between markers",
        )

    if new_text == text:
        return ReadmeRegenResult(
            path=readme,
            status="rebuilt",
            detail="no change",
        )

    readme.write_text(new_text, encoding="utf-8")
    return ReadmeRegenResult(
        path=readme,
        status="rebuilt",
        detail=f"rewrote {len(new_inner)} chars between markers",
    )


# ---------------------------------------------------------------------------
# Repair sub-passes
# ---------------------------------------------------------------------------


def _repair_filename_mismatch(
    node: Node, vault_path: Path, *, dry_run: bool
) -> list[RepairAction]:
    if not node.id:
        return []
    abs_path = vault_path / node.path
    expected_stem = node.id
    if abs_path.stem == expected_stem:
        return []
    new_path = abs_path.with_name(f"{expected_stem}.md")
    if new_path.exists():
        # Don't clobber a real other file. Leave for human resolution.
        return []
    action = RepairAction(
        code="renamed-to-match-id",
        node_id=node.id,
        path=node.path,
        detail=f"{abs_path.name} → {new_path.name}",
    )
    if not dry_run:
        abs_path.rename(new_path)
    return [action]


def _repair_missing_controlled_document(
    node: Node, vault_path: Path, *, dry_run: bool
) -> list[RepairAction]:
    spec = get_node_type(node.type)
    if spec is None:
        return []
    if not _is_risk_or_ifu(spec.folder):
        return []
    if "controlled_document" in node.frontmatter:
        return []
    action = RepairAction(
        code="set-controlled-document-false",
        node_id=node.id,
        path=node.path,
        detail="risk/IFU node was missing controlled_document; set to false",
    )
    if not dry_run:
        _set_frontmatter_field(
            vault_path / node.path, "controlled_document", False
        )
    return [action]


def _is_risk_or_ifu(folder: str) -> bool:
    folder = folder.replace("\\", "/")
    return folder.startswith("risk/") or folder == "entities/indications-for-use"


def _repair_missing_inverse_edges(
    node: Node, vault: Vault, vault_path: Path, *, dry_run: bool
) -> list[RepairAction]:
    inverses = _inverse_pairs()
    out: list[RepairAction] = []
    nodes_by_id = vault.nodes_by_id

    for edge in node.edges:
        inverse_type = inverses.get(edge.type)
        if inverse_type is None:
            continue
        target = nodes_by_id.get(edge.target)
        if target is None:
            continue
        already_present = any(
            e.target == node.id and e.type == inverse_type for e in target.edges
        )
        if already_present:
            continue
        action = RepairAction(
            code="added-inverse-edge",
            node_id=target.id,
            path=target.path,
            detail=f"added {inverse_type} → {node.id} (inverse of {edge.type})",
        )
        if not dry_run:
            _append_edge(
                vault_path / target.path,
                target=node.id,
                edge_type=inverse_type,
                weight=edge.weight,
                note=f"auto-added inverse of {edge.type} from {node.id}",
            )
        out.append(action)
    return out


# ---------------------------------------------------------------------------
# Decay sub-pass
# ---------------------------------------------------------------------------


def _maybe_decay(
    node: Node,
    vault_path: Path,
    nodes_by_id: dict[str, Node],
    today: date,
    *,
    dry_run: bool,
) -> DecayAction | None:
    if node.type != "fact":
        return None
    metric_id = node.frontmatter.get("metric_id")
    if not metric_id:
        return None
    metric = nodes_by_id.get(str(metric_id))
    if metric is None or metric.type != "metric":
        return None
    volatility = str(metric.frontmatter.get("volatility_class", ""))
    half_life = _HALF_LIFE_MONTHS.get(volatility)
    if half_life is None:
        return None

    verified_at = _coerce_date(node.frontmatter.get("verified_at"))
    if verified_at is None:
        return None
    age_months = _age_in_months(verified_at, today)
    if age_months <= 0:
        return None

    # Preserve the original confidence on first decay so re-runs are
    # idempotent (we always decay from the original, not from the decayed
    # value).
    original = node.frontmatter.get("confidence_original")
    if original is None:
        original = float(node.frontmatter.get("confidence", 1.0))
    else:
        original = float(original)

    decayed = original * (0.5 ** (age_months / half_life))
    decayed = max(0.0, min(1.0, decayed))
    # Round to 3 decimal places for stable, readable output.
    decayed = round(decayed, 3)

    current = float(node.frontmatter.get("confidence", 1.0))
    if abs(decayed - current) < 1e-4 and "confidence_original" in node.frontmatter:
        # Already decayed to this value; nothing to do.
        return None

    action = DecayAction(
        node_id=node.id,
        path=node.path,
        metric_id=str(metric_id),
        volatility_class=volatility,
        age_months=round(age_months, 1),
        confidence_before=current,
        confidence_after=decayed,
    )
    if not dry_run:
        _set_frontmatter_fields(
            vault_path / node.path,
            {
                "confidence": decayed,
                "confidence_original": original,
            },
        )
    return action


def _coerce_date(value: Any) -> date | None:
    if value is None:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None
    return None


def _age_in_months(verified_at: date, today: date) -> float:
    days = (today - verified_at).days
    return days / 30.4375  # average month length


# ---------------------------------------------------------------------------
# INDEX.md regeneration
# ---------------------------------------------------------------------------


def _render_readme_auto_section(vault: Vault, vault_path: Path) -> str:
    """Render the markdown that goes between the cb:auto markers."""

    lines: list[str] = [
        "## What's in this vault right now",
        "",
        "_This section is regenerated by `cb maintain repair` and `cb maintain "
        "rebuild-readme`. Edits inside the markers are overwritten — change "
        "vault content via `intake` / `atomize` and re-run maintain. Edits "
        "**outside** the markers are preserved._",
        "",
    ]

    # Stats line.
    type_counts: dict[str, int] = {}
    for node in vault.nodes:
        type_counts[node.type] = type_counts.get(node.type, 0) + 1
    n_nodes = len(vault.nodes)
    n_types = len(type_counts)
    lines.append(
        f"**Vault state:** {n_nodes} node{'s' if n_nodes != 1 else ''} "
        f"across {n_types} type{'s' if n_types != 1 else ''}. "
        f"Profile: `{vault.profile_name or 'default'}`."
    )
    lines.append("")

    if n_nodes == 0:
        lines.append(
            "_Newly scaffolded — no nodes yet. Run `intake` or `atomize` to "
            "start populating, then re-run `cb maintain repair`._"
        )
        return "\n".join(lines) + "\n"

    pillars = sorted(
        [n for n in vault.nodes if n.type == "pillar"], key=lambda n: n.id
    )
    auto_inject_pillars = [
        p for p in pillars if bool(p.frontmatter.get("auto_inject"))
    ]
    non_goal_pillars = [p for p in pillars if _is_non_goal_pillar(p)]
    positive_auto_inject = [p for p in auto_inject_pillars if p not in non_goal_pillars]

    if positive_auto_inject:
        lines.append("### Governing pillars (auto-injected)")
        lines.append("")
        for p in positive_auto_inject:
            title = str(p.frontmatter.get("title", p.id))
            lines.append(f"- [`{p.id}`]({p.path}) — {title}")
        lines.append("")

    if non_goal_pillars:
        lines.append("### Non-goal pillars")
        lines.append("")
        for p in non_goal_pillars:
            title = str(p.frontmatter.get("title", p.id))
            lines.append(f"- [`{p.id}`]({p.path}) — {title}")
        lines.append("")

    products = sorted(
        [n for n in vault.nodes if n.type == "product"], key=lambda n: n.id
    )
    if products:
        lines.append("### Products")
        lines.append("")
        for n in products:
            title = str(n.frontmatter.get("title", n.id))
            lines.append(f"- [`{n.id}`]({n.path}) — {title}")
        lines.append("")

    competitors = sorted(
        [n for n in vault.nodes if n.type == "competitor"], key=lambda n: n.id
    )
    if competitors:
        lines.append("### Competitors")
        lines.append("")
        for n in competitors:
            title = str(n.frontmatter.get("title", n.id))
            canonical_url = n.frontmatter.get("canonical_url")
            suffix = f" — <{canonical_url}>" if canonical_url else ""
            lines.append(f"- [`{n.id}`]({n.path}) — {title}{suffix}")
        lines.append("")

    # Latest exports table (sorted by filename for determinism; mtime
    # would make the README churn on every render even when content was
    # unchanged, which would defeat the idempotency contract elsewhere).
    exports_dir = vault_path / "exports"
    if exports_dir.is_dir():
        files = sorted(
            p for p in exports_dir.iterdir() if p.is_file() and not p.name.startswith(".")
        )
        if files:
            lines.append("### Latest exports")
            lines.append("")
            lines.append("| File | Size |")
            lines.append("|---|---:|")
            for f in files:
                lines.append(
                    f"| [`exports/{f.name}`](exports/{f.name}) | {_human_size(f.stat().st_size)} |"
                )
            lines.append("")

    return "\n".join(lines) + "\n"


def _is_non_goal_pillar(node: Node) -> bool:
    tags = node.frontmatter.get("tags") or []
    if isinstance(tags, list) and any(str(t).lower() == "non-goal" for t in tags):
        return True
    title = str(node.frontmatter.get("title", "")).strip().lower()
    return title.startswith("non-goal")


def _human_size(num_bytes: int) -> str:
    if num_bytes < 1024:
        return f"{num_bytes} B"
    if num_bytes < 1024 * 1024:
        return f"{num_bytes / 1024:.1f} KB"
    return f"{num_bytes / (1024 * 1024):.2f} MB"


def _write_index(vault: Vault, vault_path: Path) -> Path:
    target = vault_path / "_system" / "INDEX.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    content = _render_index(vault)
    target.write_text(content, encoding="utf-8")
    return target


def _render_index(vault: Vault) -> str:
    profile = vault.profile_name or "default"
    active_types = get_active_node_types(profile)
    nodes_by_type: dict[str, list[Node]] = {spec.name: [] for spec in active_types}
    for node in vault.nodes:
        if node.type in nodes_by_type:
            nodes_by_type[node.type].append(node)
    for bucket in nodes_by_type.values():
        bucket.sort(key=lambda n: n.id)

    lines: list[str] = [
        "# Master Node Index",
        "",
        "This file is regenerated by the `maintain` skill. Don't hand-edit — "
        "your changes will be overwritten by the next `cb maintain rebuild-index` "
        "or `cb validate --fix`.",
        "",
        f"**Active profile**: `{profile}`.",
        "",
        f"**Total nodes**: {len(vault.nodes)}.",
        "",
        "## Retrieval protocol",
        "",
        "1. Read summaries here and any pillar with `auto_inject: true` whose "
        "`applicable_when` matches the question.",
        "2. Load full bodies for surviving candidates and walk their `edges` "
        "frontmatter one hop. Most answers live within one or two hops.",
        "",
    ]

    by_category: dict[NodeCategory, list[tuple[str, list[Node]]]] = {
        c: [] for c in NodeCategory
    }
    for spec in active_types:
        by_category[spec.category].append((spec.name, nodes_by_type[spec.name]))

    category_titles = {
        NodeCategory.EPISTEMIC: "Epistemic nodes",
        NodeCategory.ENTITY: "Entity nodes",
        NodeCategory.PROFILE_CONDITIONAL: "Profile-conditional nodes",
    }
    for category in (
        NodeCategory.EPISTEMIC,
        NodeCategory.ENTITY,
        NodeCategory.PROFILE_CONDITIONAL,
    ):
        entries = [e for e in by_category[category] if e[1]]
        if not entries:
            continue
        lines.append(f"## {category_titles[category]}")
        lines.append("")
        for type_name, nodes in entries:
            lines.append(f"### `{type_name}` ({len(nodes)})")
            lines.append("")
            lines.append("| id | summary | confidence | verified_at |")
            lines.append("|---|---|---|---|")
            for node in nodes:
                summary = str(node.frontmatter.get("summary", "")).replace(
                    "|", "\\|"
                )
                confidence = node.frontmatter.get("confidence")
                conf_str = (
                    f"{float(confidence):.2f}"
                    if isinstance(confidence, (int, float))
                    else ""
                )
                verified = node.frontmatter.get("verified_at")
                verified_str = (
                    verified.isoformat()
                    if hasattr(verified, "isoformat") and not isinstance(verified, str)
                    else str(verified or "")
                )
                lines.append(
                    f"| `{node.id}` | {summary} | {conf_str} | {verified_str} |"
                )
            lines.append("")

    if len(vault.nodes) == 0:
        lines.append("_No nodes yet. Use the `intake` or `atomize` skill to add some._")
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Audit findings
# ---------------------------------------------------------------------------


def _audit_findings(vault: Vault) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    type_counts: dict[str, int] = {}
    for node in vault.nodes:
        type_counts[node.type] = type_counts.get(node.type, 0) + 1
    findings.append(
        AuditFinding(
            "info",
            "vault-size",
            f"vault holds {len(vault.nodes)} nodes across "
            f"{len(type_counts)} type(s).",
        )
    )
    if "source" not in type_counts:
        findings.append(
            AuditFinding(
                "notice",
                "no-sources",
                "no source nodes in the vault — claims can't derive from provenance.",
            )
        )
    if "pillar" not in type_counts:
        findings.append(
            AuditFinding(
                "notice",
                "no-pillars",
                "no pillar nodes in the vault — query has nothing to auto-inject.",
            )
        )
    return findings


# ---------------------------------------------------------------------------
# Frontmatter rewriting
# ---------------------------------------------------------------------------


def _set_frontmatter_field(path: Path, key: str, value: Any) -> None:
    _set_frontmatter_fields(path, {key: value})


def _set_frontmatter_fields(path: Path, updates: dict[str, Any]) -> None:
    """In-place rewrite of one or more frontmatter fields.

    Preserves the field order of fields that already exist; appends new
    fields at the end of the frontmatter block. The body is untouched.
    """

    text = path.read_text(encoding="utf-8")
    fm_text, body = split_frontmatter(text)
    if fm_text is None:
        raise ValueError(f"{path} has no frontmatter; refusing to rewrite")
    data = yaml.safe_load(fm_text) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} frontmatter is not a mapping")

    for k, v in updates.items():
        data[k] = v

    new_fm = yaml.safe_dump(data, sort_keys=False, allow_unicode=True).strip()
    path.write_text(f"---\n{new_fm}\n---\n{body}", encoding="utf-8")


def _append_edge(
    path: Path,
    *,
    target: str,
    edge_type: str,
    weight: float,
    note: str | None,
) -> None:
    """Append one edge entry to a node's frontmatter ``edges`` list."""

    text = path.read_text(encoding="utf-8")
    fm_text, body = split_frontmatter(text)
    if fm_text is None:
        raise ValueError(f"{path} has no frontmatter; cannot append edge")
    data = yaml.safe_load(fm_text) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} frontmatter is not a mapping")

    edges = data.get("edges") or []
    if not isinstance(edges, list):
        raise ValueError(f"{path} edges field is not a list")
    new_edge: dict[str, Any] = {
        "target": target,
        "type": edge_type,
        "weight": weight,
    }
    if note:
        new_edge["note"] = note
    edges.append(new_edge)
    data["edges"] = edges

    new_fm = yaml.safe_dump(data, sort_keys=False, allow_unicode=True).strip()
    path.write_text(f"---\n{new_fm}\n---\n{body}", encoding="utf-8")


# ---------------------------------------------------------------------------
# Errors / re-exports
# ---------------------------------------------------------------------------


__all__ = [
    "AuditFinding",
    "AuditReport",
    "DecayAction",
    "DecayResult",
    "ReadmeRegenResult",
    "RepairAction",
    "RepairResult",
    "VaultNotFoundError",
    "audit",
    "decay",
    "rebuild_index",
    "rebuild_readme",
    "repair",
]
