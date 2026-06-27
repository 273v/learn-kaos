#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-pdf>=0.1.6,<0.2"]
# ///
"""Detect a garbled OCR layer so `ocr="auto"` re-extracts it.

Scanners and old "Paper Capture" passes often leave a PDF with a *present but
garbled* text layer — the page reads ``0RlGlt IAt lJn tbe @nitp! btutts`` where
it should say "In the United States Court of Federal Claims". An empty-layer
check misses this (there IS text), so the garbage flows downstream.

`kaos-pdf` ships a cheap, dependency-free legibility signal (an English
dictionary hit-rate scored on the *worst* line of a page) that flags these
layers. `parse_pdf(..., ocr="auto")` uses exactly this signal to automatically
re-OCR a scanned page whose native text is garbled — not just empty ones.

This example scores a garbled layer against a clean one — fully offline and
deterministic, no OCR engine required.

Run it:

    uv run examples/recover-garbled-ocr.py
"""

from __future__ import annotations

from kaos_pdf import assess_text_quality, is_low_quality_layer, line_legibility

# The garbled string is the real native text layer of a Canon-scanned court
# order; the clean string is what the page actually says.
GARBLED = "0RlGlt IAt lJn tbe @nitp! btutts ourt of trs lsims"
CLEAN = "In the United States Court of Federal Claims"


def main() -> tuple[bool, bool]:
    print(f"garbled line legibility: {line_legibility(GARBLED):.2f}")  # ~0.10
    print(f"clean line legibility:   {line_legibility(CLEAN):.2f}\n")  # 1.00

    # A real page has clean body text plus one garbled title line. The page
    # score is the *worst* substantial line, so localized garbage still trips it.
    page = f"{CLEAN} filed July 17, 2015\n{GARBLED}\nNot for publication"
    quality = assess_text_quality(page)
    print(f"page worst-line score: {quality.score:.2f}")
    print(f"worst line: {quality.worst_line!r}\n")

    garbled_low = is_low_quality_layer(GARBLED)
    clean_low = is_low_quality_layer(CLEAN)
    print(f"garbled layer -> {'needs re-OCR' if garbled_low else 'kept as-is'}")
    print(f"clean layer   -> {'needs re-OCR' if clean_low else 'kept as-is'}")
    print('\nparse_pdf(path, ocr="auto") applies this automatically: it re-OCRs')
    print("scanned pages whose native layer is garbled, and leaves the rest alone.")
    return garbled_low, clean_low


if __name__ == "__main__":
    garbled_low, clean_low = main()
    assert garbled_low is True  # garbled layer is flagged for re-OCR
    assert clean_low is False  # clean text is kept as-is
