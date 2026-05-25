# _branding/

Holds the company's brand assets for use by the `doc-generate` skill. Committed to git so all team members see the same brand on regenerated documents.

## Files

- `colors.yaml` — palette and typography. Edit to match your company's brand.
- `logo.png` (optional) — primary logo used in document headers. Drop in if you have one.
- `templates/` (optional) — jinja2 template overrides for specific documents. company-brain ships defaults; this folder lets you override.

## Used by

`doc-generate` reads from this folder when rendering MRD, PID, business plan, etc., to produce documents that match the company's brand.

## Convention

Anything in `_branding/` is committed by default. The folder is intentionally small — a logo, a colors file, optional templates. Heavier shared assets belong in `_attachments/`.
