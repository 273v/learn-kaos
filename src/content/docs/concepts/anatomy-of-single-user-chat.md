---
title: Anatomy of a KAOS app
description: How the single-user-chat reference app wires kaos-agents into a real FastAPI + React product.
---

The `kaos-ui` `web:spa` template (the [capstone](/tutorials/build-an-app) you scaffolded)
isn't a toy — it's a complete reference architecture for putting a KAOS agent in front of
users. Knowing its shape shows how the pieces fit in production.

## The backend

A FastAPI app built on `kaos-agents`:

- **Auth.** A bearer token gates every request; each request carries an identity that scopes
  the session (see [session enforcement](/concepts/session-enforcement)).
- **Streaming.** The agent's [event stream](/concepts/events-and-spans) is proxied to the
  browser over **SSE**, so the UI renders tokens, tool calls, and citations as they happen.
- **State.** Each session's files live in a per-session virtual-filesystem namespace; a
  `meta.json` sidecar tracks session metadata. The agent is
  [stateless](/concepts/agent-vs-runner) — all continuity is the hydrated session memory.
- **Safety.** A read-only tool allowlist and the [permission policy](/how-to/configure-permissions)
  bound what the agent can do on a user's behalf; a circuit breaker stops runaway loops.

## The frontend

A Vite + React SPA: it sends a message, consumes the SSE event stream, and renders a typed
**event dispatch table** — text deltas, tool-call chips, citations, cost. Markdown is
rendered with link sanitization; stop/cancel controls map to the run lifecycle.

## Why study it

It answers the questions every real deployment hits: how do I authenticate, stream, isolate
tenants, bound cost and tools, and surface citations? The template ships all of that wired
together — so "build a product on KAOS" starts from a working architecture, not a blank
file. (Running it needs a provider key, and some packages from source until everything is on
PyPI — see the capstone's notes.)
