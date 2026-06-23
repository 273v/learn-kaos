#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-nlp-core>=0.1.6,<0.2"]
# ///
"""Chunk a document for retrieval — by sentence or by section.

Before you embed or search a document, you split it into chunks. `kaos-nlp-core`
offers several strategies; the right one preserves meaning. `SentenceChunker`
packs whole sentences up to a token budget (never splitting mid-sentence);
`SectionChunker` respects the document's heading structure. Each chunk carries a
char span back to the source, so retrieval results stay traceable. Deterministic,
offline, no API key.

Run it:

    uv run examples/chunk-a-document.py
"""

from __future__ import annotations

from kaos_nlp_core.chunking import SectionChunker, SentenceChunker

LEASE = (
    "ARTICLE I. TERM. The lease term is five years commencing on January 1. "
    "Rent is due monthly on the first business day. "
    "ARTICLE II. MAINTENANCE. The tenant shall maintain the premises in good repair. "
    "No pets are allowed without written consent of the landlord."
)


def main() -> tuple[int, int]:
    # Sentence chunks: whole sentences packed to a token budget.
    sentence_chunks = SentenceChunker(max_tokens=16).chunk(LEASE)
    print(f"SentenceChunker -> {len(sentence_chunks)} chunk(s):")
    for c in sentence_chunks:
        print(f"  [{c.char_span[0]:>3}:{c.char_span[1]:<3}] {c.text}")

    # Section chunks: split on the document's structure (ARTICLE headings).
    section_chunks = SectionChunker().chunk(LEASE)
    print(f"\nSectionChunker -> {len(section_chunks)} chunk(s):")
    for c in section_chunks:
        print(f"  {c.text[:64]}...")

    return len(sentence_chunks), len(section_chunks)


if __name__ == "__main__":
    n_sentence, n_section = main()
    # Multiple sentence chunks (the doc exceeds one 16-token budget)...
    assert n_sentence >= 2
    # ...and every chunk traces back to the source via its char span.
    for c in SentenceChunker(max_tokens=16).chunk(LEASE):
        assert LEASE[c.char_span[0] : c.char_span[1]] == c.text
