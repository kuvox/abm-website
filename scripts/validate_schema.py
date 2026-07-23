#!/usr/bin/env python3
"""Schema + SEO head validator. Run from the repo root; exits 1 on failure.

Checks every indexable page for:
- JSON-LD parses; exactly one block per page
- every internally-referenced @id is defined in that page's graph
  (page-scoped parsers like Google's don't resolve cross-page @ids)
- no multi-fragment @ids (a URI can carry only one '#')
- Article author/publisher resolvable; VideoObject has thumbnailUrl
- head: canonical, og:site_name/title/url/image, twitter:card present,
  no duplicate canonical/og:title

    python3 scripts/validate_schema.py
"""
import glob
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://abeckermarketing.com"

PAGES = (
    ["index.html", "about.html", "services.html", "contact.html",
     "case-studies.html", "resources.html", "supported-ad-platforms.html",
     "privacy-policy.html"]
    + sorted(glob.glob("case-studies/*.html", root_dir=ROOT))
    + sorted(glob.glob("guides/*.html", root_dir=ROOT))
    + sorted(glob.glob("resources/*.html", root_dir=ROOT))
)

HEAD_CHECKS = [
    ("canonical", r'<link rel="canonical"'),
    ("og:site_name", r'property="og:site_name"'),
    ("og:title", r'property="og:title"'),
    ("og:url", r'property="og:url"'),
    ("og:image", r'property="og:image"'),
    ("twitter:card", r'name="twitter:card"'),
]


def main() -> int:
    errors: list[str] = []
    for rel in PAGES:
        html = (ROOT / rel).read_text()
        for tag, pat in HEAD_CHECKS:
            n = len(re.findall(pat, html))
            if n == 0:
                errors.append(f"{rel}: missing {tag}")
            if tag in ("canonical", "og:title") and n > 1:
                errors.append(f"{rel}: duplicate {tag} x{n}")
        blocks = re.findall(
            r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        if rel != "privacy-policy.html" and not blocks:
            errors.append(f"{rel}: no JSON-LD")
        if len(blocks) > 1:
            errors.append(f"{rel}: multiple JSON-LD blocks x{len(blocks)}")
        ids: set[str] = set()
        refs: set[str] = set()
        parsed = []
        for b in blocks:
            try:
                d = json.loads(b)
            except Exception as e:  # noqa: BLE001
                errors.append(f"{rel}: JSON parse error: {e}")
                continue
            parsed.append(d)
            for n in d.get("@graph", [d]):
                if n.get("@id"):
                    ids.add(n["@id"])
                for m in re.finditer(r'"@id": "([^"]+)"', json.dumps(n)):
                    refs.add(m.group(1))
        dangling = sorted(r for r in refs if r not in ids and r.startswith(SITE))
        if dangling:
            errors.append(f"{rel}: dangling internal @ids: {dangling}")
        bad = [i for i in ids | refs if i.count("#") > 1]
        if bad:
            errors.append(f"{rel}: invalid multi-fragment @ids: {bad}")
        for d in parsed:
            for n in d.get("@graph", [d]):
                t = n.get("@type")
                if t == "Article" and "description" in n:
                    for k in ("author", "publisher"):
                        if n.get(k, {}).get("@id") not in ids:
                            errors.append(f"{rel}: Article.{k} unresolved")
                if t == "VideoObject" and "thumbnailUrl" not in n:
                    errors.append(f"{rel}: VideoObject missing thumbnailUrl")
    print(f"checked {len(PAGES)} pages")
    if errors:
        print("FAILED:")
        for e in errors:
            print(" -", e)
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
