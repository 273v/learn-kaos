#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-content>=0.1.6,<0.2", "kaos-nlp-core>=0.1.6,<0.2"]
# ///
"""Locate money, dates, percentages, and durations in a document — no model.

Sometimes you don't need an LLM or even a NER model — you need to *find the
sentences that contain a figure* and review them. `kaos-content`'s entity filters
locate money, dates, durations, percentages, and numbers over a document view
using built-in patterns: deterministic, instant, offline.

Run it:

    uv run examples/find-financial-terms.py
"""

from __future__ import annotations

import kaos_content as kc
from kaos_content.views import DocumentView, entity_filters as ef
from kaos_nlp_core._defaults import get_default_punkt_tokenizer

CONTRACT = [
    "This Master Services Agreement is effective as of March 1, 2026.",
    "The total contract value is $4,500,000 payable in quarterly installments.",
    "Either party may terminate on 90 days written notice.",
    "Late payments accrue interest at 1.5% per month.",
    "The parties agree to act in good faith.",  # no figures
]


def build_view() -> DocumentView:
    b = kc.DocumentBuilder()
    b.heading(1, "Master Services Agreement")
    for para in CONTRACT:
        b.paragraph(para)
    return DocumentView(b.build(), sentence_segmenter=get_default_punkt_tokenizer())


def main() -> dict[str, int]:
    view = build_view()

    finders = {
        "money": ef.sentences_with_money,
        "dates": ef.sentences_with_dates,
        "percents": ef.sentences_with_percents,
        "durations": ef.sentences_with_durations,
    }

    counts = {}
    for label, finder in finders.items():
        hits = list(finder(view))
        counts[label] = len(hits)
        print(f"{label} ({len(hits)}):")
        for hit in hits:
            print(f"  - {hit.sentence.text}")
    return counts


if __name__ == "__main__":
    counts = main()
    # Each figure type is located in its sentence; the prose-only line matches none.
    assert counts["money"] >= 1
    assert counts["dates"] >= 1
    assert counts["percents"] >= 1
    assert counts["durations"] >= 1
