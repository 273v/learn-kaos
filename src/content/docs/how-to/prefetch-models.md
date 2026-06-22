---
title: Prefetch models for offline use
description: Warm the model cache once so kaos-nlp-transformers runs offline afterward.
---

`kaos-nlp-transformers` downloads ONNX models on first use. To run **fully offline**
afterward (CI, air-gapped, or just deterministic), pre-warm the cache once, then enforce
offline mode.

## Prefetch, then go offline

```bash
# Download the models you'll use into the cache (one time, needs network)
kaos-nlp-transformers prefetch --include embedding --include reranker
# ...or a specific model
kaos-nlp-transformers prefetch --model BAAI/bge-small-en-v1.5

# Afterwards, force offline so no network fetch is attempted
export KAOS_NLP_TRANSFORMERS_OFFLINE=1
```

```bash
kaos-nlp-transformers info     # confirm what's cached and the active device
```

## Notes

- The vendored static model **`minishlab/potion-base-8M`** (the `[model2vec]` extra) needs
  **no prefetch at all** — it loads with no download, which is why the
  [embeddings how-to](/how-to/semantic-embeddings) and
  [clustering how-to](/how-to/cluster-a-corpus) run offline out of the box.
- Models are [license-vetted and SHA-pinned](/reference/model-registry); prefetch respects
  the registry.
- Cache location follows `KAOS_NLP_TRANSFORMERS_CACHE_DIR` / `HF_HOME` (see
  [environment variables](/reference/env-vars)).
