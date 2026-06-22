#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-llm-core>=0.1.12,<0.2", "kaos-llm-client>=0.1.9,<0.2"]
# ///
"""Optimize an LLM program against a metric — and only keep changes that help.

Because a KAOS program is typed, an optimizer can improve it automatically: the
`BootstrapOptimizer` selects few-shot examples to add, re-evaluates on a held-out
validation set, and **accepts the change only if the metric improves**. No blind
prompt-tweaking — every change is gated on evidence.

Runs offline with a `FunctionClient` and a deterministic metric.

Run it:

    uv run examples/optimize-program.py
"""

from __future__ import annotations

import asyncio
import json

from kaos_llm_client.providers.function import FunctionClient
from kaos_llm_client.types import ContentPart, ProviderResponse
from kaos_llm_core import BootstrapOptimizer, Call, Example, InputField, OutputField, Signature


class Classify(Signature):
    """Classify a legal document's practice area."""

    text: str = InputField(description="document text")
    area: str = OutputField(description="practice area: lease, nda, or employment")


def fake_model(messages: list[dict], profile) -> ProviderResponse:
    blob = " ".join(str(m.get("content", "")) for m in messages).lower()
    if "rent" in blob or "lease" in blob:
        area = "lease"
    elif "confidential" in blob:
        area = "nda"
    else:
        area = "employment"
    return ProviderResponse(
        provider="function", model="function-test", raw={},
        parts=[ContentPart(type="text", text=json.dumps({"area": area}))],
    )


def accuracy(prediction, expected: dict) -> float:
    return 1.0 if getattr(prediction, "area", None) == expected.get("area") else 0.0


async def main():
    call = Call(Classify, model="function-test", client=FunctionClient(function=fake_model))

    train = [
        Example(inputs={"text": "The lease term is five years."}, outputs={"area": "lease"}),
        Example(inputs={"text": "Confidential information must be protected."}, outputs={"area": "nda"}),
    ]
    val = [Example(inputs={"text": "Rent is due monthly."}, outputs={"area": "lease"})]

    result = await BootstrapOptimizer(accuracy).optimize(call, train, val)

    print(f"  validation metric before: {result.metric_before:.0%}")
    print(f"  validation metric after:  {result.metric_after:.0%}")
    print(f"  examples bootstrapped:    {result.examples_added}")
    print(f"  change accepted:          {result.accepted}  ({result.stop_reason})")
    return result


if __name__ == "__main__":
    result = asyncio.run(main())
    # The optimizer ran, measured the metric, and made an evidence-based decision.
    assert isinstance(result.metric_before, float)
    assert isinstance(result.metric_after, float)
    # Here the baseline is already perfect, so a no-improvement change is NOT kept —
    # the optimizer is metric-gated, not blind.
    assert result.metric_after >= result.metric_before
