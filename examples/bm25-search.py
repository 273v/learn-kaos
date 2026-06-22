#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-nlp-core>=0.1.6,<0.2"]
# ///
"""Rank sentences by relevance with BM25 — fast, offline retrieval.

`kaos-nlp-core` is a Rust-backed NLP engine. `search_sentences` segments a
block of text into sentences and ranks them against a query with BM25 — the
classic lexical retrieval algorithm agents use to pull relevant context out
of a corpus. No model, no key, fully deterministic.

Run it:

    uv run examples/bm25-search.py
"""

from __future__ import annotations

from kaos_nlp_core.search import search_sentences

TEXT = (
    "The lease term is five years. "
    "Rent is due monthly on the first. "
    "The tenant may renew for an additional term. "
    "Late rent incurs a five percent fee."
)


def main() -> list:
    hits = search_sentences(TEXT, "rent", top_k=3)
    print(f'Top matches for "rent":\n')
    for h in hits:
        # Each hit carries the matched sentence, its BM25 score, and the
        # character span it occupies in the source text.
        print(f"  {h.score:.3f}  {h.text!r}  (chars {h.start}-{h.end})")
    return hits


if __name__ == "__main__":
    hits = main()
    assert hits, "expected at least one hit"
    assert "Rent" in hits[0].text, f"unexpected top hit: {hits[0].text!r}"
