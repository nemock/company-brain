---
profile: medical-device
profile_version: 1.0
scaffolded_at: 2026-05-25
scaffolded_by_company_brain_version: 0.5.0
controlled_document: false
---

# Vault Profile

This vault uses the **medical-device** profile.

Adds indications-for-use, regulatory clearances, and ISO-14971-vocabulary risk node types. Every generated document carries the controlled-document-boundary footer.

## Activated profile-conditional node types

- `indication-for-use`
- `regulatory-clearance`
- `risk-insight`
- `hazard`
- `hazardous-situation`
- `harm`
- `risk-control-idea`
- `regulation`
- `standard`

## Profile notes

- All risk/ and indications-for-use nodes carry controlled_document: false.
- Predicate chains and IFU history use preceded_by / followed_by edges.

## Document generation

Every document generated for this vault carries the controlled-document-boundary footer.

## Lifecycle

The profile is set at vault creation and not designed to be flipped in place. Re-scaffolding into the same directory with a different profile will leave orphan folders from the previous profile.

## Schema source of truth

This file is human-readable; the authoritative schema lives in the [company-brain Python package](https://github.com/nemock/company-brain) under `src/company_brain/schema/`. The companion docs `_system/NODE-TYPES.md`, `_system/EDGE-TYPES.md`, and `_system/FRONTMATTER-SCHEMA.md` are rendered from that source.
