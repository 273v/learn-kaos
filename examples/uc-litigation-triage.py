#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-llm-core>=0.1.12,<0.2", "kaos-llm-client>=0.1.9,<0.2"]
# ///
"""Use case — Litigation document triage.

Ingesting a stack of court documents? Classify each by type so they route to the
right workflow. Here a typed `Call` classifies documents into a fixed set of
litigation types. Offline via FunctionClient; with a real model it generalizes.

Real-data note: point this at real filings from the public **kl3m** datasets on
Hugging Face (e.g. court documents) instead of the inline samples.

Run it:

    uv run examples/uc-litigation-triage.py
"""

from __future__ import annotations

import asyncio
import json
from typing import Literal

from kaos_llm_client.providers.function import FunctionClient
from kaos_llm_client.types import ContentPart, ProviderResponse
from kaos_llm_core import Call, InputField, OutputField, Signature

DOCS = [
    "Plaintiff Acme Corp alleges breach of contract and seeks compensatory damages.",
    "Defendant respectfully moves the Court to dismiss the complaint under Rule 12(b)(6).",
    "This Mutual Non-Disclosure Agreement is entered into by the parties as of the date below.",
]


class TriageDoc(Signature):
    """Classify a legal document by its type."""

    text: str = InputField(description="document text")
    doc_type: Literal["complaint", "motion", "contract", "correspondence"] = OutputField(
        description="the document type"
    )


def fake_model(messages, profile):
    low = " ".join(m.get("content", "") for m in messages if m.get("role") == "user").lower()
    if "alleges" in low or "plaintiff" in low:
        t = "complaint"
    elif "moves the court" in low or "motion" in low:
        t = "motion"
    elif "agreement" in low:
        t = "contract"
    else:
        t = "correspondence"
    return ProviderResponse(
        provider="function", model="function-test", raw={},
        parts=[ContentPart(type="text", text=json.dumps({"doc_type": t}))],
    )


async def main() -> list[str]:
    call = Call(TriageDoc, model="function-test", client=FunctionClient(function=fake_model))
    types = []
    for doc in DOCS:
        result = await call(text=doc)
        types.append(result.doc_type)
        print(f"  [{result.doc_type:<14}] {doc[:54]}...")
    return types


if __name__ == "__main__":
    types = asyncio.run(main())
    assert types == ["complaint", "motion", "contract"]
