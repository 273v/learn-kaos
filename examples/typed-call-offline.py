#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-llm-core>=0.1.12,<0.2", "kaos-llm-client>=0.1.9,<0.2"]
# ///
"""From a raw prompt to a *typed* LLM call.

`kaos-llm-core` lets you program LLMs with types instead of prompt strings.
You declare a `Signature` — typed inputs and outputs — and a `Call` turns
it into a function that returns a validated, typed object. No parsing of
free-form text; the framework handles structured output and validation.

Runs offline with a `FunctionClient` fake model (returns canned JSON), so
there's no key or cost. Swap in a real client and the same `Call` works.

Run it:

    uv run examples/typed-call-offline.py
"""

from __future__ import annotations

import asyncio
import json

from kaos_llm_client.providers.function import FunctionClient
from kaos_llm_client.types import ContentPart, ProviderResponse
from kaos_llm_core import Call, InputField, OutputField, Signature


class ExtractParties(Signature):
    """Extract the parties named in a contract sentence."""

    text: str = InputField(description="contract text")
    parties: list[str] = OutputField(description="names of the parties")


def fake_model(messages: list[dict], profile) -> ProviderResponse:
    # A real model would read the prompt and generate this; we return the
    # exact structured JSON we want so the example is deterministic.
    payload = {"parties": ["Acme Corp", "Globex LLC"]}
    return ProviderResponse(
        provider="function",
        model="function-test",
        raw={},
        parts=[ContentPart(type="text", text=json.dumps(payload))],
    )


async def main() -> list[str]:
    call = Call(
        ExtractParties,
        model="function-test",
        client=FunctionClient(function=fake_model),
    )
    result = await call(text="This agreement is between Acme Corp and Globex LLC.")
    # `result` is a typed object, not a string — result.parties is a list[str].
    print(f"parties: {result.parties}")
    return result.parties


if __name__ == "__main__":
    parties = asyncio.run(main())
    assert parties == ["Acme Corp", "Globex LLC"], parties
