#!/usr/bin/env python3
"""embed-check: every `?raw` import in the docs must point at a real file.

The site renders tested source files into MDX via Vite `?raw` imports
(so "shown == tested"). If a page imports a file that has been moved or
renamed, the build would embed nothing silently. This check fails CI on
any `?raw` import whose target file does not exist.

Resolves the project import aliases:
  #examples/...  -> examples/...
  #snippets/...  -> snippets/...
and ordinary relative `../...?raw` paths.

Usage: python3 scripts/embed_check.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "src" / "content" / "docs"

# import <name> from '<spec>?raw';
IMPORT_RE = re.compile(r"""from\s+['"]([^'"]+?)\?raw['"]""")
# Fenced code blocks contain *documentation* of import syntax, not real
# imports — strip them before scanning so examples in prose don't trip the check.
FENCE_RE = re.compile(r"^```.*?^```", re.DOTALL | re.MULTILINE)

ALIASES = {"#examples": ROOT / "examples", "#snippets": ROOT / "snippets"}


def resolve(spec: str, source: Path) -> Path:
    for alias, base in ALIASES.items():
        if spec == alias or spec.startswith(alias + "/"):
            return base / spec[len(alias) :].lstrip("/")
    # relative to the importing file
    return (source.parent / spec).resolve()


def main() -> int:
    if not DOCS.is_dir():
        print(f"embed-check: no docs dir at {DOCS}", file=sys.stderr)
        return 0
    problems: list[str] = []
    checked = 0
    for page in sorted(DOCS.rglob("*.mdx")):
        text = FENCE_RE.sub("", page.read_text(encoding="utf-8"))
        for spec in IMPORT_RE.findall(text):
            checked += 1
            target = resolve(spec, page)
            if not target.is_file():
                rel = page.relative_to(ROOT)
                problems.append(f"  {rel}: ?raw import '{spec}' -> missing {target}")
    if problems:
        print("embed-check FAILED — dangling ?raw imports:", file=sys.stderr)
        print("\n".join(problems), file=sys.stderr)
        return 1
    print(f"embed-check OK — {checked} ?raw import(s) all resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
