---
title: Glossary
description: The cross-package vocabulary of KAOS, in one place — each term linked to where it's explained or used.
---

The terms you'll meet across the KAOS packages and these docs. Each entry links to the
concept that explains it or the example that uses it. New here? Start with
[what is KAOS?](/what-is-kaos) and the [architecture](/architecture).

## Runtime & tools

- **KaosRuntime** — the dependency-injection container holding tools, a virtual filesystem,
  artifacts, and settings; agents and MCP servers run on it. `KaosRuntime.test_mode()` gives
  an in-memory, isolated one. [→ why DI over globals](/concepts/why-di-over-globals)
- **KaosTool / `@kaos_tool`** — a typed, MCP-native unit of work; the runtime derives its
  input schema from your type hints. [→ your first tool](/tutorials/first-tool)
- **ToolResult** — the typed return of a tool: `.text`, structured content, or a resource
  link, sized by the [artifact ladder](/concepts/artifact-size-ladder).
- **VFS (virtual filesystem)** — KAOS's storage abstraction; sessions and artifacts live
  here. The disk-backed default is a test [footgun](/concepts/why-di-over-globals) — use
  `test_mode()`. [→ inspect a runtime](/how-to/inspect-a-runtime)
- **Artifact** — a stored, addressable blob referenced by a `kaos://` URI; how large results
  travel. [→ the artifact size ladder](/concepts/artifact-size-ladder)
- **Settings resolution** — the layered precedence (defaults → file → env → call) that
  decides a config value. [→ typed settings](/how-to/add-typed-settings)

## Document model

- **ContentDocument** — the Block/Inline AST every extractor produces; the "write once, run
  on everything" bet. [→ one document model](/concepts/one-document-model)
- **Block / Inline** — structural nodes (heading, paragraph, table) vs. content within them
  (text, bold, link, citation). [→ build a document](/tutorials/build-a-document)
- **Provenance** — where a node came from (page, bounding box, confidence), preserved through
  extraction. [→ ingest a PDF](/how-to/ingest-a-pdf)
- **block ref** — a stable address into a document (e.g. `#/body/2`); what a citation points
  at. [→ grounded citations](/tutorials/grounded-citations)
- **DocumentView** — a queryable view over a `ContentDocument` (sentences, paragraphs,
  entities). [→ find money & dates](/how-to/find-financial-terms)
- **Chunk** — a retrieval-sized slice of a document with a char-span back to the source.
  [→ chunk a document](/how-to/chunk-a-document)
- **Revision** — a tracked change (insertion/deletion) surfaced from a DOCX redline; resolve
  with `accept_all`/`reject_all`. [→ redline a contract](/how-to/redline-a-contract)

## LLM programming

- **kaos-llm-client** — the transport layer: one interface over every provider.
  [→ transport vs. programming](/concepts/transport-vs-programming)
- **FunctionClient** — a client that runs a Python callable instead of an HTTP request; the
  deterministic [offline seam](/concepts/the-offline-seam) that makes this whole site
  testable. [→ offline LLM](/tutorials/offline-llm-with-functionclient)
- **ModelProfile** — typed capability metadata for a model (preferred over
  `if provider == ...`). [→ provider failover](/how-to/provider-failover)
- **Signature** — a typed input/output contract for an LLM task.
  [→ typed LLM programming](/concepts/typed-llm-programming)
- **Call** — a Signature compiled into a function returning a validated, typed object.
  [→ one-liner to program](/tutorials/oneliner-to-call-to-program)
- **Program** — a composition of Calls (extract → classify → summarize).
- **Codec** — the JSON↔typed-object layer that validates and retries model output against a
  Signature.
- **Optimizer** — improves a Program against a metric, keeping a change only if it helps
  (`BootstrapOptimizer`, `MIPRO`). [→ optimize a program](/how-to/optimize-a-program)
- **Budget** — a cost/token/trial/time ceiling enforced *before* spend; returns a
  `StopReason`. [→ cap LLM cost](/how-to/cap-llm-cost) · [cost as a contract](/concepts/cost-as-a-contract)
- **Cited[T] / Span** — a typed value with verifiable supporting spans; `Span.verify` checks
  a quote against its source. [→ grounding & verification](/concepts/grounding-and-verification)
