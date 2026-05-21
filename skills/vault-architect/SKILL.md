---
name: vault-architect
description: Scaffold a new company-brain vault. Use ONCE when starting a new vault. Confirms the target directory and industry profile, then runs `cb scaffold` to create the folder tree, _attachments/, exports/, and the _system reference files (PROFILE.md, INDEX.md, NODE-TYPES.md, EDGE-TYPES.md, FRONTMATTER-SCHEMA.md). Does NOT write node content — that is the job of intake and atomize.
---

# vault-architect

This skill scaffolds a new company-brain vault. Run it once per vault. It delegates the actual work to the `cb scaffold` CLI command so the on-disk shape stays single-sourced with the schema package.

## When to use

- The user is creating a brand-new company-brain vault.
- The user wants to refresh `_system/*.md` after upgrading company-brain (use `--force`).

## When NOT to use

- The user already has a vault and wants to add knowledge — point them at the `intake` or `atomize` skills.
- The user wants to change a vault's profile after the fact — that requires re-scaffolding into a new directory and migrating content by hand. The profile is not designed to be flipped in place.

## Workflow

### 1. Confirm with the user

Ask, in order:

1. **Target directory.** Where should the vault live? Default to the current working directory if the user doesn't specify. Resolve to an absolute path before passing to the CLI.
2. **Profile.** Which industry profile? Offer these choices with brief explanations:
   - `medical-device` — patient-facing devices regulated by FDA / MDR / etc. Activates indications-for-use, regulatory-clearance, and ISO-14971-vocabulary risk node types. Generated documents carry the controlled-document-boundary footer.
   - `default` — industry-agnostic. Only the epistemic and entity node types are active.
   - `saas`, `hardware`, `services` — reserved slots. In v1 these behave like `default`; content lands in v2.

If the target directory already contains a vault (i.e. `_system/PROFILE.md` exists), tell the user. Offer to re-run with `--force` if they want to regenerate the system docs after a company-brain upgrade.

### 2. Run the command

```bash
cb scaffold --profile <name> --path <dir>
```

For refresh after an upgrade:

```bash
cb scaffold --profile <name> --path <dir> --force
```

### 3. Report results

The CLI prints a structured summary. Read it back to the user, then add:

- A reminder of the activated profile-conditional types (if any) so they know what's available.
- The next step: add knowledge via `intake vision` (for a dictation-friendly first pass) or `atomize` (for ingesting existing documents).
- The controlled-document-boundary reminder if the profile is `medical-device`.

## Worked examples

### Starting a medical-device vault

```bash
cb scaffold --profile medical-device --path /Users/jane/work/acme-monitor-vault
```

Expected: 34 folders, 5 `_system` files, activated profile-conditional types listed in `_system/PROFILE.md`.

### Refreshing system docs after upgrade

```bash
cb scaffold --profile medical-device --path /Users/jane/work/acme-monitor-vault --force
```

This overwrites the five `_system/*.md` files but does not touch any node files, attachments, or exports.

## Constraints

- This skill never writes node content. Refuse politely if asked to add a pillar, decision, fact, etc. — that is the intake/atomize skills' job.
- This skill never runs `cb validate`. Mention that the user can run it themselves once nodes exist.
- This skill never modifies an existing PROFILE.md to switch profiles. Doing so silently would leave orphan folders and break retrieval. If the user wants a different profile, scaffold a new vault.
