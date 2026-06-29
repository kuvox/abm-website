#!/usr/bin/env python3
"""Replace site header navigation on every HTML page from site_nav.py."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from site_nav import detect_active, header, rel_prefix  # noqa: E402

HEADER_RE = re.compile(r"<header class=\"site-header\">.*?</header>", re.DOTALL)
SKIP_PARTS = frozenset({"snippets", "sessions"})


def main() -> None:
    updated = 0
    for path in sorted(ROOT.rglob("*.html")):
        if SKIP_PARTS.intersection(path.parts):
            continue
        text = path.read_text()
        if not HEADER_RE.search(text):
            continue
        rel = rel_prefix(path, ROOT)
        active = detect_active(path, ROOT)
        new_header = header(rel, active=active)
        new_text = HEADER_RE.sub(new_header, text, count=1)
        if new_text != text:
            path.write_text(new_text)
            updated += 1
            print(path.relative_to(ROOT))
    print(f"Updated {updated} file(s).")


if __name__ == "__main__":
    main()
