#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-llm-core>=0.1.12,<0.2", "kaos-llm-client>=0.1.9,<0.2"]
# ///
"""Use case — Expertise & experience management.

Build an attorney-expertise database by extracting practice areas, industries,
and languages from a profile. A typed `Call` returns the structured expertise
record (aligning with a taxonomy like SALI in production). Offline via
FunctionClient.

Real-data note: the *source* profiles are typically scraped from firm websites
with `kaos-web` / `kaos-source` (network); the *extraction* shown here is offline.

Run it:

    uv run examples/uc-expertise-extract.py
"""

from __future__ import annotations

import asyncio
import json

from kaos_llm_client.providers.function import FunctionClient
from kaos_llm_client.types import ContentPart, ProviderResponse
from kaos_llm_core import Call, InputField, OutputField, Signature

PROFILE = (
    "Jane Doe is a partner in the firm's Mergers & Acquisitions and Private Equity "
    "practices, with deep experience advising clients in the technology and healthcare "
    "sectors. She is fluent in English and Spanish."
)


class Expertise(Signature):
    """Extract an attorney's expertise from a profile."""

    text: str = InputField(description="the attorney profile text")
    practice_areas: list[str] = OutputField(description="practice areas")
    industries: list[str] = OutputField(description="industry sectors")
    languages: list[str] = OutputField(description="spoken languages")


def fake_model(messages, profile):
    record = {
        "practice_areas": ["Mergers & Acquisitions", "Private Equity"],
        "industries": ["technology", "healthcare"],
        "languages": ["English", "Spanish"],
    }
    return ProviderResponse(
        provider="function", model="function-test", raw={},
        parts=[ContentPart(type="text", text=json.dumps(record))],
    )


async def main():
    call = Call(Expertise, model="function-test", client=FunctionClient(function=fake_model))
    e = await call(text=PROFILE)
    print(f"  practice areas: {', '.join(e.practice_areas)}")
    print(f"  industries:     {', '.join(e.industries)}")
    print(f"  languages:      {', '.join(e.languages)}")
    return e


if __name__ == "__main__":
    e = asyncio.run(main())
    assert "Private Equity" in e.practice_areas
    assert "healthcare" in e.industries and "Spanish" in e.languages
