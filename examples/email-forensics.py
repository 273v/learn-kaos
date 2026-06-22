#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-source>=0.1.3,<0.2"]
# ///
"""Parse an email into structured fields — the basis of e-discovery.

`kaos-source` parses `.eml` / `.mbox` / vCard / PACER and other formats into
typed records. Here we parse a raw email into sender, recipients, subject, body,
and header forensics — the structured shape an e-discovery or investigation
pipeline indexes. Operating on raw bytes, so it's fully offline.

Run it:

    uv run examples/email-forensics.py
"""

from __future__ import annotations

from kaos_source.parsers import EmlParser

RAW_EML = b"""\
From: counsel@example.com
To: client@example.com
Cc: paralegal@example.com
Subject: Re: Merger Agreement
Date: Tue, 1 Apr 2026 10:00:00 -0400

The deal terms are confidential. Please review the indemnification clause
before our call.
"""


def main() -> dict:
    parsed = EmlParser().parse(RAW_EML)

    record = {
        "from": parsed.from_address.address,
        "to": [a.address for a in parsed.to_addresses],
        "cc": [a.address for a in parsed.cc_addresses],
        "subject": parsed.subject,
        "body": parsed.body_text.strip(),
    }
    print(f"  from:    {record['from']}")
    print(f"  to:      {record['to']}")
    print(f"  cc:      {record['cc']}")
    print(f"  subject: {record['subject']}")
    print(f"  body:    {record['body'][:60]}...")
    print(f"  header forensics: {type(parsed.forensics).__name__}")
    return record


if __name__ == "__main__":
    record = main()
    assert record["from"] == "counsel@example.com"
    assert record["to"] == ["client@example.com"]
    assert record["cc"] == ["paralegal@example.com"]
    assert record["subject"] == "Re: Merger Agreement"
    assert "indemnification clause" in record["body"]
