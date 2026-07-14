#!/usr/bin/env python3
"""One-off site patch: include scripts/site-nav.js (mobile nav close/scroll-lock
behavior) on every page that has the site header. Safe to re-run — skips pages
that already have the include."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from site_nav import rel_prefix  # noqa: E402

HEADER_RE = re.compile(r"<header class=\"site-header\">")
SKIP_PARTS = frozenset({"snippets", "sessions"})


def main() -> None:
    updated = 0
    for path in sorted(ROOT.rglob("*.html")):
        if SKIP_PARTS.intersection(path.parts):
            continue
        text = path.read_text()
        if not HEADER_RE.search(text):
            continue
        if "scripts/site-nav.js" in text:
            continue
        rel = rel_prefix(path, ROOT)
        tag = f'<script src="{rel}scripts/site-nav.js" defer></script>\n'
        if "</body>" in text:
            new_text = text.replace("</body>", tag + "</body>", 1)
        else:
            new_text = text + "\n" + tag
        if new_text != text:
            path.write_text(new_text)
            updated += 1
            print(path.relative_to(ROOT))
    print(f"Updated {updated} file(s).")


if __name__ == "__main__":
    main()
