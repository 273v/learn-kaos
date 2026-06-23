---
title: The MCP bridge
description: How kaos-mcp exposes any KAOS runtime over the Model Context Protocol — and why it holds no tools of its own.
---

KAOS is MCP-native: every [tool](/tutorials/first-tool) is already typed and annotated for
the [Model Context Protocol](https://modelcontextprotocol.io). `kaos-mcp` is the **bridge**
that serves a runtime's tools (and content resources) to any MCP client — Claude Code,
Codex, or your own.

## A bridge, not a toolbox

```mermaid
flowchart LR
    subgraph RT["Your KaosRuntime"]
        direction TB
        p1["kaos-pdf tools"]
        p2["kaos-source tools"]
        p3["kaos-agents tools"]
    end
    RT --> bridge{{"kaos-mcp<br/><small>bridge — no tools of its own</small>"}}
    bridge -->|stdio| c1["Claude Code"]
    bridge -->|stdio| c2["Codex"]
    bridge -->|HTTP + token| c3["Your client"]

    classDef br fill:#eef2ff,stroke:#6366f1,color:#1e1b4b;
    class bridge br;
```

`kaos-mcp` registers **no tools of its own**. It mounts whatever runtime you give it and
exposes that runtime's tools. So the surface an MCP client sees is entirely determined by
which packages you loaded — `kaos-pdf` + `kaos-source`, say, or the full agent stack. One
bridge, any composition.

## Transports

- **stdio** — `kaos-mcp serve` (or each package's `kaos-*-serve`). The default for
  desktop AI clients that spawn a subprocess.
- **streamable HTTP** — `--http`, which **requires an explicit auth token** (the bridge
  refuses to expose tools over the network unauthenticated — see
  [session enforcement](/concepts/session-enforcement)).

## Resources and URIs

Beyond tools, the bridge exposes content as MCP **resources** addressed by `kaos://` URIs,
so a client can read artifacts and documents the runtime produced, not just call tools.

## Why this design

Keeping the protocol bridge separate from the tools means packages stay usable as plain
Python libraries *and* as MCP servers, with no protocol code leaking into domain logic.
Adding MCP to anything is "mount it on the bridge," not "rewrite it."
