#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-content>=0.1.6,<0.2"]
# ///
"""Pull the defined-terms glossary out of a contract.

Defined terms ("Confidential Information" means ...) are the backbone of any
contract — and the first thing a reviewer or a knowledge-management pipeline
wants to index. `kaos-content` tracks definitions in the document model, so
`document_definitions()` returns them as a clean term -> definition glossary.

Fully offline and deterministic — no key, no network.

Run it:

    uv run examples/contract-definitions.py
"""

from __future__ import annotations

import kaos_content as kc


def build_nda() -> kc.ContentDocument:
    b = kc.DocumentBuilder()
    b.heading(1, "Mutual Non-Disclosure Agreement")
    b.add_definition(
        "Confidential Information",
        "any non-public information disclosed by one party to the other",
    )
    b.add_definition("Effective Date", "the date of last signature below")
    b.add_definition("Receiving Party", "the party that receives Confidential Information")
    b.paragraph(
        "The Receiving Party shall protect Confidential Information from the "
        "Effective Date for a period of three years."
    )
    return b.build()


def main() -> dict[str, str]:
    doc = build_nda()
    glossary = kc.document_definitions(doc)
    print(f"Defined terms ({len(glossary)}):\n")
    for term, definition in glossary.items():
        print(f"  • {term}: {definition}")
    return glossary


if __name__ == "__main__":
    glossary = main()
    assert "Confidential Information" in glossary
    assert glossary["Receiving Party"].startswith("the party that receives")
    assert len(glossary) == 3
