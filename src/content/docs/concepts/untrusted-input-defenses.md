---
title: Defenses for untrusted input
description: The bounds KAOS puts on documents, archives, URLs, and SQL so hostile input can't run away with your process.
---

Ingestion packages handle input you don't control — a PDF from opposing counsel, an
archive from a data room, a URL from a filing. KAOS treats all of it as **untrusted** and
bounds it, so a malicious or malformed input degrades gracefully instead of exhausting
memory, escaping a sandbox, or reaching internal services.

## The defenses, by surface

- **PDFs** (`kaos-pdf`): PDFium runs under a global lock for thread-safety; extraction is
  bounded and offloaded so one document can't block the event loop.
- **Office / archives** (`kaos-office`, `kaos-source`): OPC and zip parsing caps decompressed
  size and entry counts — **zip-bomb** protection — and rejects path-traversal members.
- **Sources & URLs** (`kaos-source`, `kaos-web`): URL fetching is guarded against **SSRF**
  (no reaching internal hosts), honors robots, redacts secrets, and caps response size;
  archive extraction is rooted so members can't write outside the target.
- **SQL** (`kaos-tabular`): DuckDB runs over registered files with a row cap; the
  filesystem-access surface is treated as a trust boundary.

## Why bound everything

Size, recursion, time, token, row, page, and path limits aren't paranoia — they're the
difference between "this input failed cleanly" and "this input took down the service." For
legal/financial work especially, you must be able to safely open a document you have every
reason to distrust. KAOS makes those limits the default, not an opt-in.
