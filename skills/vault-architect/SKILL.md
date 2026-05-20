---
name: vault-architect
description: Scaffold a new company-brain vault for a given industry profile. Creates the folder structure, _system files, and an initial PROFILE.md. Use this once when starting a new vault.
---

# vault-architect

> Placeholder skill. Implementation lands in v0.1.0.

This skill will scaffold a complete company-brain vault for a chosen industry profile (`medical-device`, `default`, etc.), including:

- All required folders (epistemic, entity, profile-conditional risk, `_system`, `_attachments`, `exports`).
- `_system/PROFILE.md` declaring the active profile.
- `_system/INDEX.md` (initially empty).
- `_system/NODE-TYPES.md`, `EDGE-TYPES.md`, `FRONTMATTER-SCHEMA.md` populated from the schema in `src/company_brain/schema/`.

See [PRD.md §6 and §8](../../PRD.md) for design detail and [ROADMAP.md](../../ROADMAP.md) v0.1.0 for sequencing.
