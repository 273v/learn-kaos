#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "kaos-agents>=0.1.28,<0.2",
#   "kaos-llm-client>=0.1.9,<0.2",
#   "kaos-llm-core>=0.1.12,<0.2",
# ]
# ///
"""Delegate work to a specialist sub-agent.

A KAOS agent can hand a sub-task to another agent: `agent_as_tool` wraps an
`Agent` as a callable sub-agent, and `Runner.delegate` runs it, emitting
`Span(subagent, start/complete)` events with the result. This is how you compose
a coordinator with specialists (a drafter, a researcher, a reviewer) instead of
one monolithic agent.

Runs offline via the FunctionClient substitution (see `first-agent`).

Run it:

    uv run examples/agent-delegation.py
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import os

from kaos_agents.config import Agent, AgentPattern
from kaos_agents.runtime.delegation import agent_as_tool
from kaos_agents.runtime.runner import Runner
from kaos_core import KaosRuntime


def _fake_model(messages: list[dict], profile):
    from kaos_llm_client.types import ContentPart, ProviderResponse

    low = " ".join(str(m.get("content", "")) for m in messages).lower()
    if "reasoning" in low and "intent" in low:
        payload = {"intent": "respond", "confidence": 0.95, "reasoning": "a drafting task"}
    else:
        payload = {"response": "DRAFT: Memo to counsel re: the indemnification clause."}
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


async def main() -> str:
    runtime = KaosRuntime.test_mode()

    with offline_model() as model:
        # A specialist sub-agent, wrapped as a delegatable tool.
        drafter = Agent(instructions="You draft legal memos.", model=model, pattern=AgentPattern.CHAT)
        delegated = agent_as_tool(drafter, name="memo_drafter", description="Drafts legal memos.")

        # A coordinator delegates a task to it.
        coordinator = Agent(instructions="Coordinate specialists.", model=model, pattern=AgentPattern.CHAT)
        runner = Runner(coordinator, runtime=runtime)

        result_summary = ""
        async for event in runner.delegate(delegated, "Draft a memo to counsel.", "deleg-1"):
            subject = getattr(event, "subject", None)
            phase = getattr(event, "phase", None)
            attrs = getattr(event, "attributes", {}) or {}
            print(f"  event: subagent {phase}  attrs={list(attrs)}")
            if str(subject) == "subagent" and str(phase) == "complete":
                result_summary = attrs.get("result_summary", "")

    print(f"\n  sub-agent result: {result_summary}")
    return result_summary


if __name__ == "__main__":
    summary = asyncio.run(main())
    if not os.environ.get("KAOS_LEARN_LIVE"):
        assert "DRAFT" in summary, summary
        assert "counsel" in summary.lower()
