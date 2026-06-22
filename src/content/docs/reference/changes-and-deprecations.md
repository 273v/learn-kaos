---
title: Changes & deprecations
description: APIs that have moved or are on their way out across the kaos-* packages.
---

The packages are pre-1.0 and evolving. This page tracks the deprecations and renames worth
knowing. Each package's own `CHANGELOG.md` is the authoritative, detailed record.

## Deprecated APIs

- **`extract_pdf` / `extract_pdf_bytes`** (kaos-pdf) — deprecated aliases; use the current
  `parse_pdf` entry point, which returns a `ContentDocument`.
- **`EmbeddingRetriever`** (kaos-nlp-transformers) — deprecated as of 0.2.0 (emits a
  `DeprecationWarning`), scheduled for removal in 0.3.0. Migrate to
  `kaos_content.indexing.SearchableDocument` / `SearchableCorpus`.
- **Adaptive retrieval** (kaos-agents) — the adaptive-retrieval pipeline is deprecated; it
  scored worse than plain BM25 cross-domain (see [why plain BM25](/concepts/why-plain-bm25)).
  It remains importable but is not the default path; use plain BM25.
- **`torch` extra** (kaos-nlp-transformers) — a deprecated no-op alias scheduled for
  removal in 0.3.0. The Rust `ort` cdylib is the canonical inference backend.

## Early-stage / not-yet-implemented

- **kaos-ml-core** is at v0: its CLI and `serve` entry points are stubs and the Rust crate
  exposes only a version probe. Use its Python API and MCP tools as the real surface (see
  [compatibility](/reference/compatibility)).

## Conventions that are stable

These are public contracts you can rely on across versions: each package's `__all__`,
documented CLI flags and `--json` output, MCP tool names and schemas, environment
variables (the `KAOS_*` / `KAOS_<MOD>_*` prefixes), and serialized model/trace shapes.
Changes to these are versioned, tested, and noted in the relevant `CHANGELOG.md`.
