#!/usr/bin/env python3
"""Remove orphaned Resources megamenu markup left after partial nav patch."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ORPHAN_RE = re.compile(
    r"\s*<li><a href=\"(?:\.\./)?resources\.html#research\">Research Articles</a></li>.*?"
    r"</div>\s*</div>\s*</li>\s*(?=<li class=\"has-menu has-megamenu has-megamenu--about\">)",
    re.DOTALL,
)

LEARN_INDENT_RE = re.compile(
    r"      <li><a href=\"case-studies\.html\">Case Studies</a></li>\n\s*<li class=\"has-menu has-megamenu has-megamenu--learn\">",
)

LEARN_FIXED = """      <li><a href="case-studies.html">Case Studies</a></li>
      <li class="has-menu has-megamenu has-megamenu--learn">"""


def main() -> None:
    for path in ROOT.rglob("*.html"):
        if "snippets" in path.parts or "sessions" in path.parts:
            continue
        text = path.read_text()
        new = ORPHAN_RE.sub("\n", text)
        new = LEARN_INDENT_RE.sub(LEARN_FIXED, new)
        if new != text:
            path.write_text(new)
            print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
