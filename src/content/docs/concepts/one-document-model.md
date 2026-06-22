---
title: One document model
description: Why every KAOS extractor produces the same AST — and what that buys you.
---

A legal/financial workflow ingests wildly different inputs: PDFs, Word documents, web
pages, spreadsheets, email. The naive approach writes separate code for each format —
separate parsing, separate search, separate citation logic. It doesn't scale, and it
makes provenance (knowing *where* a fact came from) nearly impossible.

KAOS makes a different bet: **every extractor produces the same document model.**

## The Block/Inline AST

`kaos-content` defines a single AST. **Block** nodes are structural (headings,
paragraphs, lists, tables, figures); **Inline** nodes are content within a block (text,
bold, links, citations). Every node carries:

- **Provenance** — where it came from (page, bounding box, confidence) when extracted.
- **A stable block reference** (like `#/body/2`) — a precise, addressable location.

You saw this in [build a document](/tutorials/build-a-document): a `ContentDocument`
serializes to Markdown, HTML, text, or JSON, and exposes an outline with each block's
`ref`.

## What it buys you

- **Write once, run on everything.** Search, chunking, dedup, LLM programs, and agents
  operate on the AST — so they work identically whether the source was a PDF or a web
  page. `kaos-pdf`, `kaos-office`, `kaos-web`, and `kaos-tabular` are all just *producers*
  of this one shape.
- **Citations that point at something real.** Because every block has a stable
  reference, an answer can cite `#/body/2` of a specific document — and that citation can
  be **verified** by checking the quoted text against the source span. This is the
  foundation of KAOS's grounded findings.
- **Format is a choice, not a constraint.** The AST is the source of truth; Markdown,
  HTML, CSV, and JSON are serializations you pick at the end.

## The mental model

```
real files / sources                          one AST                output
─────────────────────                     ─────────────────       ────────────
PDF, DOCX, PPTX, XLSX,   ──extractors──>   ContentDocument   ──>   search / LLM /
HTML, CSV, archives...                     (Block + Inline +        agents / citations
                                            provenance + refs)      / Markdown / JSON
```

Learn the model once and the rest of the stack stops caring what format your input was.
