---
title: Cost as a contract
description: How KAOS makes LLM spend a first-class, enforceable, observable value.
---

LLM cost is easy to lose track of: a multi-step agent can make dozens of model calls per
turn, and a runaway loop can spend real money fast. KAOS treats cost as a **contract** —
enforceable up front, observable after the fact, never an afterthought.

## Cost is on every result

Every agent turn returns real numbers: `response.cost_usd` and `response.total_tokens`
are first-class fields (you read them in [your first agent](/tutorials/first-agent)).
Offline they're `$0.0000`; live they're the actual spend, aggregated across every model
call the turn made. The same numbers surface through MCP tool results and the wire
protocols, so a consumer reads one number regardless of how it called the agent.

## Budgets enforce, they don't just report

```mermaid
flowchart LR
    call["model call"] --> acc["accumulate<br/>cost_usd · tokens"]
    acc --> check{"under Budget<br/>ceiling?"}
    check -->|yes| call
    check -->|no| stop["🛑 refuse further work<br/><small>StopReason: budget_cost</small>"]

    classDef stop fill:#fef2f2,stroke:#ef4444,color:#7f1d1d;
    class stop stop;
```

A `Budget` caps spend *before* it happens. Plans carry a max cost; the agent refuses
further work once the ceiling is reached rather than blowing past it. Cascade and Pareto
strategies spend the cheap model first and escalate only when needed. This is the same
"clever thing is opt-in and accountable" discipline as KAOS's
[retrieval defaults](/concepts/why-plain-bm25).

## Why make it a contract

- **Predictability.** A workflow with a $0.50 per-document cap can't surprise you with a
  $50 bill.
- **Transparency.** Because cost is observed per call and aggregated, you can see exactly
  where spend goes — which tool, which step, which document.
- **Composability.** Cost numbers travel with results, so a pipeline that fans out over a
  corpus can sum spend across stages without bespoke accounting at each one.

## The honest default

There's a subtlety the docs are candid about: some provider/model combinations report
cost as `$0` (e.g. certain reasoning models), and not every tool path is capped at the
same granularity. KAOS documents these gaps rather than hiding them — because a cost
contract you can't trust is worse than none. Anthropic Haiku is the documented default for
examples precisely because its cost accounting is reliable.
