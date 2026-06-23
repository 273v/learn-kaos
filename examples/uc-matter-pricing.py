#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-llm-core>=0.1.12,<0.2", "kaos-llm-client>=0.1.9,<0.2"]
# ///
"""Use case — Matter / RFP pricing.

Estimate the cost and staffing of a new matter from its scope, using patterns
from past matters. A typed `Call` returns a structured estimate you can put in an
RFP response. Offline via FunctionClient.

Real-data note: a production estimator trains on a firm's historical matter data
(e.g. with kaos-ml-core regression); this shows the structured-estimate surface.

Run it:

    uv run examples/uc-matter-pricing.py
"""

from __future__ import annotations

import asyncio
import json
from typing import Literal

from kaos_llm_client.providers.function import FunctionClient
from kaos_llm_client.types import ContentPart, ProviderResponse
from kaos_llm_core import Call, InputField, OutputField, Signature

RFP = (
    "Defend a mid-size manufacturer in complex multi-district patent litigation "
    "expected to run two years through trial, with extensive expert discovery."
)


class MatterEstimate(Signature):
    """Estimate the cost and staffing for a new matter from its scope."""

    scope: str = InputField(description="the matter scope / RFP description")
    complexity: Literal["low", "medium", "high"] = OutputField(description="complexity")
    estimated_cost_usd: int = OutputField(description="estimated total cost in USD")
    recommended_partners: int = OutputField(description="number of partners to staff")
    recommended_associates: int = OutputField(description="number of associates to staff")


def fake_model(messages, profile):
    low = " ".join(m.get("content", "") for m in messages if m.get("role") == "user").lower()
    high = any(k in low for k in ("complex", "multi-district", "two years", "trial"))
    estimate = {
        "complexity": "high" if high else "medium",
        "estimated_cost_usd": 4_500_000 if high else 750_000,
        "recommended_partners": 2 if high else 1,
        "recommended_associates": 5 if high else 2,
    }
    return ProviderResponse(
        provider="function", model="function-test", raw={},
        parts=[ContentPart(type="text", text=json.dumps(estimate))],
    )


async def main():
    call = Call(MatterEstimate, model="function-test", client=FunctionClient(function=fake_model))
    e = await call(scope=RFP)
    print(f"  complexity:      {e.complexity}")
    print(f"  estimated cost:  ${e.estimated_cost_usd:,}")
    print(f"  staffing:        {e.recommended_partners} partner(s), "
          f"{e.recommended_associates} associate(s)")
    return e


if __name__ == "__main__":
    e = asyncio.run(main())
    assert e.complexity == "high"
    assert e.estimated_cost_usd == 4_500_000
