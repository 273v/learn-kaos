#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-nlp-transformers>=0.1.5,<0.2"]
# ///
"""Detect and redact PII with a local model — for privilege & e-discovery.

Before producing documents, you often must find and redact personal information.
`kaos-nlp-transformers` ships a local PII detector (a small ONNX model) that
flags names, emails, phone numbers, and account numbers — no LLM, no API key, so
the sensitive text never leaves the machine. Here we detect PII and redact it.

Model note: the first run downloads the ONNX model and caches it; later runs are
offline.

Run it:

    uv run examples/detect-pii.py
"""

from __future__ import annotations

import kaos_nlp_transformers as knt

TEXT = (
    "Please contact Jane Doe at jane.doe@example.com or (555) 123-4567 "
    "regarding the settlement."
)


def redact(text: str, spans) -> str:
    # Replace detected PII spans with a label, right-to-left to keep offsets valid.
    out = text
    for s in sorted(spans, key=lambda e: e.start, reverse=True):
        out = out[: s.start] + f"[{s.label}]" + out[s.end :]
    return out


def main() -> tuple[list, str]:
    detector = knt.PiiDetector.load()
    spans = detector.detect([TEXT])[0]

    print(f"original: {TEXT}\n")
    print(f"{len(spans)} PII span(s) detected:")
    for s in spans:
        print(f"  {s.label:>14}: {s.text!r}")

    redacted = redact(TEXT, spans)
    print(f"\nredacted: {redacted}")
    return spans, redacted


if __name__ == "__main__":
    spans, redacted = main()
    labels = {s.label for s in spans}
    # The name and email are reliably caught and removed.
    assert "PERSON" in labels and "EMAIL_ADDRESS" in labels
    assert "jane.doe@example.com" not in redacted
    assert "Jane Doe" not in redacted
