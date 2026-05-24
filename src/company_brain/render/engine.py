"""Jinja2 environment + branding loader for doc-generate.

The engine is responsible for:

* Loading the bundled template directory (``src/company_brain/templates/``).
* Letting a vault override any template by placing the same filename in
  ``<vault>/_branding/templates/``.
* Loading ``<vault>/_branding/colors.yaml`` (if present) into a typed
  :class:`Branding` value that the HTML and docx writers consume. The
  markdown writer ignores colors but does pick up the logo reference
  when one is present.

Template overrides win over bundled templates by name. ``mrd.md.j2`` in
``_branding/templates/`` will be picked instead of the shipped version.

I/O happens here; the render data-assembly modules import Jinja-rendered
strings from this module rather than the other way around.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any

import yaml
from jinja2 import ChoiceLoader, Environment, FileSystemLoader, StrictUndefined


_DEFAULT_BRANDING = {
    "primary": "#1f3a5f",
    "secondary": "#3b82c4",
    "accent": "#10b981",
    "text": "#1f2937",
    "background": "#ffffff",
    "muted": "#9ca3af",
    "font_family_headings": "Inter, Helvetica Neue, Arial, sans-serif",
    "font_family_body": "Source Serif Pro, Georgia, serif",
}


@dataclass(frozen=True)
class Branding:
    """Resolved branding for one render pass.

    Defaults come from :data:`_DEFAULT_BRANDING`. ``<vault>/_branding/colors.yaml``
    overrides any subset of fields. ``logo_path`` resolves to an absolute path
    on disk when a logo is present in ``_branding/``, else ``None``.
    """

    primary: str
    secondary: str
    accent: str
    text: str
    background: str
    muted: str
    font_family_headings: str
    font_family_body: str
    logo_path: Path | None

    def as_dict(self) -> dict[str, Any]:
        return {
            "primary": self.primary,
            "secondary": self.secondary,
            "accent": self.accent,
            "text": self.text,
            "background": self.background,
            "muted": self.muted,
            "font_family_headings": self.font_family_headings,
            "font_family_body": self.font_family_body,
            "logo_path": str(self.logo_path) if self.logo_path else None,
        }


def load_branding(vault_path: Path) -> Branding:
    """Load branding from ``<vault>/_branding/``.

    Missing folder or file is fine: defaults are used. Logo recognition
    checks for ``logo.png``, ``logo.jpg``, ``logo.jpeg``, ``logo.svg`` in
    that order.
    """

    branding_dir = vault_path / "_branding"
    overrides: dict[str, Any] = {}
    colors_file = branding_dir / "colors.yaml"
    if colors_file.is_file():
        try:
            data = yaml.safe_load(colors_file.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            data = None
        if isinstance(data, dict):
            overrides = data

    resolved = {**_DEFAULT_BRANDING, **{k: v for k, v in overrides.items() if v is not None}}
    logo_path: Path | None = None
    for ext in ("png", "jpg", "jpeg", "svg"):
        candidate = branding_dir / f"logo.{ext}"
        if candidate.is_file():
            logo_path = candidate.resolve()
            break

    return Branding(
        primary=str(resolved["primary"]),
        secondary=str(resolved["secondary"]),
        accent=str(resolved["accent"]),
        text=str(resolved["text"]),
        background=str(resolved["background"]),
        muted=str(resolved["muted"]),
        font_family_headings=str(resolved["font_family_headings"]),
        font_family_body=str(resolved["font_family_body"]),
        logo_path=logo_path,
    )


def build_environment(vault_path: Path) -> Environment:
    """Build a Jinja2 environment whose loader prefers vault overrides.

    Lookup order for ``env.get_template('mrd.md.j2')``:

    1. ``<vault>/_branding/templates/mrd.md.j2`` (if present).
    2. The bundled template directory packaged with company-brain.

    StrictUndefined is on so a typo'd context key surfaces as an error at
    render time, not as a silently empty string in the output.
    """

    bundled = _bundled_template_dir()
    loaders = []
    overrides_dir = vault_path / "_branding" / "templates"
    if overrides_dir.is_dir():
        loaders.append(FileSystemLoader(str(overrides_dir)))
    loaders.append(FileSystemLoader(str(bundled)))

    env = Environment(
        loader=ChoiceLoader(loaders),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        autoescape=False,
    )
    # Wrap a node id in `[id]` for inline citation. Used by the bullet-list
    # patterns in mrd.md.j2 where pre-built strings are easier than nested
    # for-loops fighting trim_blocks.
    env.filters["format_cite"] = lambda node_id: f"[{node_id}]"
    return env


def _bundled_template_dir() -> Path:
    """Return the absolute path to the bundled ``templates/`` directory.

    Uses ``importlib.resources`` so this works whether company-brain is
    imported from a source checkout or installed as a wheel.
    """

    # The `as_file` context returns a real path for both source and wheel
    # installs (in the wheel case it materializes a temp dir if needed).
    pkg_files = resources.files("company_brain") / "templates"
    return Path(str(pkg_files))
