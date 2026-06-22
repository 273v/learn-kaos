---
title: MCP tools
description: How KAOS exposes tools over the Model Context Protocol, and how many each package ships.
---

KAOS is MCP-native: every tool is typed, annotated, and exposable over the
[Model Context Protocol](https://modelcontextprotocol.io). Each package ships a
`kaos-*-serve` entry point that serves its tools to any MCP client (Claude Code, Codex, …);
`kaos-mcp` bridges any runtime to MCP over stdio or streamable HTTP.

## Tools per package

Approximate counts (the authoritative list is generated per package — see below):

| Package | MCP tools | Serve command |
|---|---:|---|
| kaos-core | ~10 | — (use kaos-mcp) |
| kaos-content | ~17 | — |
| kaos-llm-client | ~7 | `kaos-llm-serve` |
| kaos-llm-core | ~32 | `kaos-llm-core-serve` |
| kaos-agents | ~14 (+7 retrieval) | `kaos-agents-serve` |
| kaos-pdf | ~8 | `kaos-pdf-serve` |
| kaos-office | ~18 | `kaos-office-serve` |
| kaos-tabular | ~17 | `kaos-tabular-serve` |
| kaos-source | ~30 | `kaos-source-serve` |
| kaos-web | ~45 | `kaos-web-serve` |
| kaos-nlp-core | ~17 | `kaos-nlp-serve` |
| kaos-nlp-transformers | ~7 | `kaos-nlp-transformers-serve` |
| kaos-ml-core | ~11 | `kaos-ml-serve` |
| kaos-graph | ~17 | `kaos-graph-serve` |
| kaos-citations | 3 | `kaos-citations-serve` |
| kaos-ui | 4 (read-only) | — |
| kaos-mcp | 0 (pure bridge) | `kaos-mcp serve` |
| kaos-names | 0 | — |

:::note
Counts are intentionally shown as approximate here — the **single source of truth** is each
package's tool registry (the monorepo's `scripts/inventory.py` enumerates every tool,
resource, and schema). Prose on this site never hard-codes exact counts elsewhere, so the
docs can't drift from the packages.
:::

## How tools are exposed

- Every tool is a `KaosTool` with typed inputs (schema derived from type hints) and
  [annotations](/tutorials/first-tool) (`readOnlyHint`, `destructiveHint`, …) that let an
  agent's [permission policy](/concepts/agent-vs-runner) decide what to auto-allow.
- `kaos-mcp` mounts a whole runtime: `kaos-mcp serve` (stdio) or `--http` (streamable
  HTTP, which requires an explicit auth token).
- Connect a serve command to an MCP client to make KAOS tools available inside it.

## Enumerate tools live

```bash
uv run --with kaos-pdf kaos-pdf-serve --help     # or list-tools via kaos-mcp
```
