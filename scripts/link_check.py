#!/usr/bin/env python3
"""link-check: every internal doc link must resolve to a real page.

Cross-links between tutorials, how-tos, and concepts are easy to typo and
Starlight builds anyway. This check scans the docs sources for root-relative
internal links (`/tutorials/...`, `/concepts/...`) and fails if any points at a
page that doesn't exist. Offline, deterministic, fast.

External links (http/https) and in-page anchors are out of scope here.

Usage: python3 scripts/link_check.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "src" / "content" / "docs"
BASE = "/learn-kaos"  # keep in sync with astro.config.mjs `base`

# Markdown [text](/path) and HTML href="/path" / src component links.
LINK_RE = re.compile(r"""\]\((/[^)\s]+)\)|href=["'](/[^"']+)["']""")
FENCE_RE = re.compile(r"^```.*?^```", re.DOTALL | re.MULTILINE)

# Routes that exist but are not docs collection pages.
KNOWN_ROUTES = {"/", "/gallery", "/llms.txt"}


def page_exists(slug: str) -> bool:
    slug = slug.strip("/")
    if not slug:
        return True  # home
    for ext in (".md", ".mdx"):
        if (DOCS / f"{slug}{ext}").is_file():
            return True
    return False


def normalize(link: str) -> str:
    # drop fragment/query, trailing slash, and the base prefix if present
    link = link.split("#", 1)[0].split("?", 1)[0]
    if link.startswith(BASE + "/") or link == BASE:
        link = link[len(BASE):] or "/"
    if len(link) > 1:
        link = link.rstrip("/")
    return link


def main() -> int:
    problems: list[str] = []
    checked = 0
    for page in sorted(DOCS.rglob("*.md")) + sorted(DOCS.rglob("*.mdx")):
        text = FENCE_RE.sub("", page.read_text(encoding="utf-8"))
        for m in LINK_RE.finditer(text):
            raw = m.group(1) or m.group(2)
            link = normalize(raw)
            if not link.startswith("/"):
                continue
            checked += 1
            if link in KNOWN_ROUTES:
                continue
            if not page_exists(link):
                problems.append(f"  {page.relative_to(ROOT)}: dead link -> {raw}")
    if problems:
        print("link-check FAILED — internal links with no target page:", file=sys.stderr)
        print("\n".join(sorted(set(problems))), file=sys.stderr)
        return 1
    print(f"link-check OK — {checked} internal link(s) all resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
