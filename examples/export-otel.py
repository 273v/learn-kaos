#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "kaos-agents[otel]>=0.1.28,<0.2",
#   "kaos-llm-client>=0.1.9,<0.2",
#   "kaos-llm-core>=0.1.12,<0.2",
#   "opentelemetry-sdk",
# ]
# ///
"""Trace an agent turn with OpenTelemetry.

A KAOS agent turn is an [event stream](events-and-spans); `OTelHook` maps those
events onto standard OpenTelemetry spans, so your agent's internals show up in
the same tracing tools you already use for services — no bespoke observability
layer. Here we capture the spans with an in-memory exporter to prove they're
emitted; in production you'd export to your OTLP collector instead.

Runs offline via the FunctionClient substitution.

Run it:

    uv run examples/export-otel.py
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import os

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from kaos_agents.config import Agent, AgentPattern
from kaos_agents.hooks.otel import OTelHook
from kaos_agents.runtime.runner import Runner
from kaos_core import KaosRuntime


def _fake_model(messages: list[dict], profile):
    from kaos_llm_client.types import ContentPart, ProviderResponse

    low = " ".join(str(m.get("content", "")) for m in messages).lower()
    payload = (
        {"intent": "respond", "confidence": 0.95, "reasoning": "x"}
        if "reasoning" in low and "intent" in low
        else {"response": "Hello from the agent."}
    )
    return ProviderResponse(
        provider="function", model="function-test", raw={},
        parts=[ContentPart(type="text", text=json.dumps(payload))],
    )


@contextlib.contextmanager
def offline_model():
    if os.environ.get("KAOS_LEARN_LIVE"):
        yield "anthropic:claude-haiku-4-5"
        return
    from unittest.mock import patch

    from kaos_llm_client.providers.function import FunctionClient

    fc = FunctionClient(function=_fake_model)
    with (
        patch("kaos_llm_core.programs.call.create_client", return_value=fc),
        patch("kaos_llm_client.create_client", return_value=fc),
    ):
        yield "function-test"


async def main() -> list[str]:
    # Wire an in-memory OTel exporter (use an OTLP exporter in production).
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    runtime = KaosRuntime.test_mode()
    with offline_model() as model:
        agent = Agent(model=model, pattern=AgentPattern.CHAT)
        # The OTelHook turns the turn's events into OTel spans.
        runner = Runner(agent, runtime=runtime, hooks=(OTelHook(),))
        await runner.turn("Summarize the lease.", "otel-demo")

    spans = exporter.get_finished_spans()
    names = sorted(s.name for s in spans)
    print(f"captured {len(spans)} OpenTelemetry span(s):\n")
    for name in names:
        print(f"  {name}")
    return names


if __name__ == "__main__":
    names = asyncio.run(main())
    # The turn produced real OTel spans for its phases.
    assert "agent.turn" in names
    assert any("intent" in n for n in names)
