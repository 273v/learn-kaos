---
title: Use real data from kl3m
description: Feed the use-case workflows with real legal & financial documents from the public kl3m datasets.
---

The [use-case examples](/use-cases) run on small inline samples so they stay offline and
deterministic. To run them on **real documents at scale**, point them at the public
**kl3m datasets** — a large, openly-licensed corpus of legal and financial text (case law,
contracts, regulations, SEC filings, and more) published by the ALEA Institute on Hugging
Face.

:::caution[Needs network]
Downloading a dataset hits the Hugging Face Hub, so this step isn't part of the offline CI.
The pattern below is the documented recipe.
:::

## Load documents from the Hub

```bash
pip install datasets        # or: uv add datasets
```

```python
from datasets import load_dataset

# Stream the dataset so you don't download it all at once.
ds = load_dataset("alea-institute/kl3m-data-snapshot", split="train", streaming=True)

for row in ds.take(100):
    text = row["text"]            # the document text
    # ...feed `text` into any use-case workflow below.
```

(Browse the available datasets at `huggingface.co/alea-institute` and pick the collection
that matches your workflow — filings, contracts, regulations, etc.)

## Feed it into a use case

Every [use-case example](/use-cases) takes raw document text. Swap the inline sample for a
kl3m row and the same typed contract holds:

```python
# e.g. classify real court documents (the litigation-triage use case)
from kaos_llm_core import Call
# ... build the TriageDoc Call as in examples/uc-litigation-triage.py ...
for row in ds.take(100):
    result = await call(text=row["text"])
    print(result.doc_type)
```

## Notes

- **License-aware by design.** kl3m is built from openly-licensed sources, which is why it's
  safe to use for training and evaluation — the same care KAOS takes with its
  [vetted model registry](/reference/model-registry).
- For **real-time** documents instead of a snapshot, use the `kaos-source` connectors —
  [SEC EDGAR](/how-to/pull-a-sec-filing), Federal Register, and others.
- Pair a real model (`KAOS_LEARN_LIVE=1`, a provider key) with real kl3m documents to run any
  use case end to end; the offline examples prove the workflow first.
