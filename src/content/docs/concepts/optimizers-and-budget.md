---
title: Optimizers & budget
description: How KAOS improves LLM programs against a metric, and bounds what they spend.
---

Because a KAOS LLM program is [typed and structured](/concepts/typed-llm-programming) — not
an ad-hoc prompt string — two things become possible that aren't with hand-written prompts:
**optimization** and **budgeting**.

## Optimizers

An optimizer improves a program (its prompts and few-shot examples) against a **metric**,
using recorded examples — rather than you hand-tuning prompts by feel. The family includes
bootstrap-style few-shot selection and instruction optimization. Because the task is a
`Signature` with a measurable output, "is this version better?" is an answerable question,
run automatically.

This is the same evidence-over-intuition stance as [why plain BM25](/concepts/why-plain-bm25):
prefer the thing a metric says is better to the thing that *feels* better.

## Budget

A shared `Budget` bounds a program or agent run by **cost** (`max_cost_usd`), **trials**,
**tokens**, or **wall-clock time**. It enforces *before* spend happens — the run refuses
further work at the ceiling rather than blowing past it (see
[cost as a contract](/concepts/cost-as-a-contract)). Cascade and Pareto strategies spend
the cheap model first and escalate only when needed.

## Why they belong together

Optimization makes a program *better*; budget makes it *bounded*. Together they let you
ship an LLM program you can both trust to perform and trust not to surprise you on the
invoice — the two questions that decide whether LLM automation is production-ready.
