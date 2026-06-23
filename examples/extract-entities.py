#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-nlp-transformers>=0.1.5,<0.2"]
# ///
"""Extract entities from text with a local NER model — people, orgs, money, dates.

`kaos-nlp-transformers` ships a zero-shot NER extractor (GLiNER) that pulls typed
entities out of text *without an LLM or API key* — you just name the labels you
want. It runs locally on a small ONNX model. This is the offline
information-extraction backbone for building databases from documents.

Model note: the first run downloads the ONNX model (~tens of MB) from Hugging
Face and caches it; subsequent runs are offline. (To pre-warm a cache for CI or
air-gapped use, see how-to/prefetch-models.)

Run it:

    uv run examples/extract-entities.py
"""

from __future__ import annotations

import kaos_nlp_transformers as knt

TEXT = (
    "On January 5, 2026, Acme Corporation paid $2,500,000 to Jane Doe "
    "to settle the matter under the Master Services Agreement."
)
LABELS = ["person", "organization", "money", "date"]


def main() -> dict[str, str]:
    extractor = knt.GLiNERExtractor.load()
    # extract() takes a batch of texts and returns a list of entity lists.
    entities = extractor.extract([TEXT], labels=LABELS)[0]

    print(f"entities in:\n  {TEXT!r}\n")
    found = {}
    for e in entities:
        print(f"  {e.label:>13}: {e.text!r}  ({e.score:.2f})")
        found[e.label] = e.text
    return found


if __name__ == "__main__":
    found = main()
    # The model reliably pulls the org, the amount, the person, and the date.
    assert found.get("organization") == "Acme Corporation"
    assert "2,500,000" in found.get("money", "")
    assert found.get("person") == "Jane Doe"
    assert "2026" in found.get("date", "")
