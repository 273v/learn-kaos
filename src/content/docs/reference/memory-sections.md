---
title: Memory sections
description: The typed sections a kaos-agents SessionMemory assembles into context each turn.
---

A KAOS agent's `SessionMemory` is divided into typed sections, each with its own token
budget, priority, and eviction policy. Each turn, `assemble_context()` packs the
highest-value content within budget — see
[memory as context assembly](/concepts/memory-as-context-assembly) for the why.

## The sections

| Section | Holds | Notes |
|---|---|---|
| `ROLE` | The agent's role/instructions | Snapshot |
| `MESSAGES` | Conversation turns | Streaming (JSONL); BM25 above threshold |
| `ACTIONS` | Tool calls and results | Streaming; searchable |
| `DOCUMENTS` | The working corpus | Unbounded; retrieval selects what enters context |
| `FINDINGS` | Verified claims with citations | Grounded `Cited[T]` provenance |
| `PLAYBOOKS` | Loaded recipes | Snapshot |
| `PLAN` | The current plan | For plan-execute pattern |
| `GRAPH` | A per-session RDF knowledge graph | PROV-O + citations; Turtle-persisted |
| _…and more_ | Intents, usage, scratch, summaries | 14 sections total |

## Policies

Each section declares:

- **budget_tokens** — its share of the context window (`0` = unbounded, e.g. `DOCUMENTS`).
- **priority** — what's trimmed first when the total budget is tight.
- **eviction_policy** — `FIFO`, `LRU`, `LFU`, `PRIORITY`, `REFUSE`, or `NONE`.

## Retrieval

Below `retrieval_threshold` items (default 20), a section returns everything (FIFO). Above
it, the agent switches to **BM25 retrieval** to select the most relevant items for the
query — the production default (see [why plain BM25](/concepts/why-plain-bm25)).

## Persistence

Streaming sections append to JSONL; snapshot sections checkpoint as JSON; the `GRAPH`
persists as Turtle. Memory hydrates from the VFS at turn start and persists at turn end —
which is why a [stateless agent](/concepts/agent-vs-runner) feels continuous (and why
tests must use `KaosRuntime.test_mode()`).
