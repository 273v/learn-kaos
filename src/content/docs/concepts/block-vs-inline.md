---
title: Block vs Inline
description: The two-category structure of the KAOS document AST.
---

The [document model](/concepts/one-document-model) has exactly two kinds of node, and
keeping them straight is the key to working with it.

## Blocks and inlines

- **Block** nodes are *structural*: headings, paragraphs, lists, list items, tables,
  blockquotes, figures, code blocks, definitions. Blocks contain other blocks or inlines.
- **Inline** nodes are *content within a block*: text, bold/italic, links, footnote and
  source references, math. Inlines don't contain blocks.

You build both with the same `DocumentBuilder` — `heading`/`paragraph` add blocks,
`bold`/`link` produce inlines you pass into a paragraph (you did this in
[build a document](/tutorials/build-a-document)).

## Standoff annotations

On top of the tree, KAOS supports **standoff annotations** — labels attached to spans of
content without changing the tree itself. This is how things like entity tags, citations,
and classifications attach to exactly the right text, and why multiple overlapping
annotations can coexist over the same content.

## Why two categories

A small, closed node vocabulary is what makes the AST *uniform* across every format. A PDF
heading, a DOCX heading, and an HTML `<h1>` all become the same `Heading` block — so
`find_headings`, `document_outline`, serialization, and citation all work identically
regardless of the source. Two categories is enough to represent real legal and financial
documents while staying simple enough to write code against once.
