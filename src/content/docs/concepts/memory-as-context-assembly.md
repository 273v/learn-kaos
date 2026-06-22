---
title: Memory as context assembly
description: How a KAOS agent decides what to put in the model's context window each turn.
---

An agent's "memory" isn't a transcript you replay. It's a **budgeted assembly problem**:
on every turn, the agent must decide *what* to put in the model's limited context window —
from possibly thousands of messages, documents, and findings.

`kaos-agents` handles this with **`SessionMemory`**: a set of typed sections, each with a
budget, a priority, and an eviction policy.

## Sections, not a blob

Memory is divided into sections (messages, actions, documents, findings, role, playbooks,
a knowledge graph, and more). Each section declares:

- a **token budget** — how much of the context window it may use,
- a **priority** — what gets trimmed first when the total budget is tight,
- an **eviction policy** — FIFO, LRU, LFU, priority, refuse, or none.

`assemble_context()` packs the highest-value content within budget each turn. The
`DOCUMENTS` section is intentionally unbounded so it can hold a full corpus; the retrieval
layer (below) decides which documents actually make it into context.

## Retrieval kicks in at scale

Below a threshold, a section just returns everything (FIFO). Once a section grows past
`retrieval_threshold` items (default 20), the agent switches to **BM25 retrieval** —
selecting the most relevant items for the current query instead of the oldest. This is
why the [why-plain-BM25](/concepts/why-plain-bm25) decision matters: it's the default that
assembles context for every large-corpus turn.

## Persistence and the footgun

Memory hydrates from a virtual filesystem at the start of each turn and persists at the
end — which is what makes a [stateless agent](/concepts/agent-vs-runner) feel continuous.
Streaming sections append to JSONL; snapshot sections checkpoint as JSON.

The catch you must know: the **default VFS is disk-backed**, so session state survives
across runs. In a test, an agent can answer turn 2 from turn 1's stored memory *without
re-doing the work* — a silent false-green. That's why every offline agent example uses
`KaosRuntime.test_mode()` (an in-memory, isolated VFS), as called out in
[your first agent](/tutorials/first-agent).

## Why model it this way

Treating context as an explicit, budgeted, evictable assembly — rather than an
ever-growing prompt — is what lets a KAOS agent work over a 1000-document deal room
without blowing the context window or the budget.
