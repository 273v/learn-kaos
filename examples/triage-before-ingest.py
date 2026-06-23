#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-nlp-core>=0.1.6,<0.2", "kaos-pdf>=0.1.0,<0.2", "fpdf2"]
# ///
"""Triage a file before ingesting it — what is it, and does it need OCR?

Before an ingestion pipeline parses a file, it should know two things: the file's
*format* (so it picks the right parser) and, for PDFs, whether there's a *text
layer* (so it knows whether to run OCR). `kaos-nlp-core` sniffs the format from
the bytes; `kaos-pdf` classifies a PDF as text vs. scanned. Both are
deterministic and offline.

This example generates a small PDF, then triages it. (A scanned PDF would
classify differently and route to OCR.)

Run it:

    uv run examples/triage-before-ingest.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import kaos_pdf
from fpdf import FPDF
from kaos_nlp_core import content_type


def make_text_pdf() -> Path:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 8, "MASTER SERVICES AGREEMENT. This Agreement is governed by the "
                         "laws of Delaware. The initial term is three years.")
    path = Path(tempfile.mkdtemp()) / "contract.pdf"
    pdf.output(str(path))
    return path


def main() -> tuple[str, str]:
    path = make_text_pdf()
    data = path.read_bytes()

    # 1. What format is it? (sniffed from the bytes, not the extension)
    fmt = content_type.detect(data)
    print(f"  format:   {fmt.mime_type}  (group={fmt.group})")

    # 2. For a PDF, is there a text layer or does it need OCR?
    kind = kaos_pdf.classify_document(path)
    needs_ocr = kind != "text"
    print(f"  pdf kind: {kind}  ->  {'route to OCR' if needs_ocr else 'extract text directly'}")

    return fmt.group, kind


if __name__ == "__main__":
    group, kind = main()
    assert group == "pdf"
    # The generated PDF has a real text layer, so no OCR is needed.
    assert kind == "text"
