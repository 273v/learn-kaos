---
title: Transport vs. programming
description: Where kaos-llm-client ends and kaos-llm-core begins — and why the split matters.
---

KAOS deliberately splits LLM work across two packages. Knowing which does what saves you
from reaching for the wrong tool.

## kaos-llm-client — transport

The **client** answers one question: *send these messages to this model, get a response.*
It's a thin, provider-native layer — one interface over Anthropic / OpenAI / Google, with
streaming, tool-calling, cost and token accounting, and the deterministic `FunctionClient`
[test double](/concepts/the-offline-seam). It knows about HTTP, providers, and retries. It
knows nothing about your task.

## kaos-llm-core — programming

The **core** answers a different question: *given this typed task, produce a validated,
typed result.* Signatures, programs, codecs, optimizers, grounding. It composes Calls into
programs, validates output, and improves prompts against a metric. It knows about your
task. It calls *down* into the client for transport, and never talks HTTP itself.

## Why the split

- **Program logic never hard-codes a provider.** Swap models or providers without touching
  your [signatures and programs](/concepts/typed-llm-programming).
- **Transport never grows task opinions.** The client stays small and reusable; new
  providers fit the same contract.
- **You can use either alone.** Need raw chat? Use the client. Need typed extraction? Use
  the core. The boundary is clean enough that each is useful by itself.

The same shape repeats one layer up: [agents](/concepts/agent-vs-runner) are the *outer*
loop over llm-core's programs, which are the loop over the client's calls.
