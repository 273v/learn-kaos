#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-nlp-core>=0.1.6,<0.2", "kaos-llm-core>=0.1.12,<0.2"]
# ///
"""The skeleton of a grounded research agent: retrieve, answer, verify — or refuse.

A research agent over a document corpus does three things: it RETRIEVES the
relevant source for a question (BM25), ANSWERS from it, and VERIFIES the answer's
citation against the source — and if no source is relevant, it REFUSES instead of
guessing. This example wires those verified primitives together over a tiny
corpus, fully offline and deterministic.

A production agent uses an LLM for the answer step (offline via FunctionClient);
here we keep it deterministic to show the retrieve -> ground -> refuse contract
without any model at all.

Run it:

    uv run examples/research-over-corpus.py
"""

from __future__ import annotations

from kaos_llm_core.signatures.grounding import Span
from kaos_nlp_core.search import Searcher

# A tiny synthetic corpus (no licensing risk).
CORPUS = {
    0: "Master Lease. The lease term is five years. Rent is due monthly on the first.",
    1: "Mutual NDA. Confidential Information must be protected for three years.",
    2: "Services Agreement. The vendor shall deliver the software by the milestone dates.",
}
RECORDS = [{"id": i, "text": t} for i, t in CORPUS.items()]


def answer(question: str, searcher: Searcher, quote: str) -> str:
    """Retrieve the best source, then verify the supporting quote against it.
    Returns a grounded answer, or a refusal when nothing relevant is found."""
    hits = searcher.search(question, top_k=1)
    if not hits:
        return "REFUSED: no source in the corpus supports that question."

    source = CORPUS[hits[0].doc_id]
    start = max(source.find(quote), 0)
    span = Span(source_uri=str(hits[0].doc_id), quote=quote, char_span=(start, start + len(quote)))
    if not span.verify(source):
        return "REFUSED: the supporting quote does not appear in the retrieved source."
    return f"GROUNDED: {quote!r} (from doc {hits[0].doc_id})"


def main() -> list[str]:
    searcher = Searcher.from_documents(RECORDS)
    results = [
        # A question the corpus supports, with a real quote -> grounded.
        answer("when is rent due", searcher, quote="Rent is due monthly"),
        # A question nothing in the corpus addresses -> refuse.
        answer("what are the patent infringement damages", searcher, quote="patent damages"),
    ]
    for r in results:
        print(f"  {r}")
    return results


if __name__ == "__main__":
    results = main()
    assert results[0].startswith("GROUNDED"), results[0]
    assert results[1].startswith("REFUSED"), results[1]
