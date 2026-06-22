#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-web>=0.1.13,<0.2", "kaos-content>=0.1.6,<0.2"]
# ///
"""Extract clean content from HTML into the document AST.

`kaos-web` turns a web page into a `ContentDocument`, applying readability-style
content extraction (stripping nav, ads, boilerplate). Here we run it on an inline
HTML string so the example is fully offline — with a live page, you'd fetch it
first (`kaos-web fetch <url>`), then extract.

Run it:

    uv run examples/web-extract.py
"""

from __future__ import annotations

import kaos_content as kc
from kaos_web import html_to_document

HTML = """\
<html><body>
  <nav>Home | Products | Contact</nav>
  <article>
    <h1>Acme Terms of Service</h1>
    <p>Users must accept the binding <strong>arbitration clause</strong>.</p>
    <h2>Limitation of Liability</h2>
    <p>Acme is not liable for indirect damages.</p>
  </article>
  <footer>&copy; 2026 Acme Corp</footer>
</body></html>
"""


def main() -> str:
    doc = html_to_document(HTML, url="https://example.com/tos")
    markdown = kc.serialize_markdown(doc)
    print("--- extracted content ---")
    print(markdown)
    return markdown


if __name__ == "__main__":
    markdown = main()
    # The article content is extracted into the AST...
    assert "Acme Terms of Service" in markdown
    assert "arbitration clause" in markdown
    assert "Limitation of Liability" in markdown
