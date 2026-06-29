#!/usr/bin/env python3
"""Replace case study preview sections site-wide from case_studies_section.py."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from case_studies_section import case_studies_section  # noqa: E402
from site_nav import rel_prefix  # noqa: E402

SKIP_PARTS = frozenset({"snippets", "sessions"})

SECTION_PATTERNS = [
    re.compile(r"<!-- =+ CASE STUDIES(?: PREVIEW)? =+ -->.*?</section>", re.DOTALL),
    re.compile(
        r'<section class="section section--alt" id="case-studies-preview">.*?</section>',
        re.DOTALL,
    ),
    re.compile(
        r'<section class="section section--alt client-case-studies-section">.*?</section>',
        re.DOTALL,
    ),
    re.compile(
        r'<section class="section">\s*<div class="container grid-2">\s*<a class="case-card".*?</section>',
        re.DOTALL,
    ),
]

H1_RE = re.compile(r"<h1>Client Case Studies</h1>")
H1_RE_ALT = re.compile(r"<h1>Customer Success Stories</h1>")
CONTACT_BTN_RE = re.compile(
    r'\s*<a href="(?:\.\./)?contact\.html" class="btn btn-primary">Contact Us Today</a>',
)


def main() -> None:
    updated = 0
    for path in sorted(ROOT.rglob("*.html")):
        if SKIP_PARTS.intersection(path.parts):
            continue
        text = path.read_text()
        if "case-card" not in text and path.name != "case-studies.html":
            continue

        rel = rel_prefix(path, ROOT)
        heading = None if path.name == "case-studies.html" else "Customer Success Stories"
        section = case_studies_section(rel, heading=heading)

        new_text = text
        for pattern in SECTION_PATTERNS:
            if pattern.search(new_text):
                new_text = pattern.sub(section, new_text, count=1)
                break

        if path.name == "case-studies.html":
            new_text = H1_RE.sub("<h1>Customer Success Stories</h1>", new_text)
            new_text = H1_RE_ALT.sub("<h1>Customer Success Stories</h1>", new_text)
            new_text = CONTACT_BTN_RE.sub("", new_text)

        if new_text != text:
            path.write_text(new_text)
            updated += 1
            print(path.relative_to(ROOT))

    print(f"Updated {updated} file(s).")


if __name__ == "__main__":
    main()
