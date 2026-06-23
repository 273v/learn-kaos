#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-llm-core>=0.1.12,<0.2", "kaos-llm-client>=0.1.9,<0.2"]
# ///
"""Use case — Commercial lending agreement analysis.

Build a covenant database for risk monitoring by extracting the financial
covenants from credit facility agreements. A typed `Call` returns the structured
covenant terms. Offline via FunctionClient.

Run it:

    uv run examples/uc-credit-covenants.py
"""

from __future__ import annotations

import asyncio
import json

from kaos_llm_client.providers.function import FunctionClient
from kaos_llm_client.types import ContentPart, ProviderResponse
from kaos_llm_core import Call, InputField, OutputField, Signature

AGREEMENT = (
    "The Borrower shall maintain a maximum total leverage ratio of 3.50 to 1.00 and a "
    "minimum interest coverage ratio of 3.00 to 1.00, tested quarterly. An Event of Default "
    "occurs upon any breach of these financial covenants."
)


class Covenants(Signature):
    """Extract the financial covenants from a credit agreement."""

    text: str = InputField(description="the credit agreement text")
    max_leverage_ratio: float = OutputField(description="maximum total leverage ratio")
    min_interest_coverage: float = OutputField(description="minimum interest coverage ratio")
    test_frequency: str = OutputField(description="how often covenants are tested")


def fake_model(messages, profile):
    covenants = {
        "max_leverage_ratio": 3.50,
        "min_interest_coverage": 3.00,
        "test_frequency": "quarterly",
    }
    return ProviderResponse(
        provider="function", model="function-test", raw={},
        parts=[ContentPart(type="text", text=json.dumps(covenants))],
    )


async def main():
    call = Call(Covenants, model="function-test", client=FunctionClient(function=fake_model))
    c = await call(text=AGREEMENT)
    print(f"  max leverage ratio:    {c.max_leverage_ratio:.2f}x")
    print(f"  min interest coverage: {c.min_interest_coverage:.2f}x")
    print(f"  tested:                {c.test_frequency}")
    return c


if __name__ == "__main__":
    c = asyncio.run(main())
    assert c.max_leverage_ratio == 3.50
    assert c.min_interest_coverage == 3.00 and c.test_frequency == "quarterly"
