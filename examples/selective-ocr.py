#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-pdf>=0.1.0,<0.2", "fpdf2", "pillow"]
# ///
"""Find which PDF pages need OCR / VLM — selective, page by page.

Real-world PDFs are often *hybrid*: a born-digital body with a scanned exhibit or
signature page stapled on. Running OCR on the whole file is slow and lossy;
skipping it misses the scanned pages. `kaos-pdf` classifies each page, so you OCR
(or send to a vision model) *only* the pages that need it and extract the text
layer directly everywhere else.

This builds a 2-page hybrid PDF (one text page, one image-only page) and routes
each page. Deterministic and offline.

Run it:

    uv run examples/selective-ocr.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import kaos_pdf
from fpdf import FPDF
from PIL import Image, ImageDraw


def make_hybrid_pdf() -> Path:
    # A scanned-looking image page (no text layer).
    img = Image.new("RGB", (600, 800), "white")
    ImageDraw.Draw(img).text((40, 60), "SCANNED EXHIBIT A - signature page", fill="black")
    img_path = Path(tempfile.mkdtemp()) / "scan.png"
    img.save(img_path)

    pdf = FPDF()
    pdf.add_page()  # page 1: born-digital text
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 8, "MASTER SERVICES AGREEMENT. Governed by Delaware law. "
                         "The initial term is three years.")
    pdf.add_page()  # page 2: a full-page image, no text layer
    pdf.image(str(img_path), x=0, y=0, w=210)

    out = Path(tempfile.mkdtemp()) / "hybrid.pdf"
    pdf.output(str(out))
    return out


def main() -> tuple[str, list[str]]:
    path = make_hybrid_pdf()

    doc_kind = kaos_pdf.classify_document(path)
    print(f"document: {doc_kind}\n")  # "mixed" for a hybrid file

    page_kinds = []
    for page in range(2):
        kind = kaos_pdf.classify_page(path, page)
        chars = len(kaos_pdf.extract_page_text(path, page).strip())
        page_kinds.append(kind)
        if kind == "text":
            print(f"  page {page}: {kind:<6} ({chars} chars) -> extract text directly")
        else:
            print(f"  page {page}: {kind:<6} ({chars} chars) -> send to OCR / VLM")

    return doc_kind, page_kinds


if __name__ == "__main__":
    doc_kind, page_kinds = main()
    # A hybrid file is "mixed"; only the image page needs OCR/VLM.
    assert doc_kind == "mixed"
    assert page_kinds[0] == "text"
    assert page_kinds[1] != "text"  # the scanned page
