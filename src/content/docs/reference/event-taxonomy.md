---
title: Event taxonomy
description: The typed events a kaos-agents turn emits, and the Span phase model.
---

A KAOS agent turn is a typed [event stream](/concepts/events-and-spans). Events come in two
shapes: **Spans** (phase boundaries) and **value events** (facts).

## Span — the universal phase boundary

A `Span` marks the start, completion, or error of a phase, carrying `span_id`,
`parent_span_id`, `duration_ms`, and `attributes`. Consumers pattern-match on
`(subject, phase)`.

**Subjects** include: `TURN`, `STEP`, `TOOL_CALL`, `SUBAGENT`, `HANDOFF`.
**Phases**: `START`, `COMPLETE`, `ERROR`.

This OTel-aligned model is what an `OTelHook` maps onto standard tracing spans.

## Value events — facts with payload

Concrete typed events that carry information beyond a phase boundary:

| Event | Meaning |
|---|---|
| `IntentClassified` | The classified user intent for the turn |
| `PlanProposed` | A proposed plan (plan-execute pattern) |
| `CitationFound` | A grounded citation was produced |
| `UsageObserved` | Token/cost usage from a model call |
| `EvidenceInsufficient` | A typed refusal — not enough support to answer |
| `GroundingRefusalTriggered` | A grounded-output refusal |
| `MemoryEvent` | A memory mutation (`ADDED`/`EVICTED`/`SUMMARIZED`/`HYDRATED`/`PERSISTED`/`SEARCHED`) |
| `TurnSummary` | The terminal aggregate (text, tokens, cost) of a successful turn |
| `RunError` / `BudgetExceeded` | Terminal error events |
| `ToolCallApprovalRequired` | Control-flow: a tool call needs approval |
| Stream deltas | `TextDelta`, `ThinkingDelta`, `ToolCallArgsDelta` for live streaming |

## Why two shapes

Phase boundaries are uniform and frequent, so one `Span` type with a subject/phase keeps
the stream small and OTel-mappable. Facts carry varied payloads, so they stay typed
classes you match with `isinstance`. Hooks (logging, cost, OTel, circuit breaker) observe
both uniformly — which is what makes turns traceable and the
[audit trail](/concepts/the-audit-trail) possible.
