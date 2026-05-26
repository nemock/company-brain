---
title: "Spec — `research-agent` skill"
status: draft
version: 0.1.0
date: 2026-05-26
target_milestone: v1.x
controlled_document: false
---

# Spec: `research-agent` skill

> **Purpose.** Lock the design for the second roadmap target out of the Aha! deep-dive analysis. Pairs with the `strategic-model` spec: research-agent gathers competitive and market intelligence into the vault as typed nodes; strategic-model generators consume those nodes.
>
> **Target milestone.** v1.x. Sequence: ship research-agent before strategic-model so the dogfood loop is intact at the strategic-model release.

---

## 1. Overview

A new Claude Code skill — `research-agent` — that takes a research question + scope and dispatches parallel web research, returning typed nodes written to the vault with full provenance. The skill replaces the hand-orchestrated parallel-agent pattern used to produce the May 2026 competitive brief: instead of the project owner manually dispatching five parallel `general-purpose` agents and synthesizing findings into a single document, the skill does the dispatch, captures the output as typed nodes, and leaves the synthesis to a downstream generator (`competitive-brief`, `swot`, `magic-quadrant`).

## 2. Why it pairs with strategic-model

The Aha! deep-dive identified strategic-model + research-agent as the most asymmetric v1.x move. The pairing is the dogfood loop:

```
[research-agent skill]
  ├── User: "Survey our top 5 competitors' IFU evolution over 5 years"
  ├── Dispatches WebFetch / WebSearch in parallel
  └── Writes typed nodes back to vault:
        competitor-x, competitor-y, ...
        indication-for-use-x-2021, ...-2023, ...-2025 (chained preceded_by)
        regulatory-clearance-K231234 (with predicate edges)
        source-fda-510k-K231234 (with derived_from edges)
              ↓
[strategic-model generator]
  └── cb render swot --subject our-product
        ├── Walks the newly-captured competitor + IFU + clearance nodes
        └── Renders SWOT.md with cited sources
```

Today (May 2026) this loop is half-built: company-brain has the schema for typed nodes but the agent that writes them at research time doesn't exist; the `competitor-profiling` skill that does adjacent work doesn't write directly into vault format.

## 3. Skill triggering

`research-agent` activates on natural-language prompts including:

- "Research [topic / question]"
- "Investigate competitor [name]"
- "Survey the [category] landscape"
- "Deep dive on [topic]"
- "Refresh our intelligence on [competitor]"
- "What do we know about [topic]?" (when the answer requires net-new external research, not just `query`)

It does **not** activate on:

- "Query the vault for X" (use `query`)
- "Ingest this file" (use `atomize`)
- "Talk to me about my vision" (use `intake vision`)

The skill loader matches descriptions; the SKILL.md description must include the trigger phrases.

## 4. Inputs

The skill takes:

| Parameter | Required | Description |
|---|---|---|
| `question` | yes | Natural-language research question. |
| `scope` | yes (with default) | One or more of: `competitor`, `market`, `regulatory`, `customer`, `standard`, `general`. Defaults to inferring from the question. |
| `time_horizon` | optional | `current` (default) / `historical` / `longitudinal`. Drives whether to capture multiple time-pointed snapshots (relevant for IFU history, predicate chains). |
| `depth` | optional | `light` (5-10 sources, ~5 minutes) / `medium` (10-20 sources, ~15 minutes) / `deep` (20-50 sources, ~30 minutes). Defaults to `medium`. |
| `target_competitors` | optional | Explicit list of competitor names or canonical URLs to scope research. If absent, the skill identifies competitors from the question. |
| `vault_path` | implicit | Always the active vault. |

## 5. Outputs

### 5.1 Typed nodes the skill writes

