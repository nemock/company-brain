# _branding/

Vitalisens (fictional) brand assets. In a real vault, this folder would also typically contain a `logo.png` and possibly `templates/` overrides. Here we ship only `colors.yaml` and this README — enough to demonstrate the convention without requiring an invented logo.

## Files

- `colors.yaml` — palette and typography for generated documents.
- `logo.png` (would go here in a real vault).
- `templates/` (would hold jinja2 overrides if the company wanted to customize the MRD, PID, etc.).

## Used by

`doc-generate` reads from this folder when rendering MRD, PID, business plan, etc., to produce documents that match the company's brand.

## Convention

Anything in `_branding/` is committed by default. The folder is intentionally small — a logo, a colors file, optional templates. Heavier shared assets belong in `_attachments/`.
