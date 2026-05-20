---
name: atomize
description: Ingest existing documents (markdown, Word, PDF, transcripts, image screenshots) into typed nodes with provenance. Each ingested document lands as an immutable source node; extracted content becomes derived typed nodes linked via derived_from.
---

# atomize

> Placeholder skill. Implementation lands across v0.2.0 (markdown, Word, PDF, transcripts, images).

v1 input formats:

- **Markdown / plain text** — always.
- **Word (`.docx`)** — for ingesting existing project initiation documents, drafts, and outlines.
- **PDF** — text + simple tables. Recognizes pasted-in FDA 510(k) summary PDFs and extracts IFU, predicates, product codes automatically.
- **Interview transcripts** (txt with timestamps) — claim extraction, quote attribution, persona signal extraction.
- **Image screenshots** (PNG/JPG) — for web captures. Uses Claude vision to extract visible text.

v1.x adds: PowerPoint (`.pptx`).

See [PRD.md §10](../../PRD.md) for the ingest-from-other-skills convention and design detail.
