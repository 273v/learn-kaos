---
title: Inspect a runtime from the CLI
description: List tools, browse the VFS, and check settings with the kaos-core CLI.
---

When you're building with KAOS, the `kaos-core` CLI lets you look inside a runtime —
what tools are registered, what's in the virtual filesystem, what settings are active —
without writing code.

```bash
# List registered tools (add --json for machine-readable output)
kaos-core tools list
kaos-core tools search "pdf" --category document

# Browse the virtual filesystem and stored artifacts
kaos-core vfs ls /artifacts/
kaos-core artifacts list --session my-session

# Show resolved settings and credential status
kaos-core config show --json
kaos-core creds list
```

**Notes**

- Every KAOS CLI follows the same conventions: `--json` for structured output,
  human-readable by default, errors to stderr. See the [CLI reference](/reference/cli).
- `kaos-core config show` reflects the full [settings resolution](/concepts/settings-resolution)
  — handy for debugging "why is this value what it is?".
- To expose the same tools to an AI client instead of the CLI, see
  [serve over MCP](/tutorials/serve-over-mcp).
