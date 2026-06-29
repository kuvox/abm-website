#!/usr/bin/env python3
"""One-off site patch: Learn nav menu + unified client reviews. Safe to re-run."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REVIEWS = (ROOT / "snippets" / "client-reviews-section.html").read_text()
# Strip snippet comment header for injection
REVIEWS = re.sub(r"<!--.*?-->\s*", "", REVIEWS, count=1, flags=re.DOTALL).strip()

MENU_RE = re.compile(
    r"<li class=\"has-menu has-megamenu has-megamenu--resources\">.*?</li>",
    re.DOTALL,
)

TESTIMONIALS_RE = re.compile(
    r"<!-- =+ TESTIMONIALS =+ -->.*?</section>\s*",
    re.DOTALL,
)

CLIENT_QUOTE_RE = re.compile(
    r"\s*<div class=\"client-quote\">.*?</div>",
    re.DOTALL,
)


def rel_prefix(path: Path) -> str:
    parts = path.relative_to(ROOT).parts
    return "../" if parts[0] in {"services", "case-studies", "resources", "guides"} else ""


def learn_menu(path: Path) -> str:
    rel = rel_prefix(path)
    res = f"{rel}resources.html"
    active = ' style="color:var(--brand);"' if path.name == "resources.html" else ""
    return f"""      <li class="has-menu has-megamenu has-megamenu--learn"><a href="{res}"{active}>Learn</a>
        <div class="megamenu megamenu--learn">
          <div class="megamenu-col">
            <ul>
              <li><a href="{res}"><span class="megamenu-learn-label">Blog</span><span class="megamenu-learn-desc">Optimize Campaigns &amp; Data Feeds</span></a></li>
              <li><a href="https://www.youtube.com/@ppcforeveryone" target="_blank" rel="noopener"><span class="megamenu-learn-label">YouTube Channel</span><span class="megamenu-learn-desc">PPC for Everyone</span></a></li>
              <li><a href="{res}#newsletter"><span class="megamenu-learn-label">Newsletter</span><span class="megamenu-learn-desc">Up-to-Date on Digital Ads</span></a></li>
            </ul>
          </div>
        </div>
      </li>"""


def patch_file(path: Path) -> list[str]:
    changes: list[str] = []
    text = path.read_text()
    original = text

    if MENU_RE.search(text):
        text = MENU_RE.sub(learn_menu(path), text, count=1)
        changes.append("nav")

    if TESTIMONIALS_RE.search(text):
        text = TESTIMONIALS_RE.sub(REVIEWS + "\n\n", text, count=1)
        changes.append("testimonials")

    if CLIENT_QUOTE_RE.search(text) and "case-contact" in text:
        text = CLIENT_QUOTE_RE.sub("", text, count=1)
        if REVIEWS not in text:
            text = text.replace(
                '<section class="case-contact',
                REVIEWS + '\n\n<section class="case-contact',
                1,
            )
            changes.append("case-study-reviews")

    if text != original:
        path.write_text(text)
    return changes


def main() -> None:
    for path in sorted(ROOT.rglob("*.html")):
        if "snippets" in path.parts:
            continue
        changed = patch_file(path)
        if changed:
            print(f"{path.relative_to(ROOT)}: {', '.join(changed)}")


if __name__ == "__main__":
    main()