- **GroundedAnswer** — the answer-or-refuse result of corpus QA: an `Answer` with claims and
  spans, or `InsufficientEvidence`. [→ the refusal contract](/concepts/the-refusal-contract)

## Agents

- **Agent** — frozen agent *config* (instructions, model, pattern, tools); stateless and
  reconstructable. [→ agent vs. runner](/concepts/agent-vs-runner)
- **Runner** — the *engine* that drives an Agent over a runtime for one turn.
- **Turn loop** — the 8-step structured loop a turn runs through.
  [→ the turn loop](/concepts/the-8-step-turn-loop)
- **Pattern** — how a turn executes: chat, research, plan-execute, findings, router.
  [→ choose a pattern](/how-to/choose-a-pattern)
- **ResearchAgent** — retrieve → answer-with-verified-citation → refuse over a corpus.
  [→ a research agent](/tutorials/research-agent-citations)
- **FindingsAgent** — recall-first enumerate → filter → synthesize, under a cost cap.
  [→ review a contract](/how-to/review-a-contract)
- **ReAct** — the inner reason-act-observe tool loop (the agent is the outer loop).
- **Delegation / handoff** — running a sub-agent as a tool, or transferring a turn to another
  agent. [→ delegate to a sub-agent](/how-to/delegate-and-handoff)
- **RunState** — a serializable paused-turn snapshot for approval/resume.
  [→ pause & resume](/how-to/pause-and-resume)
- **SessionMemory** — budgeted, sectioned context assembled per turn.
  [→ memory as context assembly](/concepts/memory-as-context-assembly)
- **Hook** — an observer of the event stream (logging, cost, OTel, circuit breaker).
  [→ trace with OpenTelemetry](/how-to/export-otel)
- **PermissionPolicy** — rules gating tool calls (read-only auto-allowed, destructive asked).
  [→ configure permissions](/how-to/configure-permissions)
- **Span / value event** — phase boundaries vs. facts in the typed event stream.
  [→ events & spans](/concepts/events-and-spans)

## Deterministic substrate

- **BM25** — the lexical full-text ranking used for retrieval; fast, offline, explainable.
  [→ why plain BM25](/concepts/why-plain-bm25) · [search with BM25](/how-to/search-text-with-bm25)
- **Embedding** — a dense vector for semantic similarity; KAOS ships a vendored static model
  for offline use. [→ semantic embeddings](/how-to/semantic-embeddings)
- **MinHash / near-duplicate** — shingle-hash similarity for finding near-duplicate text.
  [→ find near-duplicates](/how-to/find-near-duplicates)
- **NER (named-entity recognition)** — zero-shot local entity extraction (person, org, money,
  date). [→ extract entities](/how-to/extract-entities)
- **PII detection** — local detection/redaction of personal data for privilege/e-discovery.
  [→ detect & redact PII](/how-to/detect-and-redact-pii)
- **FstSet** — a finite-state index for fuzzy and prefix string matching (conflict checks,
  type-ahead). [→ conflict checking](/how-to/check-for-conflicts)
- **Citation parsing** — recognizing Bluebook cases/CFR/statutes as typed records.
  [→ parse legal citations](/how-to/parse-legal-citations)
- **Knowledge graph / SPARQL** — RDF facts about a session, queryable.
  [→ query the session graph](/how-to/query-the-session-graph)

## Protocol & serving

- **MCP (Model Context Protocol)** — the standard KAOS exposes tools over; `kaos-mcp` bridges
  any runtime to it. [→ the MCP bridge](/concepts/the-mcp-bridge)
- **`kaos-*-serve`** — each package's MCP server entry point.
  [→ serve over MCP](/tutorials/serve-over-mcp) · [connect an AI tool](/how-to/connect-an-ai-tool)

## Data & testing

- **Synthetic data** — generated, reproducible test data (per-row hashed seeds).
  [→ generate synthetic data](/how-to/generate-synthetic-data)
- **kl3m datasets** — the large, openly-licensed legal/financial corpus you point real runs
  at. [→ use real data from kl3m](/how-to/use-kl3m-data)
- **UTBMS / LEDES** — legal billing task codes and the billing data format used in the
  [billing analytics](/how-to/analyze-billing) examples.
