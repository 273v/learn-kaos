---
title: Environment variables
description: How KAOS resolves settings, the per-package prefixes, and the variables you'll actually set.
---

Every package configures itself through a typed `ModuleSettings` subclass. You rarely need
to set much — defaults are sensible — but here's how it works and the variables that matter.

## How settings resolve

`ModuleSettings` resolves each field through a fixed precedence (highest first):

1. explicit keyword overrides in code
2. values on the `KaosContext`
3. `KAOS_<MOD>_*` environment variables
4. documented legacy-alias env vars
5. a `.env` file
6. the field's default

Secrets (API keys) are held in `pydantic.SecretStr` and **redacted** from logs, errors,
CLI/JSON output, and serialized settings.

## Per-package prefixes

| Package | Env prefix | Notable variables |
|---|---|---|
| kaos-core | `KAOS_` | storage/VFS, credential-store tier |
| kaos-llm-client | `KAOS_LLM_` | provider keys (below); `KAOS_LLM_ALLOW_INSECURE_BASE_URL` (local models) |
| kaos-llm-core | `KAOS_LLM_CORE_` | default model, optimizer/budget defaults |
| kaos-agents | `KAOS_AGENT_` | `KAOS_AGENT_DEFAULT_LLM_MODEL`, `KAOS_AGENT_MAX_COST_USD`, context budget, retrieval threshold, max iterations, `KAOS_AGENT_OCR_VLM_ESCALATION` (send garbled scanned pages to a vision model — off by default) |
| kaos-mcp | `KAOS_MCP_` | transport/host/port; HTTP auth token |
| kaos-source | `KAOS_SOURCE_` | connector timeouts, `*_USER_AGENT` (EDGAR needs an email), GovInfo API key |
| kaos-web | `KAOS_WEB_` | `KAOS_WEB_SERPAPI_API_KEY` / `EXA` / `BRAVE` (optional search); `KAOS_WEB_HTTP_TOKEN` |
| kaos-nlp-transformers | `KAOS_NLP_TRANSFORMERS_` | `..._OFFLINE`, `..._CACHE_DIR`, `..._EMBEDDING_CACHE_DIR`, HTTP token |
| kaos-tabular / kaos-pdf / kaos-office / kaos-graph / kaos-nlp-core / kaos-ml-core / kaos-citations / kaos-names / kaos-ui | `KAOS_<MOD>_` | per-module knobs; mostly defaults |

`kaos-content` ships **no** environment variables — its safety knobs are call-site
arguments (`allow_raw_html`, size caps).

## LLM provider keys

For *live* LLM calls (the offline `FunctionClient` path needs none):

```bash
export ANTHROPIC_API_KEY=sk-...     # documented default (Haiku)
export OPENAI_API_KEY=sk-...
export GOOGLE_API_KEY=...
```

The `KAOS_LLM_*` equivalents (e.g. `KAOS_LLM_ANTHROPIC_API_KEY`) take precedence when set.
See [compatibility](/reference/compatibility) for provider caveats.

## Finding a package's variables

The authoritative list for any package is its `ModuleSettings` subclass and `--help`:

```bash
uv run --with kaos-agents kaos-agent --help
```
