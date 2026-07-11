#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOCK = re.compile(
    r'(<script[^>]+type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',
    re.I | re.S,
)


def replace_jsonld(path: Path, transform) -> bool:
    text = path.read_text(encoding="utf-8")
    changed = False

    def update(match: re.Match[str]) -> str:
        nonlocal changed
        try:
            data = json.loads(match.group(2))
        except json.JSONDecodeError:
            return match.group(0)
        new_data = transform(data, text)
        if new_data == data:
            return match.group(0)
        changed = True
        return match.group(1) + "\n" + json.dumps(new_data, ensure_ascii=False, indent=2) + "\n" + match.group(3)

    updated = BLOCK.sub(update, text)
    if changed:
        path.write_text(updated, encoding="utf-8")
    return changed


def normalize_product(data, html: str):
    if not isinstance(data, dict) or data.get("@type") != "Product":
        return data
    data = json.loads(json.dumps(data))
    og = re.search(
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\'](.*?)["\']',
        html,
        re.I | re.S,
    )
    if og and not data.get("image"):
        data["image"] = og.group(1).strip()
    offers = data.get("offers")
    if isinstance(offers, dict) and "offerCount" in offers:
        digits = re.sub(r"\D", "", str(offers["offerCount"]))
        if digits:
            offers["offerCount"] = int(digits)
    return data


def normalize_home(data, _html: str):
    if not isinstance(data, dict):
        return data
    data = json.loads(json.dumps(data))
    schema_type = data.get("@type")
    types = schema_type if isinstance(schema_type, list) else [schema_type]
    if "Organization" in types:
        data.update(
            {
                "@id": "https://www.shanlinyang.com/#org",
                "legalName": "Xiamen Shan Lin Yang Trading Co., Ltd.",
                "email": "616192733@qq.com",
                "telephone": "+86-177-5065-9112",
            }
        )
        if isinstance(data.get("contactPoint"), dict):
            data["contactPoint"].setdefault("email", "616192733@qq.com")
    if schema_type == "VideoObject" and isinstance(data.get("publisher"), dict):
        data["publisher"] = {"@id": "https://www.shanlinyang.com/#org"}
    return data


def main() -> None:
    changed = []
    for path in sorted((ROOT / "products").glob("*.html")):
        if replace_jsonld(path, normalize_product):
            changed.append(str(path.relative_to(ROOT)))
    if replace_jsonld(ROOT / "index.html", normalize_home):
        changed.append("index.html")
    print("Normalized: " + ", ".join(changed) if changed else "Schema already normalized")


if __name__ == "__main__":
    main()
