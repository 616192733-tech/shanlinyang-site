#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts)
ERRORS: list[str] = []
WARNINGS: list[str] = []
CANONICALS: dict[str, Path] = {}
TITLES: list[tuple[str, Path]] = []


def one(pattern: str, text: str, flags: int = re.I | re.S) -> str | None:
    match = re.search(pattern, text, flags)
    return match.group(1).strip() if match else None


for path in HTML_FILES:
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8", errors="replace")
    title = one(r"<title[^>]*>(.*?)</title>", text)
    description = one(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', text)
    canonical = one(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\'](.*?)["\']', text)
    h1_count = len(re.findall(r"<h1\b", text, re.I))
    jsonld_count = len(re.findall(r'application/ld\+json', text, re.I))

    if not title:
        ERRORS.append(f"{rel}: missing <title>")
    else:
        TITLES.append((re.sub(r"\s+", " ", title), rel))
        if len(title) > 65:
            WARNINGS.append(f"{rel}: long title ({len(title)} chars)")
    if not description:
        ERRORS.append(f"{rel}: missing meta description")
    elif len(description) > 170:
        WARNINGS.append(f"{rel}: long description ({len(description)} chars)")
    if not canonical:
        ERRORS.append(f"{rel}: missing canonical")
    else:
        if not canonical.startswith("https://www.shanlinyang.com/"):
            ERRORS.append(f"{rel}: canonical is outside preferred www host: {canonical}")
        if canonical in CANONICALS:
            WARNINGS.append(f"{rel}: canonical duplicates {CANONICALS[canonical]}: {canonical}")
        CANONICALS[canonical] = rel
    if h1_count != 1:
        ERRORS.append(f"{rel}: expected 1 H1, found {h1_count}")
    if jsonld_count > 4:
        WARNINGS.append(f"{rel}: review {jsonld_count} JSON-LD blocks for duplication")

for title, count in Counter(t for t, _ in TITLES).items():
    if count > 1:
        pages = ", ".join(str(p) for t, p in TITLES if t == title)
        WARNINGS.append(f"duplicate title on {count} pages: {title} [{pages}]")

sitemap = ROOT / "sitemap.xml"
if not sitemap.exists():
    ERRORS.append("missing sitemap.xml")
else:
    try:
        tree = ElementTree.parse(sitemap)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = tree.findall("sm:url", ns)
        lastmods = [u.findtext("sm:lastmod", default="", namespaces=ns) for u in urls]
        repeated = Counter(lastmods).most_common(1)
        if repeated and repeated[0][0] and repeated[0][1] >= max(20, len(urls) // 2):
            WARNINGS.append(
                f"sitemap: {repeated[0][1]}/{len(urls)} URLs share lastmod {repeated[0][0]}; use real modification dates"
            )
    except ElementTree.ParseError as exc:
        ERRORS.append(f"sitemap.xml is invalid XML: {exc}")

print(f"Audited {len(HTML_FILES)} HTML files")
for message in WARNINGS:
    print(f"WARNING: {message}")
for message in ERRORS:
    print(f"ERROR: {message}")
print(f"Summary: {len(ERRORS)} errors, {len(WARNINGS)} warnings")
sys.exit(1 if ERRORS else 0)
