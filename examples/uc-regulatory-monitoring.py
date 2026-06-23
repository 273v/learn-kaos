#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-llm-core>=0.1.12,<0.2", "kaos-llm-client>=0.1.9,<0.2"]
# ///
"""Use case — Federal Register regulatory monitoring.

Watch a feed of regulatory notices, keep only the ones relevant to your business,
and summarize them for a stakeholder memo. A typed `Call` filters each notice and
summarizes the relevant ones. Offline via FunctionClient.

Real-data note: pull the live feed with `kaos-source` (Federal Register connector,
network) or from the public **kl3m** datasets on Hugging Face; the filter +
summarize shown here is offline.

Run it:

    uv run examples/uc-regulatory-monitoring.py
"""

from __future__ import annotations

import asyncio
import json

from kaos_llm_client.providers.function import FunctionClient
from kaos_llm_client.types import ContentPart, ProviderResponse
from kaos_llm_core import Call, InputField, OutputField, Signature

# Today's notices (a real run pulls these from the Federal Register).
NOTICES = [
    "CFPB proposes a rule on overdraft fees for consumer deposit accounts.",
    "EPA announces revised emissions standards for heavy-duty trucks.",
    "OCC issues guidance on small-dollar consumer lending practices.",
]

INTEREST = "consumer financial products and lending"


class TriageNotice(Signature):
    """Decide if a regulatory notice is relevant to the area of interest, and summarize it."""

    interest: str = InputField(description="the area of interest")
    notice: str = InputField(description="the regulatory notice text")
    relevant: bool = OutputField(description="whether it is relevant to the interest")
    summary: str = OutputField(description="a one-line summary for a stakeholder memo")


def fake_model(messages, profile):
    low = " ".join(m.get("content", "") for m in messages if m.get("role") == "user").lower()
    is_consumer_finance = any(
        k in low for k in ("overdraft", "consumer deposit", "consumer lending", "small-dollar")
    )
    payload = {
        "relevant": is_consumer_finance,
        "summary": "Affects consumer financial products — review for compliance impact."
        if is_consumer_finance
        else "Not relevant to consumer finance.",
    }
    return ProviderResponse(
        provider="function", model="function-test", raw={},
        parts=[ContentPart(type="text", text=json.dumps(payload))],
    )


async def main() -> list[str]:
    call = Call(TriageNotice, model="function-test", client=FunctionClient(function=fake_model))
    relevant = []
    print(f"Monitoring for: {INTEREST}\n")
    for notice in NOTICES:
        r = await call(interest=INTEREST, notice=notice)
        mark = "RELEVANT" if r.relevant else "skip    "
        print(f"  [{mark}] {notice[:60]}")
        if r.relevant:
            relevant.append(notice)
            print(f"            -> {r.summary}")
    return relevant


if __name__ == "__main__":
    relevant = asyncio.run(main())
    # The two consumer-finance notices are kept; the EPA one is filtered out.
    assert len(relevant) == 2
    assert all("truck" not in r.lower() for r in relevant)
