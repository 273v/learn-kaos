#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-content>=0.1.6,<0.2"]
# ///
"""Build a structured document, serialize it, and address a block.

`kaos-content` is KAOS's document model: one Block/Inline AST that every
extractor (PDF, DOCX, web, ...) produces, so the rest of the stack works
on a single shape. Here we build one by hand with `DocumentBuilder`,
render it to Markdown, and read its outline — including each heading's
stable **block reference** (`ref`), which is how citations point at a
precise location in a document.

Fully offline and deterministic — no key, no network.

Run it:

    uv run examples/build-a-document.py
"""

from __future__ import annotations

import kaos_content as kc


def build() -> kc.ContentDocument:
    b = kc.DocumentBuilder()
    b.heading(1, "Lease Agreement")
    b.paragraph("This lease is between ", kc.DocumentBuilder.bold("the parties"), ".")
    b.heading(2, "Rent")
    b.paragraph(
        "Tenant shall pay rent ",
        kc.DocumentBuilder.link("monthly", "https://example.com/terms"),
        ".",
    )
    return b.build()


def main() -> tuple[str, list]:
    doc = build()

    # 1. Serialize the AST to Markdown.
    markdown = kc.serialize_markdown(doc)
    print("--- Markdown ---")
    print(markdown)

    # 2. Read the outline. Each entry has a stable `ref` — the block
    #    reference a citation would point at.
    outline = kc.document_outline(doc)
    print("--- Outline (depth | text | block ref) ---")
    for h in outline:
        print(f"  h{h['depth']}  {h['text']!r:<22}  {h['ref']}")

    return markdown, outline


if __name__ == "__main__":
    markdown, outline = main()
    # Deterministic self-checks: structure and the block refs are stable.
    assert "# Lease Agreement" in markdown
    assert "**the parties**" in markdown
    assert "[monthly](https://example.com/terms)" in markdown
    assert [(h["depth"], h["text"], h["ref"]) for h in outline] == [
        (1, "Lease Agreement", "#/body/0"),
        (2, "Rent", "#/body/2"),
    ]
