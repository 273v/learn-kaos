---
title: Pull a SEC filing
description: Fetch and parse EDGAR filings with kaos-source.
---

`kaos-source` ships REST connectors for government data — including **SEC EDGAR**. Fetch a
filing, then parse it into the [document AST](/concepts/one-document-model) like any other
source.

:::caution[Needs network access]
EDGAR is a live API, so the fetch step can't run in this site's offline CI. The *parsing*
step is offline (it's the same as [extracting a web page](/how-to/web-page-to-ast)). The
commands below are documented.
:::

## Fetch and parse

```bash
# Discover and materialize an EDGAR filing (EDGAR requires a User-Agent with an email)
export KAOS_SOURCE_EDGAR_USER_AGENT="Your Name your.email@example.com"
kaos-source materialize "edgar://<cik>/<accession>" --name acme-10k
kaos-source preview acme-10k --max-bytes 4096
```

In Python, the EDGAR connector fetches the filing, which you then parse:

```python
# (fetch via the EDGAR connector — network) then parse the HTML offline:
from kaos_web import html_to_document
doc = html_to_document(filing_html, url="https://www.sec.gov/...")
```

## Notes

- Connector requirements vary: **EDGAR** needs a `User-Agent` containing an email;
  **GovInfo** needs an API key; **Federal Register** and **eCFR** need neither (see
  [environment variables](/reference/env-vars)).
- Once parsed, everything downstream is offline and identical to any other document:
  [search](/how-to/search-text-with-bm25), [extract citations](/how-to/extract-citations),
  [SQL over extracted tables](/how-to/run-sql-analytics), or a
  [research agent](/tutorials/research-agent-citations) over a filing corpus.
- `kaos-source` also handles filesystem, archives, browser capture, GLEIF, and PACER.
