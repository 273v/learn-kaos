#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-llm-core>=0.1.12,<0.2", "kaos-llm-client>=0.1.9,<0.2"]
# ///
"""Use case — Pre-bill UTBMS task coding.

Outside-counsel guidelines require every billing line to carry a UTBMS task code.
A typed `Call` assigns the code from the narrative — automating pre-bill review.
Offline via FunctionClient.

Run it:

    uv run examples/uc-billing-utbms.py
"""

from __future__ import annotations

import asyncio
import json
from typing import Literal

from kaos_llm_client.providers.function import FunctionClient
from kaos_llm_client.types import ContentPart, ProviderResponse
from kaos_llm_core import Call, InputField, OutputField, Signature

# A few UTBMS litigation (L) task codes.
LINES = [
    "Draft and revise motion to dismiss.",
    "Telephone conference with client regarding case strategy.",
    "Review and analyze documents produced in discovery.",
]


class CodeLine(Signature):
    """Assign the UTBMS litigation task code to a billing narrative."""

    narrative: str = InputField(description="the billing line narrative")
    task_code: Literal["L120", "L160", "L320", "L390"] = OutputField(
        description="UTBMS code: L120 analysis/strategy, L160 settlement/client comms, "
        "L320 document production/review, L390 other case assessment"
    )


def fake_model(messages, profile):
    low = " ".join(m.get("content", "") for m in messages if m.get("role") == "user").lower()
    if "motion" in low or "draft" in low:
        code = "L120"
    elif "client" in low or "conference" in low:
        code = "L160"
    elif "documents" in low or "discovery" in low:
        code = "L320"
    else:
        code = "L390"
    return ProviderResponse(
        provider="function", model="function-test", raw={},
        parts=[ContentPart(type="text", text=json.dumps({"task_code": code}))],
    )


async def main() -> list[str]:
    call = Call(CodeLine, model="function-test", client=FunctionClient(function=fake_model))
    codes = []
    for line in LINES:
        result = await call(narrative=line)
        codes.append(result.task_code)
        print(f"  {result.task_code}  {line}")
    return codes


if __name__ == "__main__":
    codes = asyncio.run(main())
    assert codes == ["L120", "L160", "L320"]
