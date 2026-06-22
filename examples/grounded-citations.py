#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-llm-core>=0.1.12,<0.2"]
# ///
"""Verify that a claim is actually supported by its source — or reject it.

This is the heart of KAOS's grounded answers: an LLM doesn't just produce text,
it produces a claim *with a span* pointing at the exact source quote — and that
span is **verified** against the source. A quote that isn't really there fails
verification, so a hallucinated citation is caught instead of trusted.

`Span.verify(source_text)` does the check. It's pure and deterministic — no LLM,
no key — so this runs offline and the same claim always gets the same verdict.

Run it:

    uv run examples/grounded-citations.py
"""

from __future__ import annotations

from kaos_llm_core.signatures.grounding import Span

# A tiny "corpus" — one source document.
SOURCE = (
    "MASTER LEASE AGREEMENT. The lease term is five years commencing January 1. "
    "Rent is due monthly on the first business day. "
    "The tenant may renew for one additional five-year term."
)


def span_for(quote: str) -> Span:
    """Build a Span for a claimed quote. char_span is where the LLM *says* the
    quote is; verify() independently checks the quote really appears there."""
    start = SOURCE.find(quote)
    # If the quote isn't in the source, the offset is unknown — record (0, len)
    # and let verify() reject it.
    start = start if start >= 0 else 0
    return Span(source_uri="lease", quote=quote, char_span=(start, start + len(quote)))


def main() -> list[tuple[str, bool]]:
    # Two claims an LLM might return, each with a supporting span (a quote it
    # says it found in the source).
    claims = [
        ("rent is paid monthly", span_for("Rent is due monthly")),
        # This one is plausible but WRONG — the source says five years, not ten.
        ("the lease runs ten years", span_for("lease term is ten years")),
    ]

    results = []
    for claim, span in claims:
        supported = span.verify(SOURCE)
        verdict = "GROUNDED  ✓" if supported else "REJECTED  ✗ (quote not in source)"
        print(f"  {verdict}  — claim: {claim!r}")
        results.append((claim, supported))
    return results


if __name__ == "__main__":
    results = main()
    # The first claim is grounded; the hallucinated second one is caught.
    assert results[0][1] is True, "expected the real quote to verify"
    assert results[1][1] is False, "a fabricated quote must be rejected"
