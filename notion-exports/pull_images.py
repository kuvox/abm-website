"""Temporary helper: download Notion-signed image URLs listed in a manifest.

Manifest format: one entry per line, `<output-path><TAB><url>`.
Usage: python3 pull_images.py <manifest.tsv>
"""
import pathlib
import sys
import urllib.request

manifest = pathlib.Path(sys.argv[1])
failures = 0
for line in manifest.read_text().splitlines():
    line = line.strip()
    if not line:
        continue
    out, url = line.split("\t", 1)
    dest = pathlib.Path(out)
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        with urllib.request.urlopen(url) as resp:
            dest.write_bytes(resp.read())
        print(f"ok  {dest} ({dest.stat().st_size} bytes)")
    except Exception as exc:  # noqa: BLE001
        failures += 1
        print(f"FAIL {dest}: {exc}")
sys.exit(1 if failures else 0)
