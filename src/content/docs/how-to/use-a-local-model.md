---
title: Use a local model
description: Point KAOS at a self-hosted Ollama or vLLM endpoint.
---

You can run KAOS against a local, self-hosted model server (Ollama, vLLM, LM Studio) instead
of a cloud provider — useful for privacy, cost, or offline operation.

:::caution[Needs a running local server]
This requires a model server running on your machine, so it can't be exercised in this
site's CI. The configuration is documented below.
:::

## Configure the endpoint

Point the client at your local OpenAI-compatible endpoint. Because it's not HTTPS to a known
provider, you must explicitly acknowledge the insecure base URL:

```bash
export KAOS_LLM_ALLOW_INSECURE_BASE_URL=1     # required for http://localhost endpoints
export OPENAI_BASE_URL=http://localhost:11434/v1   # e.g. Ollama
```

```python
from kaos_llm_client import create_client

client = create_client("openai:llama3.1")   # served by your local endpoint
print(client.chat([{"role": "user", "content": "Hi"}]).text)
```

## Notes

- The `KAOS_LLM_ALLOW_INSECURE_BASE_URL` gate is an SSRF safeguard: KAOS refuses non-HTTPS /
  non-provider base URLs by default so a misconfiguration can't quietly send prompts
  somewhere unexpected. You opt in deliberately.
- Everything downstream — [typed programs](/tutorials/oneliner-to-call-to-program),
  [agents](/tutorials/first-agent) — works identically; only the client changes (the same
  reason the [FunctionClient seam](/concepts/the-offline-seam) works).
- For fully-offline *deterministic* runs (tests, demos), prefer `FunctionClient` over a local
  model — it needs no server at all.
