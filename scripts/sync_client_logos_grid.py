#!/usr/bin/env python3
"""Replace client logo grid blocks site-wide from client_logos_grid.py."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from client_logos_grid import client_logos_grid  # noqa: E402
from site_nav import rel_prefix  # noqa: E402

SNIPPET_PATH = ROOT / "snippets" / "client-logos-grid.html"
SHELL_MARKER = '<div class="client-collage-shell">'

ORPHAN_OLD_LOGOS = re.compile(
    r'(\s*<div class="logo-item" tabindex="0">.*?logo-tooltip-blurb.*?</div>\s*)+'
    r'(?:\s*\n)*(?:\s*</div>\s*){1,3}(?=\s*\n)',
    re.DOTALL,
)

SNIPPET_HEADER = """<!--
  CANONICAL client logo grid — source of truth: client_logos_grid.py
  Regenerate: python3 scripts/sync_client_logos_grid.py
  See client-logos.md for usage.

  Root-level pages: images/website-logos/website-client-logos/...
  Nested pages: ../images/website-logos/website-client-logos/...
-->
"""


def _div_block_bounds(text: str, marker: str) -> tuple[int, int] | None:
    """Return (start, end) indices for a balanced <div>…</div> block."""
    start = text.find(marker)
    if start == -1:
        return None
    depth = 0
    i = start
    while i < len(text):
        open_pos = text.find("<div", i)
        close_pos = text.find("</div>", i)
        if close_pos == -1:
            return None
        if open_pos != -1 and open_pos < close_pos:
            depth += 1
            i = open_pos + 4
            continue
        depth -= 1
        i = close_pos + len("</div>")
        if depth == 0:
            return (start, i)
    return None


def _replace_collage_shell(text: str, block: str) -> str:
    bounds = _div_block_bounds(text, SHELL_MARKER)
    if bounds is None:
        return text
    start, end = bounds
    return text[:start] + block + text[end:]


def _remove_orphan_old_logos(text: str) -> str:
    return ORPHAN_OLD_LOGOS.sub("\n", text)


def main() -> None:
    SNIPPET_PATH.write_text(SNIPPET_HEADER + client_logos_grid() + "\n")
    print(f"updated {SNIPPET_PATH.relative_to(ROOT)}")

    updated = 0
    for path in sorted(ROOT.rglob("*.html")):
        if "snippets" in path.parts:
            continue
        text = path.read_text()
        if SHELL_MARKER not in text and "logo-tooltip-blurb" not in text:
            continue
        rel = rel_prefix(path, ROOT)
        block = client_logos_grid(rel)
        new_text = _replace_collage_shell(text, block)
        new_text = _remove_orphan_old_logos(new_text)
        if new_text != text:
            path.write_text(new_text)
            updated += 1
            print(path.relative_to(ROOT))

    print(f"Updated {updated} HTML file(s).")


if __name__ == "__main__":
    main()
