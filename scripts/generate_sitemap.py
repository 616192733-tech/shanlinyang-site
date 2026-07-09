#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.shanlinyang.com"


def git_date(path: Path) -> str:
    result = subprocess.run(
        ["git", "log", "-1", "--format=%cs", "--", str(path.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.stdout.strip() or "2026-01-01"


def canonical(text: str) -> str | None:
    match = re.search(
        r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\'](.*?)["\']',
        text,
        re.I | re.S,
    )
    return match.group(1).strip() if match else None


config = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
redirected = {item["source"] for item in config.get("redirects", [])}
entries: dict[str, tuple[str, str, str]] = {}

for path in sorted(ROOT.rglob("*.html")):
    if ".git" in path.parts:
        continue
    rel = path.relative_to(ROOT).as_posix()
    public_path = "/" if rel == "index.html" else f"/{rel}"
    if public_path in redirected:
        continue
    text = path.read_text(encoding="utf-8", errors="replace")
    url = canonical(text)
    if not url or not url.startswith(f"{SITE}/"):
        continue
    if url in entries:
        continue
    if url == f"{SITE}/":
        priority, frequency = "1.0", "weekly"
    elif "/products/" in url or url.endswith("contact.html"):
        priority, frequency = "0.9", "weekly"
    elif "/blog/" in url:
        priority, frequency = "0.7", "monthly"
    else:
        priority, frequency = "0.8", "monthly"
    entries[url] = (git_date(path), frequency, priority)

lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for url, (lastmod, frequency, priority) in sorted(entries.items()):
    lines.extend([
        "  <url>",
        f"    <loc>{html.escape(url)}</loc>",
        f"    <lastmod>{lastmod}</lastmod>",
        f"    <changefreq>{frequency}</changefreq>",
        f"    <priority>{priority}</priority>",
        "  </url>",
    ])
lines.append("</urlset>")
(ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Generated sitemap.xml with {len(entries)} canonical URLs")
