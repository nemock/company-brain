"""Document generation.

Sub-modules:

* :mod:`engine` — Jinja2 environment + branding loader.
* :mod:`mrd` — MRD generator (v0.3.0).
* :mod:`one_pager` — one-pager generator (v0.3.0, sub-piece 3).

Output formats supported by ``cb render`` land alongside these modules:
markdown is in v0.3.0 sub-pieces 2 and 3; docx and html arrive in sub-piece 4.
"""

from .engine import Branding, build_environment, load_branding
from .mrd import RenderResult, render_mrd
from .one_pager import render_one_pager
from .scaffolds import (
    SCAFFOLD_REGISTRY,
    ScaffoldProfileError,
    list_scaffold_names,
    render_scaffold,
)

__all__ = [
    "Branding",
    "RenderResult",
    "SCAFFOLD_REGISTRY",
    "ScaffoldProfileError",
    "build_environment",
    "list_scaffold_names",
    "load_branding",
    "render_mrd",
    "render_one_pager",
    "render_scaffold",
]
