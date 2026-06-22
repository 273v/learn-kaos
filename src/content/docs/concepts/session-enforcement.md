---
title: Session enforcement
description: How KAOS keeps sessions and tenants isolated, and why HTTP serving must authenticate.
---

When a runtime is served to multiple callers — over MCP HTTP, or inside a multi-tenant app
— isolation isn't optional. KAOS enforces it at the boundary.

## Identity on every request

Calls carry an identity (`client_id` / `request_id`). The runtime scopes session memory,
the virtual filesystem, and artifacts to that identity, so one caller can't read another's
data. The single-user-chat reference app, for example, namespaces each session's files and
injects the right `client_id` per request.

## Uniform "not found"

Asked for a resource that doesn't exist *or* that the caller isn't allowed to see, the
runtime returns the **same** not-found response. It never reveals "this exists but isn't
yours" — which would leak the existence of other tenants' data.

## HTTP must authenticate

The MCP HTTP transport (`kaos-mcp --http`, `kaos-*-serve --http`) **requires an explicit
auth token** and refuses to run open by default. Exposing tools — some of which touch
files, networks, or credentials — to an unauthenticated network endpoint is exactly the
mistake the default guards against. (The token is an operator acknowledgement, not a
substitute for real reverse-proxy auth in production.)

## Why it's structural

Isolation and auth live in the runtime and the bridge, not in each tool. So every tool a
runtime exposes inherits the same boundary — you can't forget to add it to a new tool.
