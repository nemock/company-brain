"""company-brain CLI entry point.

v0.1.0 ships a stub so the package is installable. Real commands land per the roadmap:
  - cb validate          (v0.1.0)
  - cb render <doc>      (v0.3.0)
  - cb viewer            (v0.4.0)
  - cb fetch <url>       (v1.x)
  - cb intake-510k <K>   (v1.x)
"""

from __future__ import annotations

import sys

from . import __version__


BANNER = f"""company-brain {__version__}

Pre-1.0, under active development. No usable commands yet.

See:
  https://github.com/nemock/company-brain
  ROADMAP.md for milestone sequencing
  PRD.md for design
"""


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if args and args[0] in {"-V", "--version"}:
        print(__version__)
        return 0
    print(BANNER, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
