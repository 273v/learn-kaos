#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "kaos-office>=0.1.4,<0.2",
#   "kaos-content>=0.1.3,<0.2",
#   "kaos-nlp-transformers>=0.1.5,<0.2",
# ]
# ///
"""Turn a signed contract into a reusable template — no LLM, no API key.

A genuinely practical legal task: take a *real* agreement, find its variable
fields (the parties, the dollar amounts, the dates), and swap them for template
placeholders so you can reuse the document. This composes three KAOS packages:

  parse the DOCX  (kaos-office)
    → find fields with a local NER model  (kaos-nlp-transformers / GLiNER)
      → rewrite as a {{template}} and redline the changes  (kaos-office)

Then fill the template with new values to generate a fresh contract. Everything
runs locally — the only "model" is a small on-device NER model (downloaded once,
then cached; no provider key).

Run it:

    uv run examples/contract-to-template.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import kaos_content as kc
import kaos_nlp_transformers as knt
import kaos_office as ko
from kaos_content.revision import Revisions

# The "real" agreement we'll templatize.
PARAGRAPHS = [
    "This Mutual Nondisclosure Agreement is entered into as of March 1, 2026, "
    "by and between Acme Corporation and Globex Industries.",
    "The receiving party shall pay liquidated damages of $50,000 for any breach "
    "of its confidentiality obligations under this Agreement.",
]

# Which NER labels become which kind of template field.
FIELD_OF = {"organization": "party", "money": "amount", "date": "date"}

_extractor = knt.GLiNERExtractor.load()


def templatize(text: str) -> tuple[str, dict[str, str]]:
    """Replace every party/amount/date in `text` with a {{field}} placeholder,
    returning the rewritten text and the field → original-value map. Runs NER on
    the whole document at once (context matters — in isolation a model may tag a
    generic phrase like "the receiving party" as an org)."""
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
    # Apply right-to-left so earlier offsets stay valid.
    for start, end, token in sorted(spans, reverse=True):
        text = text[:start] + token + text[end:]
    return text, fields


def write_docx(title: str, paragraphs: list[str], path: Path) -> Path:
    b = kc.DocumentBuilder()
    b.heading(1, title)
    for p in paragraphs:
        b.paragraph(p)
    ko.write_docx(b.build(), path)
    return path


def main():
    work = Path(tempfile.mkdtemp())
    agreement = write_docx("Mutual NDA", PARAGRAPHS, work / "agreement.docx")

    print("Real agreement (agreement.docx):")
    print(f"  {PARAGRAPHS[0]}\n")

    # 1. Find fields + build the template. Run NER over the whole document at
    #    once, then split back into paragraphs to author the template DOCX.
    template_full, fields = templatize("\n\n".join(PARAGRAPHS))
    template_paras = template_full.split("\n\n")
    template = write_docx("Mutual NDA", template_paras, work / "template.docx")

    print(f"Found {len(fields)} field(s) with on-device NER (no LLM, no key):")
    for token, value in fields.items():
        print(f"  {token:<12} <- {value!r}")

    print("\nReusable template (template.docx):")
    print(f"  {template_paras[0]}\n")

    # 2. Redline the original → template: every swap is a tracked change you can
    #    review, so the parameterization is fully auditable.
    redline = ko.compare_docx(str(agreement), str(template))
    changes = list(Revisions.from_document(redline))
    print(f"Redline (agreement → template): {len(fields)} fields parameterized, "
          f"{len(changes)} tracked change(s).\n")

    # 3. Fill the template for a new deal — the reuse payoff.
    new_values = {
        "{{date_1}}": "June 30, 2026",
        "{{party_1}}": "Initech LLC",
        "{{party_2}}": "Stark Industries",
        "{{amount_1}}": "$250,000",
    }
    filled = template_paras[0]
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
