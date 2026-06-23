#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "kaos-pdf>=0.1.0,<0.2",
#   "kaos-office>=0.1.4,<0.2",
#   "kaos-content>=0.1.3,<0.2",
#   "kaos-nlp-transformers>=0.1.5,<0.2",
#   "fpdf2",
# ]
# ///
"""Turn a signed contract PDF into a reusable template — no LLM, no API key.

A genuinely practical legal task: take a *real* agreement, find its variable
fields (the parties, the dollar amounts, the dates), and swap them for template
placeholders so you can reuse the document. This composes four KAOS packages:

  read the PDF + clean the text     (kaos-pdf)
    → find fields with a local NER model   (kaos-nlp-transformers / GLiNER)
      → rewrite as a {{template}} + redline the changes   (kaos-office)

Then fill the template with new values to generate a fresh contract. Everything
runs locally — the only "model" is a small on-device NER model (downloaded once,
then cached; no provider key).

Run it:

    uv run examples/contract-to-template.py
"""

from __future__ import annotations

import re
import tempfile
from pathlib import Path

import kaos_content as kc
import kaos_nlp_transformers as knt
import kaos_office as ko
import kaos_pdf
from fpdf import FPDF
from kaos_content.revision import Revisions

# The clauses of the "signed" agreement we'll templatize.
CLAUSES = [
    "This Mutual Nondisclosure Agreement is entered into as of March 1, 2026, "
    "by and between Acme Corporation and Globex Industries.",
    "The receiving party shall pay liquidated damages of $50,000 for any breach "
    "of its confidentiality obligations under this Agreement.",
]

# Which NER labels become which kind of template field.
FIELD_OF = {"organization": "party", "money": "amount", "date": "date"}

_extractor = knt.GLiNERExtractor.load()


def make_pdf(path: Path) -> Path:
    """Stand in for a real signed PDF on disk."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    for clause in CLAUSES:
        pdf.multi_cell(0, 8, clause)
        pdf.ln(3)
    pdf.output(str(path))
    return path


def read_pdf_text(path: Path) -> str:
    """Extract the page text and normalize PDF whitespace — line wrapping splits
    phrases like 'Acme\\nCorporation', so collapse runs of whitespace to spaces."""
    raw = kaos_pdf.extract_page_text(path, 0)
    return re.sub(r"\s+", " ", raw).strip()


def templatize(text: str) -> tuple[str, dict[str, str]]:
    """Replace every party/amount/date with a {{field}} placeholder; return the
    rewritten text and the field → original-value map. Runs NER on the whole
    document (context matters — in isolation a model may tag a generic phrase
    like 'the receiving party' as an org)."""
    entities = sorted(
        _extractor.extract([text], labels=list(FIELD_OF), threshold=0.6)[0],
        key=lambda e: e.start,
    )
    counters: dict[str, int] = {}
    fields: dict[str, str] = {}
    spans = []
    for e in entities:
        base = FIELD_OF[e.label]
        counters[base] = counters.get(base, 0) + 1
        token = f"{{{{{base}_{counters[base]}}}}}"
        fields[token] = e.text
        spans.append((e.start, e.end, token))
    for start, end, token in sorted(spans, reverse=True):  # right-to-left
        text = text[:start] + token + text[end:]
    return text, fields


def sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=\.)\s+", text) if s.strip()]


def write_docx(paragraphs: list[str], path: Path) -> Path:
    b = kc.DocumentBuilder()
    b.heading(1, "Mutual NDA")
    for p in paragraphs:
        b.paragraph(p)
    ko.write_docx(b.build(), path)
    return path


def main():
    work = Path(tempfile.mkdtemp())

    # 1. Read the "signed" PDF and clean the extracted text.
    pdf = make_pdf(work / "agreement.pdf")
    text = read_pdf_text(pdf)
    print("Signed contract (agreement.pdf), text extracted & cleaned:")
    print(f"  {sentences(text)[0]}\n")

    # 2. Find fields + build the template.
    template_text, fields = templatize(text)
    print(f"Found {len(fields)} field(s) with on-device NER (no LLM, no key):")
    for token, value in fields.items():
        print(f"  {token:<12} <- {value!r}")
    print("\nReusable template (template.docx):")
    print(f"  {sentences(template_text)[0]}\n")

    # 3. Author the original + template as DOCX and redline them — every swap is
    #    a tracked change a human can review, so the parameterization is auditable.
    original_docx = write_docx(sentences(text), work / "agreement.docx")
    template_docx = write_docx(sentences(template_text), work / "template.docx")
    changes = list(Revisions.from_document(ko.compare_docx(str(original_docx), str(template_docx))))
    print(f"Redline (contract → template): {len(fields)} fields parameterized, "
          f"{len(changes)} tracked change(s).\n")

    # 4. Fill the template for a new deal — the reuse payoff.
    new_values = {
        "{{date_1}}": "June 30, 2026",
        "{{party_1}}": "Initech LLC",
        "{{party_2}}": "Stark Industries",
        "{{amount_1}}": "$250,000",
    }
    filled = sentences(template_text)[0]
    for token, value in new_values.items():
        filled = filled.replace(token, value)
    print("Fill it for a new deal:")
    print(f"  {filled}")
    return fields, changes, filled


if __name__ == "__main__":
    fields, changes, filled = main()
    # NER found the parties, the date, and the amount...
    assert fields.get("{{party_1}}") == "Acme Corporation"
    assert fields.get("{{party_2}}") == "Globex Industries"
    assert any("2026" in v for v in fields.values())
    assert any(v.startswith("$") for v in fields.values())
    # ...the redline captured the swaps...
    assert len(changes) >= len(fields)
    # ...and the filled contract carries the new values, not the originals.
    assert "Initech LLC" in filled and "Acme Corporation" not in filled
