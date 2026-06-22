#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-office>=0.1.4,<0.2", "kaos-content>=0.1.6,<0.2"]
# ///
"""Write a real DOCX, then extract it back to the document AST.

`kaos-office` both *writes* and *reads* Office formats. This example builds a
`ContentDocument`, writes it to a real `.docx`, then parses that file back — and
shows the extracted AST matches what we put in. It demonstrates the "one
document model" idea end to end: the same AST a PDF or web page produces is what
you get from a Word document.

Self-contained and offline — it generates its own .docx in a temp dir, so there's
no binary fixture and no network.

Run it:

    uv run examples/office-roundtrip.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import kaos_content as kc
import kaos_office as ko


def build_doc() -> kc.ContentDocument:
    b = kc.DocumentBuilder()
    b.heading(1, "Statement of Work")
    b.paragraph("The vendor shall deliver the software by the milestone dates.")
    b.heading(2, "Payment")
    b.paragraph("Net 30 from invoice.")
    return b.build()


def main() -> str:
    original = build_doc()

    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "sow.docx"

        # Write a genuine .docx file...
        ko.write_docx(original, path)
        print(f"wrote {path.name} ({path.stat().st_size} bytes)")

        # ...then extract it back to the AST, as if it arrived from a client.
        extracted = ko.parse_docx(path)

    markdown = kc.serialize_markdown(extracted)
    print("--- extracted back to Markdown ---")
    print(markdown)
    return markdown


if __name__ == "__main__":
    markdown = main()
    # The headings and text survived the write -> .docx -> extract round trip.
    assert "# Statement of Work" in markdown
    assert "Payment" in markdown
    assert "Net 30 from invoice." in markdown
