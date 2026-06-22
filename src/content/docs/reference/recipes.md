---
title: Agent recipes
description: The built-in workflow recipes and schema-bundled extraction recipes kaos-agents ships.
---

`kaos-agents` ships reusable **recipes** — playbooks loaded into an agent's planning
context. Two families:

## Workflow recipes

Auto-loaded planning playbooks for common tasks:

| Recipe | What it does |
|---|---|
| `contract-extraction` | Extract key terms with `Cited[T]` provenance |
| `corpus-qa` | RAG-backed document Q&A with grounded citations |
| `federal-register-research` | Federal Register + eCFR regulatory research |
| `edgar-research` | SEC filing analysis with EDGAR tools |
| `summarization` | Configurable-style document summarization |

API: `load_builtin_recipes()`, `load_recipe(name)`, `recipe_names()`.

## Extraction recipes

Schema-bundled recipes for structured document extraction, each with a published recall
floor as the competitive baseline. Used via `kaos-extract --recipe <name>` or the
`kaos-extract-schema` MCP tool:

| Recipe | Columns | Recall floor |
|---|---|---|
| `merger-agreement` | 27 | 99.66% |
| `spa-deal-points` | 32 | 98.13% |
| `lease` | 24 | 97.20% |
| `lpa` | 27 | 99.14% |
| `court-opinion` | 16 | 96.49% |

Each carries an `ExtractionSchema`, notes, and named golden eval sets. API:
`load_extraction_recipes()`, `load_extraction_recipe(name)`, `extraction_recipe_names()`.

:::note
Running these against real documents calls an LLM (needs a key). The offline path on this
site teaches the underlying primitives — [typed calls](/tutorials/oneliner-to-call-to-program)
and [grounded citations](/tutorials/grounded-citations) — that recipes compose.
:::
