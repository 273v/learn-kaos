#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-pdf>=0.1.4,<0.2", "kaos-content>=0.1.6,<0.2", "fpdf2>=2.7"]
# ///
"""Extract a PDF to the document AST.

`kaos-pdf` turns a PDF into a `ContentDocument` — the same AST every other
extractor produces — with page/position provenance. So a PDF, a Word doc, and a
web page all become one shape the rest of the stack works on.

To stay self-contained and offline, this example *generates* a small PDF with a
pure-Python writer (fpdf2), then extracts it with kaos-pdf — no committed binary,
no network. With a real document, just point `parse_pdf` at its path.

Run it:

    uv run examples/pdf-extract.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import kaos_content as kc
import kaos_pdf as kp
from fpdf import FPDF


def make_pdf(path: Path) -> None:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", style="B", size=16)
    pdf.cell(0, 10, "Engagement Memo")
    pdf.ln(14)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(
        0,
        8,
        "The retainer is twenty thousand dollars. Fees are billed monthly "
        "against the retainer. Unused amounts are refundable on termination.",
    )
    pdf.output(str(path))


def main() -> str:
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "memo.pdf"
        make_pdf(path)
        print(f"generated {path.name} ({path.stat().st_size} bytes)")

        # Extract it to the content AST.
        doc = kp.parse_pdf(path)

    text = kc.serialize_text(doc)
    print("--- extracted text ---")
    print(text.strip())
    return text


if __name__ == "__main__":
    text = main()
    assert "retainer is twenty thousand dollars" in text
    assert "billed monthly" in text
