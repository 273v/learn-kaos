#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-nlp-core>=0.1.6,<0.2"]
# ///
"""Detect near-duplicate text with MinHash.

Exact hashing tells you if two documents are *identical*; MinHash tells you if
they're *nearly* identical — the question that matters for contract versions,
boilerplate clauses, and deduplicating a corpus. `kaos-nlp-core` shingles the
text into overlapping token n-grams and estimates their Jaccard similarity from
compact MinHash signatures.

Fully offline and deterministic.

Run it:

    uv run examples/near-duplicates.py
"""

from __future__ import annotations

from kaos_nlp_core.hashing import MinHasher

# Two versions of the same clause (one word changed) + an unrelated clause.
CLAUSE_V1 = (
    "The Tenant shall pay rent monthly on the first business day of each month "
    "and any late payment incurs a five percent fee on the outstanding balance"
)
CLAUSE_V2 = (
    "The Tenant shall pay rent monthly on the first business day of every month "
    "and any late payment incurs a five percent fee on the outstanding balance"
)
UNRELATED = (
    "Confidential Information must be protected by the Receiving Party for a "
    "period of three years following the date of disclosure"
)


def main() -> tuple[float, float]:
    hasher = MinHasher()
    # 3-token shingles over the lowercased words.
    sig_v1 = hasher.hash_token_shingles(CLAUSE_V1.lower().split(), 3)
    sig_v2 = hasher.hash_token_shingles(CLAUSE_V2.lower().split(), 3)
    sig_u = hasher.hash_token_shingles(UNRELATED.lower().split(), 3)

    near_dup = sig_v1.jaccard(sig_v2)
    unrelated = sig_v1.jaccard(sig_u)
    print(f"  similarity(clause v1, clause v2 — one word changed) = {near_dup:.3f}")
    print(f"  similarity(clause v1, unrelated NDA clause)         = {unrelated:.3f}")
    return near_dup, unrelated


if __name__ == "__main__":
    near_dup, unrelated = main()
    # Near-duplicate scores high; the unrelated clause scores zero.
    assert near_dup > 0.5, f"expected high near-dup similarity, got {near_dup}"
    assert unrelated == 0.0
