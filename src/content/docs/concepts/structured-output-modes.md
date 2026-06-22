---
title: Structured output modes
description: The three ways KAOS gets typed data out of an LLM, and when each applies.
---

When you run a [typed Call](/tutorials/oneliner-to-call-to-program), KAOS has to coax the
model into producing data that matches your `Signature`'s output fields. There are three
mechanisms, picked by the model's capabilities (its `ModelProfile`):

- **Native structured output** — the provider supports a schema/JSON mode directly. KAOS
  hands it the schema and gets back conforming JSON. The most reliable.
- **Tool-based** — the model is given a single "tool" whose arguments are the schema, and
  is asked to call it. Used when native mode isn't available but tool-calling is.
- **Prompted** — the schema is described in the prompt and the response is parsed. The
  universal fallback; the least strict, so KAOS validates and **retries** on a mismatch.

## Why have all three

Providers differ. Hard-coding one mode would either exclude models or sacrifice
reliability. By selecting from a model's `ModelProfile` — capability metadata, not a
`if provider == ...` branch — the same `Call` works across providers and degrades
gracefully.

## Validation is the backstop

Whatever the mode, the output is validated against the Signature. A wrong shape is caught
and retried (a bounded number of times), and an unrecoverable failure becomes a typed
error — never silently-wrong data flowing downstream. This is the same
[fail-closed](/concepts/the-refusal-contract) stance KAOS takes with grounding.
