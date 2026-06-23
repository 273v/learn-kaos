#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-llm-core>=0.1.12,<0.2", "kaos-llm-client>=0.1.9,<0.2"]
# ///
"""Use case — Matter data tagging.

Rich matter reporting needs every matter tagged with a practice area. A typed
`Call` reads a matter description and assigns the practice area (aligning with a
taxonomy like SALI in production). Offline via FunctionClient.

Run it:

    uv run examples/uc-matter-tagging.py
"""

from __future__ import annotations

import asyncio
import json
from typing import Literal

from kaos_llm_client.providers.function import FunctionClient
from kaos_llm_client.types import ContentPart, ProviderResponse
from kaos_llm_core import Call, InputField, OutputField, Signature

MATTERS = [
    "Advise on the merger of two portfolio companies and draft the purchase agreement.",
    "Defend the company in a patent infringement suit.",
    "Negotiate a commercial office lease for the new headquarters.",
]


class TagMatter(Signature):
    """Tag a matter with its primary practice area."""

    description: str = InputField(description="the matter description")
    practice_area: Literal["M&A", "litigation", "real estate", "employment"] = OutputField(
        description="the primary practice area"
    )


def fake_model(messages, profile):
    low = " ".join(m.get("content", "") for m in messages if m.get("role") == "user").lower()
    if "merger" in low or "purchase agreement" in low:
        area = "M&A"
    elif "infringement" in low or "suit" in low or "defend" in low:
        area = "litigation"
    elif "lease" in low or "office" in low:
        area = "real estate"
    else:
        area = "employment"
    return ProviderResponse(
        provider="function", model="function-test", raw={},
        parts=[ContentPart(type="text", text=json.dumps({"practice_area": area}))],
    )


async def main() -> list[str]:
    call = Call(TagMatter, model="function-test", client=FunctionClient(function=fake_model))
    areas = []
    for m in MATTERS:
        result = await call(description=m)
        areas.append(result.practice_area)
        print(f"  [{result.practice_area:<12}] {m[:50]}...")
    return areas


if __name__ == "__main__":
    areas = asyncio.run(main())
    assert areas == ["M&A", "litigation", "real estate"]
