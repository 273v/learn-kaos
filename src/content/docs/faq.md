---
title: FAQ
description: Straight answers about KAOS — keys, packages, production-readiness, how it compares, and licensing.
---

Quick, honest answers to the questions people ask when evaluating KAOS. For the bigger
picture, see [what is KAOS?](/what-is-kaos) and [how it fits together](/architecture).

## Do I need an API key?

**Not for the golden path.** Every tutorial and most how-tos run **offline** — deterministic
packages run as themselves, and LLM examples use a built-in fake model
([the FunctionClient seam](/concepts/the-offline-seam)). You only need a provider key for the
optional *live* examples, which are clearly badged. Set `KAOS_LEARN_LIVE=1` plus your key to
switch an example to a real model.

## Which packages do I actually need?

As few as **one layer**. The packages are deliberately small and composable — adopt
`kaos-pdf` just to parse PDFs, or `kaos-citations` just to parse citations, without pulling
in agents or LLMs. Dependencies point [downward through the layers](/architecture), never up.

## Is KAOS production-ready?

It's **early** — the packages are at **v0** (0.1.x; a few are alpha), and APIs are still
stabilizing. The *substrate* (documents, citations, NLP, retrieval, tabular) is solid and
deterministic; the agent and LLM-programming layers are moving faster. Pin versions, read the
[changes & deprecations](/reference/changes-and-deprecations) page, and expect some churn.
This site only documents what's real and tested today.

## How is this different from LangChain / LlamaIndex?

Different bets, not a drop-in replacement. KAOS emphasizes:

- **Typed programs over string-prompting** — [signatures and programs](/concepts/typed-llm-programming)
  give validated, typed results, and an [optimizer](/how-to/optimize-a-program) tunes them
  against a metric.
- **Grounding and refusal as first-class outcomes** — answers carry
  [verifiable citations](/concepts/grounding-and-verification) and
  [refuse rather than hallucinate](/concepts/the-refusal-contract). This matters most for
  legal/financial work.
- **A deterministic, offline substrate** — BM25, citations, NLP, graph, and ML run without a
  model or a network, so they're fast, cheap, and testable.
- **MCP-native and offline-testable** — every tool is [serveable over MCP](/concepts/the-mcp-bridge),
  and the whole stack runs deterministically in CI.

## Can AI agents use KAOS directly?

Yes — that's a design goal. Every package's tools are
[MCP-native](/concepts/the-mcp-bridge) and can be [served to a client](/how-to/connect-an-ai-tool)
like Claude Code or Codex. These docs are also published as
[`/llms.txt` and `/llms-full.txt`](https://273v.github.io/learn-kaos/llms.txt) for one-shot
ingestion.

## Why "legal & financial"?

Because that's where **provenance, citations, and refusal** are non-negotiable — a wrong,
confidently-stated answer gets relied upon. The substrate is general-purpose; the design
priorities are tuned for high-stakes document work.

## What are the requirements?

**Python 3.13+** and [**uv**](/get-started/install) — that's the whole setup for running
examples. uv reads each example's [PEP 723](https://peps.python.org/pep-0723/) header and runs
it in a cached, isolated environment.

## Is everything on PyPI?

Most `kaos-*` packages are published to PyPI and install normally. A few app-stack pieces may
need installing from source until everything lands — the [capstone](/tutorials/build-an-app)
and the relevant examples note where this applies.

## What's the license?

**Apache 2.0** — open source, published under [github.com/273v](https://github.com/273v) by
[273 Ventures](https://273ventures.com).
