---
title: Serve KAOS over HTTP (with auth)
description: Expose a runtime over streamable HTTP — safely, behind a required auth token.
---

For network serving (rather than a stdio subprocess), `kaos-mcp` and the package `*-serve`
commands offer **streamable HTTP**. It is **auth-required by default** — KAOS refuses to
expose tools over an open network endpoint.

:::caution[Operator configuration]
This runs a network server, so it isn't exercised in this site's offline CI. The setup is
documented below.
:::

## Run it

```bash
# An explicit token is required — the server won't start without acknowledging it
export KAOS_MCP_HTTP_TOKEN="$(openssl rand -hex 32)"
kaos-agents-serve --http --port 8000
```

Clients then connect with the token as a bearer credential.

## Notes

- The required token is an **operator acknowledgement**, not a substitute for real
  authentication. In production, put the server behind a reverse proxy that does proper
  auth/TLS — the token guards against *accidentally* exposing tools, not against a determined
  attacker. See [session enforcement](/concepts/session-enforcement).
- Identity on each request scopes session memory and the VFS, so multiple callers stay
  isolated.
- For desktop AI clients, prefer stdio ([connect an AI tool](/how-to/connect-an-ai-tool)) —
  it's simpler and needs no network exposure.