| Node type | When written | Source kind chain |
|---|---|---|
| `source` | Always — at least one per net-new piece of external information | `web-snapshot`, `press-release`, `fda-510k-summary`, `market-data`, `citation`, or `web-snapshot-network` depending on what was captured |
| `competitor` | When a new competitor entity is identified | (entities don't have `source_kind`) |
| `indication-for-use` | Medical-device profile only, when an IFU is captured | — |
| `regulatory-clearance` | Medical-device profile only, when a 510(k) / De Novo / PMA / clearance event is captured | — |
| `note` | One per research run — a research-finding note summarizing the run with citations to the typed nodes written | — |

### 5.2 Provenance discipline

- **Every** captured fact lands in a `source` node first. Entity nodes (competitor, IFU, clearance) reference source nodes via `derived_from` edges.
- **No claim ever ships without a source node behind it.** This mirrors the vision-vs-evidence pillar.
- **The research run itself becomes a source node** of `source_kind: skill-output` with `producing_skill: research-agent` and a body containing the research transcript / log.

### 5.3 The summary note

After every research run, the skill writes a `note` node — call it `note-research-<topic>-<date>` — containing:

- The original question
- The scope used
- A concise summary of what was found (200-400 words)
- A list of all typed nodes created or updated in this run, with their ids
- A list of open follow-up questions the research surfaced

This note is itself a queryable node — `cb get-node note-research-cardiac-monitor-landscape-2026-05` returns the summary + everything derived from it.

## 6. The research dispatch model

The skill dispatches sub-agents in parallel — exactly the pattern hand-orchestrated for the May 2026 competitive brief. Specifically:

1. **Decomposition phase.** The skill parses the question and decomposes it into 3-7 sub-questions, each mapped to a research category (general wikis, second-brain tools, medical-device eQMS, AI PRD tools, direct competitors — as concrete examples from the May 2026 run).
2. **Parallel dispatch phase.** Each sub-question becomes a parallel sub-agent invocation (using the `Agent` tool internally) with WebFetch + WebSearch access. Each sub-agent returns structured findings.
3. **Synthesis phase.** The skill merges findings, deduplicates against existing vault nodes, identifies what's net-new vs. what updates an existing node, and proposes a batch of typed-node writes for user review.
4. **Review phase.** The skill presents the batch in tabular form (one row per proposed node, with type / id / one-line summary / source citation). User accepts / edits / rejects.
5. **Write phase.** Accepted nodes are written. Each gets a `derived_from` edge to the source node(s) that informed it. The research-run note is written last with references to every node created.

## 7. Termination criteria

The skill stops dispatching new sub-agents when:

- **The question is sufficiently answered.** LLM judgment after the synthesis phase — does the current node set cover the question?
- **Diminishing returns detected.** If the last two sub-agent batches produced mostly duplicates of existing vault nodes, stop.
- **Depth budget exhausted.** `light` / `medium` / `deep` parameter maps to a sub-agent count budget; exceed it and stop.
- **Source-domain saturation.** If the same 5 source domains are recurring across sub-agents, broaden or stop.

The skill does **not** stop on:

- Time elapsed (no wall-clock limit; budget is measured in sub-agent invocations).
- User idle (the skill runs to completion without prompting).

## 8. Integration with `atomize` and `intake`

- **The research-run note is a `source` node** with `source_kind: skill-output` and `producing_skill: research-agent`. This means the existing `atomize` "ingest-from-other-skills" convention recognizes the structure and routes content correctly if a user wants to re-process it later.
- **Sub-mode of `intake`?** No. `research-agent` is its own skill, not a sub-mode of intake. `intake` is for conversational human-driven capture; `research-agent` is for autonomous web-research dispatch. Two different shapes.
- **Hand-off to `strategic-model`.** The summary note's body should include a recommended next step like: *"To generate a SWOT against this competitor set, run `cb render swot --subject our-product --as-of <date>`."*

## 9. Skill structure (SKILL.md outline)

```
---
name: research-agent
description: When the user wants to research a topic, investigate a
  competitor, survey a landscape, or refresh competitive intelligence
  by dispatching parallel web research and capturing findings as typed
  vault nodes. Use when the user mentions "research X," "investigate Y,"
  "deep dive on Z," "survey the landscape," or "what do we know about W."
  NOT for querying existing vault knowledge (use query) or ingesting a
  specific file (use atomize).
---

# research-agent

## When to invoke

[Detailed trigger phrases and disambiguation from query / atomize / intake.]

## The flow

### 1. Question parsing

[Decomposition into sub-questions; mapping to research categories.]

### 2. Parallel dispatch

[Sub-agent invocation pattern. Use the Agent tool with general-purpose
subagent_type for each sub-question. Pass a structured prompt template
that produces structured findings.]

### 3. Synthesis and dedup

[Merge findings; check against existing vault nodes via cb list-nodes;
identify net-new vs. updates.]

### 4. Batched review

[Present table of proposed nodes; collect user accept/edit/reject.]

### 5. Write phase

[Write nodes; create derived_from edges; write the research-run note.]

## Output guarantees

- Every captured fact has a `source` node.
- Every entity node has at least one `derived_from` edge to a source.
- The research-run note links to every node created.
- No claim ships uncited.

## Profile awareness

- `default` profile: captures `competitor`, `source`, `note`. No
  medical-device-specific types.
- `medical-device` profile: also captures `indication-for-use`,
  `regulatory-clearance` with predicate edges where applicable.

## Disambiguation from related skills

- `competitor-profiling` (existing): also profiles competitors but
  outputs a single markdown profile per competitor, not typed nodes.
  research-agent supersedes for vault-resident workflows but stays
  compatible — research-agent recognizes competitor-profiling output
  via the atomize convention.
- `customer-research`: focused on customer interview synthesis;
  different inputs (transcripts) and outputs (personas, insights).
- `query`: read-only over the vault; does not dispatch external research.
```

## 10. Test cases

The skill should produce valid output on at minimum these scenarios:

1. **"Research the top 5 medical device wearables companies."**
   - Expected: 5 competitor nodes; for each, 1-3 indication-for-use nodes; for each, 0-2 regulatory-clearance nodes; 10-25 source nodes (web-snapshot, fda-510k-summary, press-release); 1 research-run note.
   - Validates: medical-device profile coverage; predicate-edge resolution; competitor disambiguation by canonical URL.

2. **"Investigate competitor X and capture their IFU evolution."**
   - Expected: 1 competitor node updated; 2-5 indication-for-use nodes chained by `preceded_by`/`followed_by`; supporting source nodes; 1 research-run note.
   - Validates: time-horizon `longitudinal`; IFU history chain construction.

3. **"Survey the OKR-tool landscape."**
   - Expected: 5-10 competitor nodes; market-data source nodes; 1 research-run note. No IFU, no clearance (default profile).
   - Validates: default-profile behavior; competitor identification from a fresh question.

4. **"What's the regulatory clearance picture for cardiac monitors in 2025?"**
   - Expected: 5-15 regulatory-clearance nodes (most cleared in 2024-2025); supporting fda-510k-summary source nodes; 1 research-run note.
   - Validates: medical-device profile depth; clearance disambiguation by K-number.

5. **Re-run of test 1 after 90 days.**
   - Expected: most existing nodes left untouched (deduped); 0-3 new IFU nodes if any competitor had a new clearance in the interim; 0-2 new competitor nodes if new entrants emerged; 1 new research-run note referencing the prior run.
   - Validates: dedup correctness; idempotency; longitudinal node growth.

## 11. Open questions

1. **Does the skill have a write-budget per run?** I.e., can it write 500 nodes in a single research run, or should it be capped? Recommendation: cap at ~50 nodes per run by default with a `--allow-large-runs` override.

2. **Sub-agent context budget.** Each parallel sub-agent has its own context window. How does the skill handle a sub-agent that hits the limit before completing? Recommendation: graceful degradation — the sub-agent returns what it has, the orchestrator notes the truncation in the research-run note.

3. **Authentication for sources that require it.** WebFetch on a paywalled FDA-related source, a Crunchbase profile, or a LinkedIn page won't work. Recommendation: skill notes which sources required auth and asks the user to capture them manually via `atomize`.

4. **Cost / rate limiting.** Parallel WebFetch + WebSearch + downstream LLM token cost is real. The `depth` parameter (light / medium / deep) approximates a budget but doesn't track actual cost. Recommendation: surface estimated cost in the synthesis phase before the write phase commits.

5. **Edge construction in the medical-device profile.** When the skill captures a regulatory-clearance with declared predicates, the predicate may not have been ingested yet. Recommendation: write the edge with a warning; rely on `cb validate --fix` to resolve later or warn about unresolved predicates.

6. **Skill chaining.** Should `research-agent` automatically invoke `strategic-model` generation when the user's question implies it (e.g., "what's the competitive landscape?" → research-agent + SWOT)? Recommendation: no, keep skills atomic; the research-run note's body recommends the follow-up command.

## 12. Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| 0.1.0 | 2026-05-26 | nemock + Claude | Initial spec. Locks the design for the v1.x companion to the strategic-model spec. Defines triggering, inputs, outputs, dispatch model, termination criteria, integration with existing skills. Six open questions to resolve before code lands. |
