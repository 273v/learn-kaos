#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "kaos-agents>=0.1.28,<0.2",
#   "kaos-llm-client>=0.1.9,<0.2",
#   "kaos-llm-core>=0.1.12,<0.2",
# ]
# ///
"""Your first KAOS agent — a stateful chat agent that remembers, run offline.

`kaos-agents` splits an agent into two parts: an `Agent` is frozen *config*
(instructions, model, pattern, tools); a `Runner` is the *engine* that drives
it. State doesn't live on the agent — it lives in session memory, hydrated from
a virtual filesystem each turn. That's why the agent below remembers turn 1 when
it answers turn 2.

Offline note: a real agent calls an LLM provider. To run this for free with no
API key, we substitute the model factory with a deterministic `FunctionClient`
— the same technique the kaos-agents test suite uses. Set `KAOS_LEARN_LIVE=1`
(and `ANTHROPIC_API_KEY`) to drop the substitution and use a real model.

Run it (offline, no key):

    uv run examples/first-agent.py
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import os

from kaos_agents.config import Agent, AgentPattern
from kaos_agents.runtime.runner import Runner
from kaos_core import KaosRuntime


def _fake_model(messages: list[dict], profile):
    """A deterministic stand-in for an LLM provider.

    The chat loop makes two kinds of structured calls — intent classification
    and the response — so we return the right shape for each. The response
    reports how many remembered turns it can see, which makes session memory
    visible in the output.
    """
    from kaos_llm_client.types import ContentPart, ProviderResponse

    blob = " ".join(str(m.get("content", "")) for m in messages)
    if "reasoning" in blob.lower() and "intent" in blob.lower():
        payload = {"intent": "respond", "confidence": 0.95, "reasoning": "a direct question"}
    else:
        remembered = blob.count("user:")  # user turns visible in the prompt's history
        payload = {"response": f"Offline reply — I can see {remembered} user message(s) of history."}
    return ProviderResponse(
        provider="function",
        model="function-test",
        raw={},
        parts=[ContentPart(type="text", text=json.dumps(payload))],
    )


@contextlib.contextmanager
def offline_model():
    """Swap the LLM factory for a FunctionClient unless running live."""
    if os.environ.get("KAOS_LEARN_LIVE"):
        yield "anthropic:claude-haiku-4-5"  # real model id; needs a key
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
    # test_mode() = in-memory, isolated VFS. Critical: with the default disk VFS,
    # session memory would leak across runs and tests would false-green.
    runtime = KaosRuntime.test_mode()

    with offline_model() as model:
        agent = Agent(instructions="Be brief.", model=model, pattern=AgentPattern.CHAT)
        runner = Runner(agent, runtime=runtime)

        # Same session id across both turns -> the agent remembers turn 1.
        r1 = await runner.turn("Hello!", "demo-session")
        r2 = await runner.turn("What did I just say?", "demo-session")

    print(f"turn 1: {r1.text}")
    print(f"turn 2: {r2.text}")
    print(f"cost (offline): ${r1.cost_usd:.4f}")
    return [r1.text, r2.text]


if __name__ == "__main__":
    replies = asyncio.run(main())
    if not os.environ.get("KAOS_LEARN_LIVE"):
        # Memory persists: turn 2 sees more history than turn 1.
        assert "1 user message" in replies[0], replies[0]
        assert "2 user message" in replies[1], replies[1]
