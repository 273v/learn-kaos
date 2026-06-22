---
title: Connect KAOS to an AI tool
description: Make KAOS tools available inside Claude Code, Codex, or another MCP client.
---

KAOS tools can run inside your AI coding tool over MCP. `kaos-*` packages each ship a
`*-serve` command, and `kaos setup` writes the client config for you.

:::caution[Needs an external AI client]
This wires KAOS into a third-party MCP client you run separately. The result — KAOS tools
appearing in that client — happens in *that* tool, so there's nothing for this site's CI to
assert. The commands below are the documented setup.
:::

## Write the client config

```bash
# Configure a specific client to launch KAOS MCP servers
kaos setup claude --scope project     # Claude Code (writes .mcp.json)
kaos setup codex                      # Codex
kaos setup gemini                     # Gemini
```

This registers the relevant `kaos-*-serve` commands so the client can start them.

## Or point a client at one server directly

Most MCP clients accept a stdio server command. Add, for example:

```jsonc
{
  "mcpServers": {
    "kaos-pdf": { "command": "kaos-pdf-serve" },
    "kaos-agents": { "command": "kaos-agents-serve", "args": ["--with-source", "--with-web"] }
  }
}
```

Restart the client; the KAOS tools appear in its tool list.

## Notes

- What a client sees is exactly the runtime's tools — see [the MCP bridge](/concepts/the-mcp-bridge)
  and [serve over MCP](/tutorials/serve-over-mcp) for how that's assembled.
- For network serving instead of stdio, see [serve over HTTP](/how-to/serve-over-http) — it
  requires an auth token.
- The [MCP tools reference](/reference/mcp-tools) lists what each package exposes.
