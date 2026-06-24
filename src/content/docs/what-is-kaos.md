---
title: What is KAOS?
description: KAOS (Kelvin Agentic Operating System) is an open-source ecosystem of composable packages for agentic legal and financial data work.
---

**KAOS — the Kelvin Agentic Operating System — is open agentic infrastructure for legal and
financial work**, built by [273 Ventures](https://273ventures.com) and published
as a family of small, composable `kaos-*` packages under
[github.com/273v](https://github.com/273v).

It is not a single framework you adopt wholesale. It is a set of building blocks
that share one type system and one runtime, so they compose cleanly:

- **A runtime and tool model** (`kaos-core`) — an MCP-native type system, a
  dependency-injection runtime, a virtual filesystem, and an artifact store that
  every other package builds on.
- **A document model** (`kaos-content`) — one Block/Inline AST with provenance,
  so a PDF, a DOCX, a web page, and a spreadsheet all become the same shape.
- **Ingestion** (`kaos-pdf`, `kaos-office`, `kaos-tabular`, `kaos-source`,
  `kaos-web`) — turn real documents and data sources into that AST.
- **LLM programming** (`kaos-llm-client`, `kaos-llm-core`) — provider-native
  clients plus typed, composable, optimizable LLM "programs".
- **Agents** (`kaos-agents`) — a stateful agent runtime with memory, patterns,
  permissions, cost accounting, and grounded-citation findings.
- **A deterministic substrate** (`kaos-nlp-core`, `kaos-graph`, `kaos-citations`,
  `kaos-ml-core`, `kaos-nlp-transformers`, `kaos-names`) — fast, offline NLP,
  graph, citation, and ML primitives.
- **Apps and serving** (`kaos-ui`, `kaos-mcp`) — scaffold user-facing apps and
  expose any runtime over the Model Context Protocol.

## Two audiences

- **Python developers** build pipelines and apps directly against the packages.
- **AI agents** consume the same capabilities over MCP — every package can serve
  its tools to Claude Code, Codex, or any MCP client.

## How to learn it here

This site teaches KAOS **by running it**. The recommended order — the *golden
path* — starts simple and deterministic, then layers on LLMs and agents:

1. [Run your first example](/get-started/first-example) (no key, ~10 seconds)
2. [Install the toolchain](/get-started/install)
3. Author and run a tool, build a document, call a model, and build an agent —
   the guided tutorials (landing milestone by milestone).

Everything you run on the spine works **offline**: deterministic packages run as
themselves, and LLM steps use a built-in fake model so you never need an API key
to learn.

:::note
Learn KAOS is being built in public, milestone by milestone. This is the **M0**
foundation: the home, install, your-first-example, and the gallery. The full
tutorial spine, how-to cookbook, concepts, and generated reference are on the way.
:::
