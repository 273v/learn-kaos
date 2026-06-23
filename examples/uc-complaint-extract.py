#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-llm-core>=0.1.12,<0.2", "kaos-llm-client>=0.1.9,<0.2"]
# ///
"""Use case — Complaint / settlement database.

Build a searchable database from regulatory complaints and settlements by
extracting the structured fields that matter: the parties, the violation, and
the amount. A typed `Call` returns a validated record. Offline via FunctionClient.

Real-data note: run this over real complaints/settlements from the public
**kl3m** datasets on Hugging Face instead of the inline sample.

Run it:

    uv run examples/uc-complaint-extract.py
"""

from __future__ import annotations

import asyncio
import json

from kaos_llm_client.providers.function import FunctionClient
from kaos_llm_client.types import ContentPart, ProviderResponse
from kaos_llm_core import Call, InputField, OutputField, Signature

COMPLAINT = (
    "In the matter of Globex Financial, the Commission alleges failure to supervise "
    "in violation of Section 15(b). Globex agreed to pay a civil penalty of $2,500,000 "
    "to settle the charges."
)


class ComplaintRecord(Signature):
    """Extract the key fields from a regulatory complaint or settlement."""

    text: str = InputField(description="the complaint or settlement text")
    respondent: str = OutputField(description="the party charged")
    violation: str = OutputField(description="the alleged violation, briefly")
    penalty_usd: int = OutputField(description="the monetary penalty in US dollars")


def fake_model(messages, profile):
    # A real model reads the text; we return the structured record we want.
    record = {
        "respondent": "Globex Financial",
        "violation": "failure to supervise (Section 15(b))",
        "penalty_usd": 2_500_000,
    }
    return ProviderResponse(
        provider="function", model="function-test", raw={},
        parts=[ContentPart(type="text", text=json.dumps(record))],
    )


async def main():
    call = Call(ComplaintRecord, model="function-test", client=FunctionClient(function=fake_model))
    rec = await call(text=COMPLAINT)
    print(f"  respondent:  {rec.respondent}")
    print(f"  violation:   {rec.violation}")
    print(f"  penalty:     ${rec.penalty_usd:,}")
    return rec


if __name__ == "__main__":
    rec = asyncio.run(main())
    assert rec.respondent == "Globex Financial"
    assert rec.penalty_usd == 2_500_000
