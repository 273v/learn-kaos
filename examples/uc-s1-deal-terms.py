#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-llm-core>=0.1.12,<0.2", "kaos-llm-client>=0.1.9,<0.2"]
# ///
"""Use case — SEC EDGAR IPO filing analysis.

Build a deal database from S-1 registration statements by extracting the offering
terms. A typed `Call` returns the structured deal points. Offline via
FunctionClient.

Real-data note: fetch real S-1 filings from SEC EDGAR (see the
how-to/pull-a-sec-filing recipe) or the public **kl3m** datasets on Hugging Face,
then run this extraction over them.

Run it:

    uv run examples/uc-s1-deal-terms.py
"""

from __future__ import annotations

import asyncio
import json

from kaos_llm_client.providers.function import FunctionClient
from kaos_llm_client.types import ContentPart, ProviderResponse
from kaos_llm_core import Call, InputField, OutputField, Signature

S1_EXCERPT = (
    "Acme Robotics, Inc. is offering 10,000,000 shares of common stock at an assumed "
    "initial public offering price of $18.00 per share. We intend to use the net proceeds "
    "for research and development and general corporate purposes. The shares will trade on "
    "the Nasdaq Global Market under the symbol ACME."
)


class IPODealTerms(Signature):
    """Extract the IPO deal terms from an S-1 registration statement."""

    text: str = InputField(description="the S-1 excerpt")
    issuer: str = OutputField(description="the issuing company")
    shares_offered: int = OutputField(description="number of shares offered")
    price_per_share: float = OutputField(description="price per share in USD")
    ticker: str = OutputField(description="the ticker symbol")


def fake_model(messages, profile):
    terms = {
        "issuer": "Acme Robotics, Inc.",
        "shares_offered": 10_000_000,
        "price_per_share": 18.00,
        "ticker": "ACME",
    }
    return ProviderResponse(
        provider="function", model="function-test", raw={},
        parts=[ContentPart(type="text", text=json.dumps(terms))],
    )


async def main():
    call = Call(IPODealTerms, model="function-test", client=FunctionClient(function=fake_model))
    t = await call(text=S1_EXCERPT)
    raised = t.shares_offered * t.price_per_share
    print(f"  issuer:  {t.issuer} ({t.ticker})")
    print(f"  offering: {t.shares_offered:,} shares @ ${t.price_per_share:.2f}")
    print(f"  gross raise: ${raised:,.0f}")
    return t


if __name__ == "__main__":
    t = asyncio.run(main())
    assert t.ticker == "ACME" and t.shares_offered == 10_000_000
    assert t.price_per_share == 18.00
