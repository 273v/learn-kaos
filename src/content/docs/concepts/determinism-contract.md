---
title: The determinism contract
description: Why so much of KAOS is byte-for-byte reproducible — and how the Rust core delivers it.
---

Much of KAOS is **deterministic**: the same input yields the same output, every time. That
isn't an accident — it's a contract that makes the system testable, auditable, and cheap to
run offline (it's why this whole site's gallery runs in CI without flaking).

## What's deterministic

The non-LLM substrate: `kaos-citations`, `kaos-graph`, `kaos-nlp-core`, the static
`model2vec` embeddings, `kaos-content` serialization, `kaos-core` tool execution. Pass a
seed (e.g. `kaos-names`' `rng=`) and even the "random" parts are reproducible.

## How the Rust core delivers it

The performance-critical packages are **Rust with a thin Python API** (PyO3), shipped as
`abi3` wheels. The Rust core does the heavy lifting — SIMD string ops, petgraph algorithms,
BM25 — with no GPU nondeterminism and no Python-level floating-point drift in the hot path.
You write Python; the determinism comes from the compiled core.

## Where determinism ends

LLM calls are inherently variable. KAOS draws the line cleanly: deterministic packages are
deterministic; LLM steps are isolated behind the [client interface](/concepts/the-offline-seam),
where `FunctionClient` makes even *those* reproducible for tests. So "tested offline" and
"works live" are the same code, and the parts that *can* be reproducible *are*.

## Why it matters

Determinism is what lets a citation be **verified**, an audit trail be **replayed**, and a
benchmark be **trusted**. A system you can't reproduce is one you can't really check.
