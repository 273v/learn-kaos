---
title: Model registry
description: The license-vetted, SHA-pinned models kaos-nlp-transformers ships, by task.
---

`kaos-nlp-transformers` only loads models from a curated registry — each entry is
**license-reviewed** and **SHA-pinned** (never a moving `main` revision), so a model can't
silently change underneath you. The tasks and their registered families:

| Task | Registered models (examples) | Notes |
|---|---|---|
| **Embeddings** | `minishlab/potion-base-8M`, `potion-base-32M`, `potion-retrieval-32M` (static, `[model2vec]`); `BAAI/bge-small-en-v1.5` (ONNX) | static models load with **no download** — used in the [embeddings how-to](/how-to/semantic-embeddings) |
| **Reranking** | cross-encoder rerankers | re-score query/passage pairs after retrieval |
| **NLI** | small NLI cross-encoders | entailment scoring; satisfies the classify protocol |
| **NER** | GLiNER-style zero-shot extractors | label-driven span extraction |
| **PII** | a closed-label BERT-small token classifier | ~24 PII categories, faster than zero-shot NER |

## How loading works

- The **`ort` (ONNX Runtime) Rust cdylib** is the canonical inference backend; `model2vec`
  is the static-numpy backend for registered static embeddings. No PyTorch in the base
  runtime path.
- Models download on first use into a cache; pre-warm with `kaos-nlp-transformers prefetch`
  and run offline with `KAOS_NLP_TRANSFORMERS_OFFLINE=1`. The vendored static models need
  no download at all.

## Bypassing the registry

You can load an unregistered model with `KAOS_NLP_TRANSFORMERS_ALLOW_UNREGISTERED=true` —
but then **license review and contract-matching are your responsibility**. The registry
exists precisely so the default path is safe. See
[the determinism contract](/concepts/determinism-contract) for why pinning matters.
