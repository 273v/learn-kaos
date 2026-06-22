#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "kaos-ml-core>=0.1.2,<0.2",
#   "kaos-nlp-transformers[model2vec]>=0.1.5,<0.2",
#   "numpy",
# ]
# ///
"""Cluster documents by topic — embeddings + k-means, offline.

`kaos-ml-core` provides classical ML over your content. Here we embed a handful
of documents (with the vendored static model, no download) and cluster them with
mini-batch k-means — automatically separating lease clauses from NDA clauses.
This is how you organize a corpus without labels. Deterministic via a fixed seed.

Run it:

    uv run examples/cluster-documents.py
"""

from __future__ import annotations

import os

os.environ.setdefault("KAOS_NLP_TRANSFORMERS_OFFLINE", "1")

import numpy as np  # noqa: E402
import kaos_nlp_transformers as knt  # noqa: E402
from kaos_ml_core.cluster import minibatch_kmeans  # noqa: E402

DOCS = [
    "The lease term is five years with rent due monthly.",       # lease
    "Tenant pays rent each month under the lease agreement.",    # lease
    "Confidential information must be protected for three years.",  # nda
    "The receiving party shall keep all confidential data secret.",  # nda
]


def main() -> list[int]:
    model = knt.EmbeddingModel.load("minishlab/potion-base-8M")
    features = np.asarray(model.embed(DOCS), dtype=np.float32)

    result = minibatch_kmeans(features, n_clusters=2, random_state=0)
    labels = result.labels.tolist()

    print("document -> cluster:\n")
    for doc, label in zip(DOCS, labels):
        print(f"  [{label}]  {doc[:48]}...")
    return labels


if __name__ == "__main__":
    labels = main()
    # The grouping is stable: the two lease docs land together, the two NDA docs
    # land together, and the topics separate. (Cluster *ids* may vary; grouping
    # doesn't.)
    assert labels[0] == labels[1], "lease docs should cluster together"
    assert labels[2] == labels[3], "NDA docs should cluster together"
    assert labels[0] != labels[2], "lease and NDA should be different clusters"
