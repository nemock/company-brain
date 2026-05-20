# Controlled-Document Boundary

> This is the explicit statement of what company-brain is **not**. Read it before using company-brain in any regulated context.

## What company-brain produces

Planning artifacts: marketing requirements documents, project initiation documents, business plans, competitive briefs, risk brainstorms, knowledge-graph nodes, queries, audit reports.

Every node carries a `controlled_document: false` frontmatter field. When the `medical-device` profile is active, every generated document also carries a footer disclaimer:

> This is a planning artifact. It is not a controlled document and is not part of any design history file, risk management file, or traceability matrix per ISO 14971, IEC 62304, or 21 CFR 820.

## What company-brain does NOT produce

- Signed and dated design history file (DHF) records.
- Risk management files per ISO 14971.
- Traceability matrices linking user needs to design inputs, design outputs, verification, and validation.
- Verification and validation (V&V) protocols.
- Documents intended for regulatory submission (510(k), De Novo, PMA, CE Tech File, etc.).
- Any document under formal change control as part of a quality management system.

## Why this boundary exists

For medical-device companies, design controls require:

1. Records produced under a controlled process (training records, approval signatures, change control).
2. Auditable traceability between user needs, design inputs, design outputs, V&V, and risk controls.
3. Document control with versioning, distribution, and retention per 21 CFR 820.40 or equivalent.

company-brain does none of this. It is designed for the planning thinking that happens *above* the design controls layer — thinking that informs what controlled records will eventually need to say, but is itself a different category of artifact.

Treating a planning artifact as a controlled record (or vice versa) creates regulatory risk. The boundary is enforced by:

- The `controlled_document: false` flag on every node and exported document.
- The footer disclaimer on every medical-device-profile output.
- The folder structure (`risk/`, `entities/indications-for-use/`) that signals "this is planning territory."
- This document, which adopters should read before using company-brain in a regulated context.

## What to do if a planning artifact should become a controlled record

Treat company-brain output as **input** to your controlled documentation process, not as the controlled documentation itself. The typical flow is:

1. A team uses company-brain to draft planning artifacts (MRD, PID, risk brainstorm).
2. The team identifies what content from those drafts should enter the controlled documentation.
3. The content is re-authored or re-formatted inside the controlled documentation system (eQMS, document control system, etc.), under that system's change control, approval, and traceability rules.
4. The controlled document goes through the QMS process; the planning artifact stays in company-brain as historical context.

Do not export a company-brain document and submit it as a controlled record. Do not edit a company-brain export inside an eQMS to make it look controlled. The boundary protects both the planning work (it stays exploratory) and the regulated work (it stays clean).

## Disclaimer

company-brain is provided "as is" under the MIT license. Nothing in this project constitutes regulatory advice. Adopters in regulated industries are responsible for their own compliance with applicable laws, regulations, and quality system requirements.
