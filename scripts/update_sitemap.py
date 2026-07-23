#!/usr/bin/env python3
"""Regenerate sitemap.xml with real per-file lastmod dates (from file mtimes).

Run from the repo root after any content change:
    python3 scripts/update_sitemap.py
"""
from datetime import datetime, timezone
from pathlib import Path

SITE = "https://abeckermarketing.com"
ROOT = Path(__file__).resolve().parent.parent

# (relative file, url path, priority, changefreq)
PAGES = [
    ("index.html", "/", "1.0", "monthly"),
    ("about.html", "/about.html", "0.8", "monthly"),
    ("case-studies.html", "/case-studies.html", "0.8", "monthly"),
    ("contact.html", "/contact.html", "0.8", "monthly"),
    ("services.html", "/services.html", "0.9", "monthly"),
    ("supported-ad-platforms.html", "/supported-ad-platforms.html", "0.7", "monthly"),
    ("resources.html", "/resources.html", "0.8", "weekly"),
]
PAGES += [
    (f"guides/{p.name}", f"/guides/{p.name}", "0.7", "monthly")
    for p in sorted((ROOT / "guides").glob("*.html"))
]
PAGES += [
    (f"case-studies/{p.name}", f"/case-studies/{p.name}", "0.7", "monthly")
    for p in sorted((ROOT / "case-studies").glob("*.html"))
]
PAGES += [
    (f"resources/{p.name}", f"/resources/{p.name}", "0.6", "monthly")
    for p in sorted((ROOT / "resources").glob("*.html"))
]
PAGES += [("privacy-policy.html", "/privacy-policy.html", "0.3", "yearly")]


def lastmod(rel: str) -> str:
    ts = (ROOT / rel).stat().st_mtime
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")


def main() -> None:
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for rel, url, priority, freq in PAGES:
        out.append("  <url>")
        out.append(f"    <loc>{SITE}{url}</loc>")
        out.append(f"    <lastmod>{lastmod(rel)}</lastmod>")
        out.append(f"    <changefreq>{freq}</changefreq>")
        out.append(f"    <priority>{priority}</priority>")
        out.append("  </url>")
    out.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(out) + "\n")
    print(f"wrote sitemap.xml ({len(PAGES)} urls)")


if __name__ == "__main__":
    main()
