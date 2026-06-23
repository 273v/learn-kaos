---
title: The agent turn loop
description: What actually happens inside a single kaos-agents turn.
---

A [Runner](/concepts/agent-vs-runner) turn isn't a single LLM call — it's a structured
loop. Understanding its shape makes agent behavior predictable and debuggable.

## The anatomy of a turn

```mermaid
flowchart TD
    msg["1 · Add message<br/>to memory"] --> ctx["2 · Assemble context<br/><small>budgeted sections + BM25</small>"]
    ctx --> intent["3 · Classify intent"]
    intent --> dispatch{"4 · Dispatch"}
    dispatch -->|respond| chat["Direct response"]
    dispatch -->|tool use| react["ReAct loop"]
    dispatch -->|research| rag["RAG pass"]
    dispatch -->|plan| plan["Plan-execute"]
    chat --> run
    react --> run
    rag --> run
    plan --> run
    run["5 · Run program<br/><small>tools under permissions + budget</small>"] --> mem["6 · Update memory<br/><small>actions · findings · usage</small>"]
    mem --> persist["7 · Persist to VFS"] --> summary["8 · Emit TurnSummary<br/><small>+ Span(TURN, COMPLETE)</small>"]

    classDef step fill:#f0f9ff,stroke:#0ea5e9,color:#0c4a6e;
    classDef branch fill:#eef2ff,stroke:#6366f1,color:#1e1b4b;
    classDef done fill:#f0fdf4,stroke:#22c55e,color:#14532d;
    class msg,ctx,intent,run,mem,persist step;
    class dispatch,chat,react,rag,plan branch;
    class summary done;
```

1. **Add the message** to session memory.
2. **Assemble context** — [budgeted section assembly](/concepts/memory-as-context-assembly),
   with BM25 retrieval over large sections.
3. **Classify intent** — what does the user want (respond, tool use, research, plan,
   clarify)?
4. **Dispatch** to the matching behavior: a direct response, a ReAct tool loop, a research
   (RAG) pass, or a plan-execute run.
5. **Run the chosen program**, calling tools under the [permission policy](/concepts/session-enforcement)
   and the [cost budget](/concepts/cost-as-a-contract).
6. **Update memory** — record actions, findings (with citations), and usage.
7. **Persist** the session to the VFS.
8. **Emit a `TurnSummary`** — the typed aggregate (text, tokens, cost) alongside the
   terminal `Span(TURN, COMPLETE)`.

## Why a loop, not a call

- **Observability.** Each step emits [events](/concepts/events-and-spans), so the whole
  turn is traceable and auditable.
- **Control.** Permissions, cost, and circuit breakers apply *between* steps — the loop is
  where the guardrails live.
- **Composability.** ReAct is the inner loop; the agent is the outer loop. The agent
  decides *which* program to run; the program drives the model. Patterns (chat, research,
  findings, plan-execute) differ only in step 4's dispatch.
