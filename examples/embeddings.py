#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-nlp-transformers[model2vec]>=0.1.5,<0.2", "numpy"]
# ///
"""Embed text and measure semantic similarity — offline, no download.

`kaos-nlp-transformers` produces dense embeddings for semantic search and
clustering. Most models download on first use, but the vendored static model
`minishlab/potion-base-8M` (the `[model2vec]` extra) loads with **no download**,
so this example runs offline and deterministically.

Run it:

    uv run examples/embeddings.py
"""

from __future__ import annotations

import os

# Force offline so no network model fetch is attempted.
os.environ.setdefault("KAOS_NLP_TRANSFORMERS_OFFLINE", "1")

import numpy as np  # noqa: E402
import kaos_nlp_transformers as knt  # noqa: E402

SENTENCES = [
    "Rent is due monthly on the first.",       # 0
    "The tenant pays rent every month.",       # 1  (similar to 0)
    "The patent covers a novel circuit design.",  # 2  (unrelated)
]


def cosine(a, b) -> float:
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def main() -> tuple[float, float]:
    model = knt.EmbeddingModel.load("minishlab/potion-base-8M")
    vectors = model.embed(SENTENCES)
    print(f"embedded {len(SENTENCES)} sentences -> {vectors.shape[1]}-dim vectors\n")

    sim_related = cosine(vectors[0], vectors[1])
    sim_unrelated = cosine(vectors[0], vectors[2])
    print(f"  sim('rent monthly', 'pays rent every month') = {sim_related:.3f}")
    print(f"  sim('rent monthly', 'patent circuit design')  = {sim_unrelated:.3f}")
    return sim_related, sim_unrelated


if __name__ == "__main__":
    related, unrelated = main()
    # Robust semantic check: the related pair is more similar than the unrelated one.
    assert related > unrelated, f"expected related > unrelated, got {related} vs {unrelated}"
