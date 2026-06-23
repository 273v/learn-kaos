#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-citations>=0.1.0,<0.2"]
# ///
"""Parse legal citations from text — cases, regulations, statutes.

`kaos-citations` recognizes Bluebook-style legal citations and returns them as
*typed* records: a case citation gives you the case name, reporter, volume, page,
year, and court; a CFR citation gives you title and section. This is pure parsing
— deterministic, offline, no model or API key. It's the backbone of every
legal-data workflow (building case databases, linking authorities, checking
references).

Run it:

    uv run examples/parse-citations.py
"""

from __future__ import annotations

import kaos_citations as kc

TEXT = (
    "The Court reaffirmed Miranda v. Arizona, 384 U.S. 436 (1966), and distinguished "
    "Brown v. Board of Education, 347 U.S. 483 (1954). The complaint also alleges "
    "violations of 17 CFR 240.10b-5 and 15 U.S.C. § 78j(b)."
)


def main() -> list:
    citations = kc.extract_citations(TEXT)

    print(f"found {len(citations)} citation(s):\n")
    for c in citations:
        if c.kind == "case":
            print(f"  [case]    {c.case_name} — {c.volume} {c.reporter} {c.page} ({c.year}) [{c.court}]")
        else:
            print(f"  [{c.kind:<7}] {c.normalized}")
    return citations


if __name__ == "__main__":
    citations = main()
    kinds = [c.kind for c in citations]
    # Two cases, a regulation, and a statute — all parsed, no model needed.
    assert kinds.count("case") == 2
    cases = [c for c in citations if c.kind == "case"]
    assert any("Miranda v. Arizona" in c.case_name and c.year == 1966 for c in cases)
    assert any(c.kind == "cfr" for c in citations)
