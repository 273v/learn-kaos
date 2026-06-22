#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-citations>=0.1.2,<0.2"]
# ///
"""Your first KAOS example: pull typed legal citations out of plain text.

Fully offline and deterministic — no API key, no network, no model.
`kaos-citations` is pure-Python with a Rust-backed matcher, so the same
input always yields the same typed output.

Run it:

    uv run examples/citations-extract.py
"""

from __future__ import annotations

from kaos_citations import extract_citations

TEXT = (
    "The Supreme Court's decision in Brown v. Board of Education, "
    "347 U.S. 483 (1954), remains a landmark. Securities claims often "
    "arise under 15 U.S.C. 78j(b)."
)


def main() -> list:
    citations = extract_citations(TEXT)
    print(f"Found {len(citations)} citation(s):\n")
    for c in citations:
        # Every citation carries a kind, the raw matched text, a
        # normalized form, and an absolute (start, end) span into TEXT.
        print(f"  kind={c.kind:<8} normalized={c.normalized!r}  span={c.span}")
    return citations


if __name__ == "__main__":
    result = main()
    # A tiny self-check so this file doubles as its own test (the docs
    # site and CI both run it; see snippets-test / examples-smoke).
    assert any(c.kind == "case" for c in result), "expected a case citation"
    assert any(c.normalized == "347 U.S. 483 (1954)" for c in result)
