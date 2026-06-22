---
title: Glossary
description: The cross-package vocabulary of KAOS, in one place.
---

The terms you'll meet across the KAOS packages and these docs.

## Runtime & tools

- **KaosRuntime** — the dependency-injection container that holds tools, a virtual
  filesystem, artifacts, and settings. Agents and MCP servers run on it.
  (`KaosRuntime.test_mode()` gives an in-memory, isolated one for tests.)
- **KaosTool / `@kaos_tool`** — a typed, MCP-native unit of work. The runtime derives its
  input schema from your type hints.
- **ToolResult** — the typed return of a tool: `.text`, structured content, or a resource
  link.
- **VFS (virtual filesystem)** — KAOS's storage abstraction; sessions and artifacts live
  here. Default backend is disk (a [footgun](/concepts/memory-as-context-assembly) for
  tests — use `test_mode()`).
- **Artifact** — a stored, addressable blob (referenced by a `kaos://` URI).

## Document model

- **ContentDocument** — the Block/Inline AST every extractor produces.
- **Block / Inline** — structural nodes (heading, paragraph, table) vs. content within
  them (text, bold, link).
- **Provenance** — where a node came from (page, bounding box, confidence).
- **block ref** — a stable address into a document (e.g. `#/body/2`), what a citation
  points at.

## LLM programming

- **kaos-llm-client** — the transport layer: one interface over providers.
- **FunctionClient** — a client that runs a Python callable instead of an HTTP request;
  the deterministic [offline seam](/concepts/the-offline-seam).
- **ModelProfile** — typed capability metadata for a model (preferred over
  `if provider == ...`).
- **Signature** — a typed input/output contract for an LLM task.
- **Call** — a Signature compiled into a function returning a validated typed object.
- **Program** — a composition of Calls (extract → classify → summarize).
- **Cited[T] / Span** — a typed value with verifiable supporting spans; `Span.verify`
  checks a quote against its source.

## Agents

- **Agent** — frozen agent *config* (instructions, model, pattern, tools).
- **Runner** — the *engine* that drives an Agent over a runtime.
- **Pattern** — how a turn executes: chat, plan-execute, research, findings, router.
- **SessionMemory** — budgeted, sectioned context assembled per turn.
- **Hook** — an observer of the [event stream](/concepts/events-and-spans) (logging,
  cost, OTel, circuit breaker).
- **PermissionPolicy** — rules gating tool calls (read-only auto-allowed, destructive
  auto-asked).
- **Span / value event** — phase boundaries vs. facts in the typed event stream.

## Protocol & serving

- **MCP (Model Context Protocol)** — the standard KAOS exposes tools over; `kaos-mcp`
  bridges any runtime to it.
- **`kaos-*-serve`** — each package's MCP server entry point.
