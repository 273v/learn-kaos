---
title: Why dependency injection
description: Why KAOS passes a runtime explicitly instead of reaching for global state.
---

KAOS code takes a `KaosRuntime` (and a `KaosContext`) as an explicit argument rather than
reading from a global singleton. That's a deliberate choice with concrete payoffs.

## Explicit over ambient

A tool, an agent, an MCP handler — each receives the runtime it should use. Nothing reads
"the current runtime" from module-level state. So two runtimes can coexist in one process:
one in-memory and isolated for a test, one disk-backed for production, a third scoped to a
tenant — without stepping on each other.

## The footgun this avoids

The default virtual filesystem is **disk-backed**, so a runtime's session memory persists
across runs. If runtimes were global, a test would silently inherit a previous run's state
and **false-green** — answering from stored memory instead of re-doing the work. Because the
runtime is injected, a test just constructs an isolated one: `KaosRuntime.test_mode()` gives
an in-memory, throwaway runtime. (This is why every offline agent example here uses it.)

## Payoffs

- **Testability.** Inject a fake or isolated runtime; no global teardown, no cross-test leak.
- **Multi-tenancy.** One process, many isolated runtimes/sessions — see
  [session enforcement](/concepts/session-enforcement).
- **Predictability.** What a piece of code touches is visible in its signature, not hidden
  in import-time state. This is the same explicit-over-magic stance as
  [typed settings](/concepts/settings-resolution).
