---
title: Set up to build
description: Go from running examples to building your own KAOS project with uv.
---

[Install](/get-started/install) covered the one tool you need to *run* examples: `uv`.
This page sets you up to *build* your own KAOS project.

## Start a project

```bash
uv init my-kaos-project
cd my-kaos-project
```

## Add the packages you need

KAOS is à la carte — add only the layers you'll use. A few common starting points:

```bash
# Foundation + document model
uv add kaos-core kaos-content

# LLM programming
uv add kaos-llm-client kaos-llm-core

# Agents (pulls in the LLM layer)
uv add kaos-agents

# Deterministic substrate (offline, no key)
uv add kaos-nlp-core kaos-citations kaos-graph kaos-names
```

All packages require **Python 3.13+** and are Apache-2.0 licensed. The Rust-backed
packages (`kaos-nlp-core`, `kaos-graph`, `kaos-ml-core`, `kaos-nlp-transformers`) ship
prebuilt `abi3` wheels — no Rust toolchain needed to use them.

## Provider keys (only for live LLM calls)

Deterministic packages and the `FunctionClient`
[offline path](/tutorials/offline-llm-with-functionclient) need **no keys**. To make
*live* LLM calls, set a provider key:

```bash
export ANTHROPIC_API_KEY=sk-...     # the documented default for KAOS examples
# or OPENAI_API_KEY / GOOGLE_API_KEY
```

KAOS reads these via typed settings (`KAOS_LLM_*` env vars also work and take
precedence). Keys are held in `SecretStr` and redacted from logs and output.

## Verify

```bash
uv run python -c "import kaos_core; print(kaos_core.__version__)"
```

You're ready. Follow the [tutorial spine](/tutorials/first-tool) to build something, or
browse the [how-to cookbook](/how-to/search-text-with-bm25) for task recipes.
