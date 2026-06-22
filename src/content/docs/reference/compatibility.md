---
title: Compatibility & caveats
description: Python and platform requirements, provider caveats, and version sources.
---

## Python & platforms

- **Python 3.13+** is required by every `kaos-*` package.
- The Rust-backed packages (`kaos-nlp-core`, `kaos-graph`, `kaos-ml-core`,
  `kaos-nlp-transformers`) ship prebuilt **`abi3` wheels** — no Rust toolchain needed to
  install or use them.
- All packages are **Apache-2.0** licensed.

## Versions

Live versions are on the [package reference](/reference/packages) (PyPI badges). For the
authoritative version of any package:

```bash
uv run --with kaos-core python -c "import kaos_core; print(kaos_core.__version__)"
```

The packages are pre-1.0 and move quickly; pin versions in production
(`uv add 'kaos-core>=0.1,<0.2'`).

## LLM provider caveats

These matter when you run the *live* path (the offline `FunctionClient` path is unaffected):

- **Anthropic Haiku is the documented default** for examples on this site — it's cheap and
  has reliable cost accounting.
- **OpenAI reasoning models are not supported for the findings pattern** — they're
  incompatible with the `temperature=0` the pattern needs, and some report cost as `$0`
  (see [cost as a contract](/concepts/cost-as-a-contract) on the honest cost gaps).
- Set provider keys via `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / `GOOGLE_API_KEY`, or the
  `KAOS_LLM_*` equivalents (which take precedence). Keys are held in `SecretStr` and
  redacted from logs and output.

## On-demand downloads & network

- **kaos-nlp-transformers** downloads ONNX models on first use; pre-warm with
  `kaos-nlp-transformers prefetch`. The vendored `potion-base-8M` (via the `[model2vec]`
  extra) loads with **no download**.
- **kaos-web** browser automation needs `uv run playwright install chromium`; HTTP
  extraction works without it.
- **kaos-source** REST connectors hit live government APIs (EDGAR requires a `User-Agent`
  containing an email; GovInfo needs an API key; Federal Register / eCFR need neither).

## Maturity note

`kaos-ml-core` is at an early (v0) stage: its CLI and serve entry points are stubs and the
Rust crate exposes only a version probe. Use its **Python API and MCP tools** as the real
surface; treat the CLI as not-yet-implemented.
