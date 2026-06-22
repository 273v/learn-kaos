---
title: Provenance & the producer contract
description: Why every KAOS extractor emits the same document shape, with where-it-came-from attached.
---

KAOS's ingestion packages — `kaos-pdf`, `kaos-office`, `kaos-web`, `kaos-tabular`,
`kaos-source` — share one contract: they are **producers** of the
[document model](/concepts/one-document-model). Each turns its format into a
`ContentDocument` (or `TabularDocument`) carrying **provenance**.

## Provenance: where each piece came from

Extracted nodes record their origin — page number, bounding box, confidence, source URI.
So when an answer later cites a fact, the citation can point not just at a document but at
the exact place in it (a [block ref](/tutorials/build-a-document)) — and that citation can
be [verified](/concepts/the-refusal-contract).

## The producer contract

Because every extractor emits the *same* shape, downstream code is written once. Search,
chunking, dedup, LLM programs, agents, and citation verification don't branch on "was this
a PDF or a web page" — they operate on the AST. Adding a new format means writing a new
*producer*; nothing downstream changes.

## Why it's foundational

Provenance + a uniform shape is what makes KAOS trustworthy for legal and financial work:
you can always trace an output back to its source, byte for byte, regardless of what format
that source arrived in.
