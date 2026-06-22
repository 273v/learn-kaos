---
title: Pick your path
description: KAOS serves different kinds of learners. Choose the route that matches why you're here.
---

KAOS docs are organized the [Diátaxis](https://diataxis.fr/) way — tutorials (learn),
how-to guides (do a task), reference (look up facts), and explanation (understand).
Different readers need different doors. Find yours.

> Pages marked _(soon)_ are planned and land in upcoming milestones. The links that
> work today take you to live, tested pages.

## "Just show me it works"

You want proof, fast — no setup, no key.

1. [Run your first example](/get-started/first-example) — deterministic, ~10 seconds.
2. [Browse the gallery](/gallery) — pick any card, one `uv run`.
3. [How KAOS fits together](/architecture) — the 60-second mental model.

## "Teach me, step by step"

You want to learn KAOS properly, building as you go. Follow the **golden path** —
each tutorial builds on the last, all runnable offline:

1. [Your first tool](/tutorials/first-tool)
2. [Build a document](/tutorials/build-a-document)
3. [Offline LLM with FunctionClient](/tutorials/offline-llm-with-functionclient)
4. [Your first model call](/tutorials/first-model-call)
5. [From a one-liner to a typed program](/tutorials/oneliner-to-call-to-program)
6. [Your first agent](/tutorials/first-agent)
7. Research agent with citations _(soon)_ → Build an app _(soon)_

## "I have a specific task"

You're competent and want a recipe, not a lesson. The how-to cookbook _(growing)_
covers tasks like:

- [Run your first example](/get-started/first-example) (extract citations) — live today
- Ingest a PDF / Office doc / spreadsheet _(soon)_
- Cap LLM cost, switch providers _(soon)_
- Build a BM25 index, find near-duplicates, rank a graph _(soon)_

## "I want the facts"

You want exact API, CLI, tool, and setting details. Generated reference _(soon)_:
per-package API, the full MCP tool inventory, CLI flags, and environment variables —
all generated from source so they can't drift.

## "I want to understand the design"

You want the *why*. Start with [how KAOS fits together](/architecture); the concepts
section _(growing)_ explains the agent loop, memory, retrieval choices, the
cost-as-a-contract model, and grounded citations.

## "I want to extend KAOS"

You're a contributor or module author. Start with [your first tool](/tutorials/first-tool)
and [how KAOS fits together](/architecture); the module-authoring track and the
[offline-testing pattern](/get-started/first-example) for contributors land next.

## "I want to use KAOS from an AI agent"

You want KAOS tools inside Claude Code, Codex, or another MCP client. The
MCP-consumer track — connect an AI tool, serve a runtime over MCP, and the tool
reference — lands in an upcoming milestone.
