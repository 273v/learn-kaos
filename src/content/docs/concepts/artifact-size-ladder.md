---
title: The artifact size ladder
description: How KAOS decides when data lives inline vs. as a stored artifact.
---

Tool results and documents range from a few bytes to hundreds of megabytes. KAOS handles
this with a **size ladder**: small data travels inline; large data is stored as an
artifact and referenced by a URI. This keeps the context window and message payloads
small without losing access to big results.

## The tiers

- **Inline (small)** — results under a small threshold (on the order of ~16KB) are returned
  directly in the `ToolResult`. Fast, no indirection.
- **Summary + resource (medium)** — larger results (up to a higher threshold, ~256KB) come
  back as a short summary plus a link to the full content.
- **Artifact (large)** — big outputs are written to the artifact store and referenced by a
  `kaos://` URI. The consumer fetches it on demand instead of carrying it around.

## Why a ladder

- **The context window is precious.** Dumping a 200KB extraction into an agent's prompt
  wastes budget and may not even fit. A reference costs a handful of tokens.
- **Provenance stays intact.** An artifact URI is addressable and durable, so a later step
  (or a citation) can point back at exactly the produced output.
- **It's automatic.** Tools don't each reinvent "is this too big?" — the runtime applies
  the ladder uniformly, so behavior is predictable across every tool.

This is the storage counterpart to [memory as context assembly](/concepts/memory-as-context-assembly):
both are about spending a limited context window on the right things.
