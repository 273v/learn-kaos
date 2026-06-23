---
title: How KAOS fits together
description: The five layers of the KAOS ecosystem and how the kaos-* packages depend on each other.
---

KAOS is not one framework — it's a stack of small packages that share one runtime
and one document model, so they compose. Understanding the **layers** and the
**dependency direction** is the fastest way to know which package you need.

## The five layers

Dependencies point **downward** — higher layers build on lower ones, never the
reverse. You can adopt as little as one layer.

```mermaid
flowchart TB
    apps["<b>Apps &amp; serving</b><br/>kaos-ui · kaos-mcp"]
    agents["<b>Agents</b><br/>kaos-agents<br/><small>memory · patterns · permissions · cost · cites</small>"]
    llm["<b>LLM programming</b><br/>kaos-llm-core · kaos-llm-client<br/><small>signatures · programs · optimizers · FunctionClient</small>"]
    data["<b>Ingestion &amp; data</b><br/>kaos-pdf · kaos-office · kaos-tabular<br/>kaos-source · kaos-web"]
    sub["<b>Deterministic substrate</b><br/>kaos-nlp-core · kaos-graph · kaos-citations<br/>kaos-names · kaos-ml-core · kaos-nlp-transformers"]
    found["<b>Foundation</b><br/>kaos-core <small>(runtime · tools · VFS · settings)</small><br/>kaos-content <small>(the document AST)</small>"]

    apps --> agents --> llm
    llm --> data
    llm --> sub
    data --> found
    sub --> found

    classDef l1 fill:#eef2ff,stroke:#6366f1,color:#1e1b4b;
    classDef l2 fill:#f0f9ff,stroke:#0ea5e9,color:#0c4a6e;
    classDef l3 fill:#f0fdf4,stroke:#22c55e,color:#14532d;
    class apps,agents l1;
    class llm,data,sub l2;
    class found l3;
```

<p style="text-align:center"><small>Dependencies point downward — adopt as little as one layer.</small></p>

## How a request flows

A typical "answer a question over my documents" task touches the stack
top-to-bottom and back:

```mermaid
flowchart LR
    files["📄 files &amp; sources"] --> ingest["<b>Ingestion</b><br/>kaos-pdf · office · web · source"]
    ingest --> doc["<b>ContentDocument</b><br/>kaos-content AST"]
    doc --> index["<b>Substrate</b><br/>BM25 · citations · graph"]
    index --> agent["<b>Agent turn</b><br/>kaos-agents"]
    agent --> prog["<b>LLM program</b><br/>kaos-llm-core + client"]
    prog --> findings["<b>Grounded findings</b><br/>answers + block_ref cites"]
    findings -.cites.-> doc
    findings --> serve["<b>Serve</b><br/>kaos-mcp · kaos-ui"]

    classDef hi fill:#f0fdf4,stroke:#22c55e,color:#14532d;
    class findings hi;
```

1. **Ingestion** (`kaos-pdf`/`kaos-office`/`kaos-web`/`kaos-source`) turns real files
   and sources into a **`ContentDocument`** (`kaos-content`).
2. The **deterministic substrate** (`kaos-nlp-core` BM25, `kaos-citations`,
   `kaos-graph`) indexes, searches, and structures that content — fast, offline.
3. An **agent** (`kaos-agents`) runs a turn: it assembles memory, retrieves relevant
   content, and calls an **LLM program** (`kaos-llm-core`) through a **client**
   (`kaos-llm-client`).
4. The agent returns **grounded findings** — answers with `block_ref` citations back
   into the source documents — under a cost budget and a permission policy.
5. The whole thing can be **served over MCP** (`kaos-mcp`) to an AI client, or wrapped
   in an **app** (`kaos-ui`).

## Two key design choices

- **One document model.** Because every extractor produces the same
  `kaos-content` AST, search, citation, LLM, and agent code is written once — not
  per format. (See [build a document](/tutorials/build-a-document).)
- **One client interface, fake or real.** `kaos-llm-client` exposes every provider
  through one interface, and ships a deterministic `FunctionClient`. That's why this
  whole site runs and tests **offline**. (See
  [the FunctionClient seam](/tutorials/offline-llm-with-functionclient).)

## Where to start

- Build something: follow the [tutorial spine](/tutorials/first-tool).
- Just evaluate: [run an example](/get-started/first-example) in 10 seconds.
- Find the package for a task: [pick your path](/learning-paths).

:::tip
See the [package reference](/reference/packages) for the per-package tool, CLI, and
settings details — generated from each package and drift-checked in CI.
:::
