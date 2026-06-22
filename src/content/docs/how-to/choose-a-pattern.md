---
title: Choose an agent pattern
description: Pick the right kaos-agents pattern for the job — chat, plan, research, or findings.
---

A `kaos-agents` **pattern** decides how a turn executes. Picking the right one is most of
getting an agent to behave. The main patterns:

| Pattern | Use it when… | What it does |
|---|---|---|
| **Chat** | a single-step question or tool use | classifies intent, responds or runs one ReAct tool loop. The simplest; what [your first agent](/tutorials/first-agent) used. |
| **Research** | answering a question over a document corpus | retrieves relevant passages (BM25), answers with **verified citations**, and **refuses** when evidence is weak — the [grounding contract](/concepts/grounding-and-verification). |
| **Plan-execute** | a complex multi-step goal | proposes a plan, executes steps, and can replan — bounded by a [budget](/concepts/optimizers-and-budget). |
| **Findings** | extracting structured findings across many docs | a recall-first extract → filter → synthesize pipeline with per-doc cost caps and typed refusals. |
| **Router** | choosing among the above per turn | classifies the request and dispatches to the right pattern. |

## How to decide

- **One question, maybe one tool?** → Chat.
- **Answer must cite my documents?** → Research.
- **A goal with several steps?** → Plan-execute.
- **Pull the same fields out of 100 contracts?** → Findings.
- **Mixed traffic?** → Router.

All patterns share the same [turn loop](/concepts/the-8-step-turn-loop), memory,
[permissions](/how-to/configure-permissions), and [cost accounting](/concepts/cost-as-a-contract)
— they differ only in how step 4 (dispatch) runs. So switching patterns is a config change
on the [Agent](/concepts/agent-vs-runner), not a rewrite.
