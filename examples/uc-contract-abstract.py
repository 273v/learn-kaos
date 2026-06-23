#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-llm-core>=0.1.12,<0.2", "kaos-llm-client>=0.1.9,<0.2"]
# ///
"""Use case — Post-execution contract abstraction.

Track executed contracts by extracting the obligations that drive calendars and
alerts: effective date, term, renewal, and governing law. A typed `Call` returns
a validated abstract you can store and report on. Offline via FunctionClient.

Run it:

    uv run examples/uc-contract-abstract.py
"""

from __future__ import annotations

import asyncio
import json

from kaos_llm_client.providers.function import FunctionClient
from kaos_llm_client.types import ContentPart, ProviderResponse
from kaos_llm_core import Call, InputField, OutputField, Signature

CONTRACT = (
    "This Master Services Agreement is effective as of January 1, 2026, for an initial "
    "term of three years, and renews automatically for successive one-year terms unless "
    "either party gives 90 days' notice. This Agreement is governed by the laws of Delaware."
)


class ContractAbstract(Signature):
    """Abstract the key tracking fields from an executed contract."""

    text: str = InputField(description="the contract text")
    effective_date: str = OutputField(description="effective date (YYYY-MM-DD)")
    term_years: int = OutputField(description="initial term in years")
    auto_renews: bool = OutputField(description="whether it renews automatically")
    governing_law: str = OutputField(description="governing-law jurisdiction")


def fake_model(messages, profile):
    abstract = {
        "effective_date": "2026-01-01",
        "term_years": 3,
        "auto_renews": True,
        "governing_law": "Delaware",
    }
    return ProviderResponse(
        provider="function", model="function-test", raw={},
        parts=[ContentPart(type="text", text=json.dumps(abstract))],
    )


async def main():
    call = Call(ContractAbstract, model="function-test", client=FunctionClient(function=fake_model))
    a = await call(text=CONTRACT)
    print(f"  effective:     {a.effective_date}")
    print(f"  term:          {a.term_years} years")
    print(f"  auto-renews:   {a.auto_renews}")
    print(f"  governing law: {a.governing_law}")
    return a


if __name__ == "__main__":
    a = asyncio.run(main())
    assert a.term_years == 3 and a.auto_renews is True
    assert a.governing_law == "Delaware"
