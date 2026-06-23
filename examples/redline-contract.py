#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-office>=0.1.4,<0.2", "kaos-content>=0.1.3,<0.2"]
# ///
"""Redline two contract versions and work with the tracked changes.

`kaos-office` compares two DOCX versions into a Word **redline** (tracked
changes), and its reader surfaces those changes as *typed revisions* you can
inspect and resolve in code: list every insertion and deletion with its author,
then `accept_all` (the final version) or `reject_all` (the original). This is the
contract-redlining workflow — fully offline, no model.

Run it:

    uv run examples/redline-contract.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import kaos_content as kc
import kaos_office as ko
from kaos_content.revision import RevisionType, Revisions, accept_all, reject_all


def clause(text: str) -> kc.ContentDocument:
    b = kc.DocumentBuilder()
    b.heading(1, "Loan Agreement")
    b.paragraph(text)
    return b.build()


def main():
    d = Path(tempfile.mkdtemp())
    original, revised, redline = d / "v1.docx", d / "v2.docx", d / "redline.docx"

    # Two versions of a clause — counsel changed the rate and the term.
    ko.write_docx(clause("The interest rate is five percent and the term is three years."), original)
    ko.write_docx(clause("The interest rate is seven percent and the term is five years."), revised)

    # Compare into a Word redline (tracked changes).
    ko.write_redline(original, revised, redline)

    # The reader surfaces the tracked changes as typed revisions.
    doc = ko.parse_docx(str(redline), track_changes=True)
    revisions = list(Revisions.from_document(doc))

    print(f"{len(revisions)} tracked change(s):\n")
    for rv in revisions:
        verb = "inserted" if rv.change_type is RevisionType.INSERTION else "deleted"
        print(f"  {verb:>8}: {rv.text!r}  (by {rv.author})")

    # Resolve the markup two ways (the body is the last non-empty line).
    def body(d) -> str:
        lines = [ln.strip() for ln in kc.serialize_markdown(d).splitlines() if ln.strip()]
        return lines[-1] if lines else ""

    accepted = body(accept_all(doc))
    rejected = body(reject_all(doc))
    print(f"\n  accept all -> {accepted}")
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
