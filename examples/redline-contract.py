#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-office>=0.1.4,<0.2", "kaos-content>=0.1.3,<0.2"]
# ///
"""Redline two contract versions — and review the result in Word.

`kaos-office` compares two DOCX versions into a Word **redline** (tracked
changes); its reader surfaces those changes as *typed revisions* you can inspect
and resolve in code with `accept_all` (the final version) or `reject_all` (the
original). Fully offline, no model.

This writes three real Word files you can open and review, then prints the diff.

Run it:

    uv run examples/redline-contract.py
"""

from __future__ import annotations

from pathlib import Path

import kaos_content as kc
import kaos_office as ko
from kaos_content.revision import RevisionType, Revisions, accept_all, reject_all

ORIGINAL = "The interest rate is five percent and the term is three years."
REVISED = "The interest rate is seven percent and the term is five years."

# Write the Word files somewhere a person can actually open them.
OUT = Path.cwd() / "redline-demo"


def clause(text: str) -> kc.ContentDocument:
    b = kc.DocumentBuilder()
    b.heading(1, "Loan Agreement")
    b.paragraph(text)
    return b.build()


def body_text(doc) -> str:
    """The last non-empty line of the rendered document — the clause text."""
    lines = [ln.strip() for ln in kc.serialize_markdown(doc).splitlines() if ln.strip()]
    return lines[-1] if lines else ""


def main():
    OUT.mkdir(exist_ok=True)
    original = OUT / "original.docx"
    revised = OUT / "revised.docx"
    redline = OUT / "redline.docx"
    ko.write_docx(clause(ORIGINAL), original)
    ko.write_docx(clause(REVISED), revised)
    # Compare the two versions into a Word redline (real tracked changes).
    ko.write_redline(original, revised, redline)

    print(f"Wrote 3 Word files to {OUT}/  — open them in Word to review:")
    print("  • original.docx  — the original contract")
    print("  • revised.docx   — counsel's revised version")
    print("  • redline.docx   — the tracked-changes redline   ← open this one\n")

    print(f"  before:  {ORIGINAL}")
    print(f"  after:   {REVISED}\n")

    # Read the redline back; each edit is a typed revision.
    doc = ko.parse_docx(str(redline), track_changes=True)
    revisions = list(Revisions.from_document(doc))
    print(f"{len(revisions)} tracked change(s) in redline.docx:")
    for rv in revisions:
        verb = "inserted" if rv.change_type is RevisionType.INSERTION else "deleted"
        print(f"  {verb:>8}: {rv.text!r}")

    # Resolve the markup two ways, in code.
    accepted = body_text(accept_all(doc))
    rejected = body_text(reject_all(doc))
    print("\nResolve the markup in code:")
    print(f"  accept all -> {accepted}")
    print(f"  reject all -> {rejected}")
    return revisions, accepted, rejected


if __name__ == "__main__":
    revisions, accepted, rejected = main()
    types = {rv.change_type for rv in revisions}
    # The redline carries both insertions and deletions...
    assert RevisionType.INSERTION in types and RevisionType.DELETION in types
    # ...accepting keeps the revised numbers, rejecting restores the originals.
    assert "seven percent" in accepted and "five years" in accepted
    assert "five percent" in rejected and "three years" in rejected
