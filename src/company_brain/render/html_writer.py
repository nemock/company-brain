"""Branded HTML output for generated documents.

Wraps the rendered markdown body inside a minimal but branded HTML
document. The wrapper template lives at ``templates/html-wrapper.html.j2``;
overriding it via ``<vault>/_branding/templates/html-wrapper.html.j2`` lets
a company control the entire page chrome.

The markdown body is converted to HTML via ``markdown-it-py`` (already a
transitive dependency through ``rich``). We enable the GFM-style table
plugin so the MRD's tables render as real HTML tables.
"""

from __future__ import annotations

from pathlib import Path

from markdown_it import MarkdownIt

from .engine import Branding, build_environment


def render_html(
    *,
    title: str,
    body_markdown: str,
    branding: Branding,
    vault_path: Path,
) -> str:
    """Render branded HTML around the given markdown body.

    ``vault_path`` is passed in so the Jinja loader can pick up any
    ``_branding/templates/html-wrapper.html.j2`` override the vault provides.
    """

    md = MarkdownIt("commonmark").enable("table")
    body_html = md.render(body_markdown)

    env = build_environment(vault_path)
    template = env.get_template("html-wrapper.html.j2")

    return template.render(
        title=title,
        body_html=body_html,
        branding=branding.as_dict(),
    )
