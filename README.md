# company-brain

> ⚠️ **Pre-1.0, under active development.** APIs, schema, and skill interfaces will change without notice. Watch [ROADMAP.md](ROADMAP.md) for milestones.

An AI-native knowledge graph for companies — products, people, decisions, vision, evidence, competitive landscape — that lives in Obsidian-compatible markdown and lets agents retrieve cheaply from typed nodes and typed edges.

Built as a set of Claude Code skills plus a Python CLI. Industry-agnostic core with an opt-in **medical-device** profile that adds indications-for-use, regulatory clearances, and ISO-14971-vocabulary risk nodes — all explicitly **above** any design controls layer.

## Status

Current milestone: **v0.3.0 — Query, MRD, and one-pager.** The pipeline now goes end-to-end: scaffold a vault, capture knowledge via `intake`, ingest existing docs via `atomize`, query the graph via `query`, and generate a real MRD or one-pager via `doc-generate`.

- [PRD.md](PRD.md) — design spec.
- [ROADMAP.md](ROADMAP.md) — milestone sequencing.
- [docs/controlled-document-boundary.md](docs/controlled-document-boundary.md) — what company-brain is **not**.

## What's here today

- **Schema** — typed nodes, typed edges, source kinds, industry profiles (medical-device + default).
- **CLI** — `cb scaffold`, `cb validate`, `cb describe-profile`, `cb describe-node`, `cb extract`, `cb list-nodes`, `cb get-node`, `cb render`, `cb install-skills`.
- **Skills** — `vault-architect`, `intake` (vision / product / competitor / metric / meeting-notes / risk / clearance sub-modes), `atomize` (markdown / Word / PDF / transcript / image), `query` (IB retrieval analyst), `doc-generate` (MRD + one-pager, profile-aware, markdown / html / docx).
- **Example vault** — `examples/meddev-fictional/` exercises every node type in the medical-device profile; pre-generated MRD and one-pager live in `exports/`.
- Placeholders for the two skills that land in v0.4.0 (`maintain`, `visualize`).

## What's coming

See [ROADMAP.md](ROADMAP.md) for the full milestone list. Highlights:

- **v0.1.0** — ✅ schema definitions, `vault-architect` skill, hand-built medical-device example vault, `cb validate`.
- **v0.2.0** — ✅ `intake` (vision + product + competitor sub-modes), `atomize` (markdown / Word / PDF / transcripts / image screenshots).
- **v0.3.0** — ✅ `query` + MRD generator (profile-aware, evidence-vs-vision split, IFU comparison, anti-decisions section) + one-pager + markdown / html / docx output.
- **v0.4.0** — `visualize` + `maintain` + scaffold generators for PID, business plan, competitive brief, risk brainstorm.
- **v1.0.0** — public release tag and announcement.

## License

MIT. See [LICENSE](LICENSE).

## Inspiration

- The Infinite Brain pattern (atomic typed nodes + typed edges + frontmatter summaries + agent-readable system index).
- [graphify](https://github.com/safishamsi/graphify) — Python CLI shape, D3.js viewer, "god nodes" analytics. (graphify analyzes source code; company-brain analyzes company knowledge.)
- [obsidian-infinite-brain](https://github.com/JotaSXBR/obsidian-infinite-brain) — five-skill decomposition.
