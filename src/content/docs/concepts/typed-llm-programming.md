---
title: Typed LLM programming
description: Why KAOS programs LLMs with types and signatures instead of prompt strings.
---

There are two ways to use an LLM in code.

The **string way**: build a prompt by concatenation, send it, get text back, and parse
that text with regexes or `json.loads`, hoping it's shaped how you asked. Every call
site reinvents prompting, parsing, validation, and retries. The contract lives in your
head.

The **typed way**, which KAOS takes: declare the *contract* — typed inputs and outputs —
and let the framework handle prompting, structured output, validation, and retries.

## Two layers

KAOS splits this across two packages, deliberately:

- **`kaos-llm-client`** is *transport*: the thin, provider-native client. One interface
  over Anthropic / OpenAI / Google, with cost and token accounting. It answers "send
  these messages to this model."
- **`kaos-llm-core`** is *programming*: signatures, programs, codecs, optimizers. It
  answers "given this typed task, produce a validated typed result." It calls down into
  `kaos-llm-client` for transport.

Keeping them separate means program logic never hard-codes a provider, and the transport
layer never grows opinions about your task.

## Signatures and Calls

A **`Signature`** is a typed contract — `InputField`s and `OutputField`s:

```python
class ExtractParties(Signature):
    """Extract the parties named in a contract sentence."""
    text: str = InputField(description="contract text")
    parties: list[str] = OutputField(description="names of the parties")
```

A **`Call`** compiles a signature into a function. `result = await call(text=...)`
returns a *typed object* — `result.parties` is a real `list[str]`, validated, not a blob
of text you have to parse. You saw this in
[from a one-liner to a typed program](/tutorials/oneliner-to-call-to-program).

## Why it's better

- **The contract is explicit and checked.** Wrong-shaped output is caught and retried,
  not silently passed downstream.
- **`ModelProfile` over `if provider == ...`.** Capability metadata travels with the
  model, so you write profile-aware code, not provider conditionals.
- **Programs compose.** A `Program` chains Calls (extract → classify → summarize), each
  typed, with shared budgets and traces. The typed Call is the atom; programs are the
  molecule; agents are the organism.
- **Optimizable.** Because the task is structured, optimizers can improve prompts and
  few-shot examples against a metric — something you can't do with ad-hoc strings.
