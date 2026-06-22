#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "kaos-agents>=0.1.28,<0.2",
#   "kaos-llm-client>=0.1.9,<0.2",
#   "kaos-llm-core>=0.1.12,<0.2",
# ]
# ///
"""A full research agent: answer over a corpus with verified citations — or refuse.

This is the marquee KAOS workflow. A `ResearchAgent` retrieves relevant passages
from a document corpus, answers the question, and **verifies** every cited quote
against its source. If the corpus doesn't support an answer, it returns a typed
refusal instead of guessing.

Offline note: like `first-agent`, we substitute the model factory with a
deterministic `FunctionClient` so it runs free, with no key, in CI. The fake
model parses the real source URI and a verbatim quote out of the corpus it's
given, so the citation genuinely verifies — the grounding is real even though
the "model" is fake. Set `KAOS_LEARN_LIVE=1` + `ANTHROPIC_API_KEY` for a real run.

Run it (offline, no key):

    uv run examples/research-agent.py
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import os
import re

from kaos_agents import ResearchAgent, SessionMemory, SessionStore
from kaos_core import KaosRuntime

CORPUS = {
    "lease.txt": (
        "Master Lease Agreement. The lease term is five years. "
        "Rent is due monthly on the first business day of each month."
    ),
    "nda.txt": (
        "Mutual NDA. Confidential Information must be protected for three years "
        "following the date of disclosure."
    ),
}


def _fake_model(messages: list[dict], profile):
    """Deterministic stand-in. Drives the research turn by returning the exact
    structured shapes each step expects, parsing real quotes from the corpus so
    citations verify."""
    from kaos_llm_client.types import ContentPart, ProviderResponse

    blob = " ".join(str(m.get("content", "")) for m in messages)
    low = blob.lower()

    if "reasoning" in low and "intent" in low:
        payload = {"intent": "research", "confidence": 0.95, "reasoning": "asks about the documents"}
    elif "=== source:" in low and "result" in low:
        # The corpus QA step. Quote verbatim from the passage we were given.
        # The corpus is about rent/NDAs; a question about patents has no support.
        quote = "Rent is due monthly on the first business day"
        if "patent" not in low and quote.lower() in low:  # corpus supports the answer
            m = re.search(r"=== SOURCE:\s*(.+?)\s*===", blob, re.IGNORECASE)
            uri = m.group(1) if m else "lease.txt"
            payload = {
                "result": {
                    "kind": "answer",
                    "value": "Rent is due monthly on the first business day of each month.",
                    "confidence": 0.95,
                    "claims": [
                        {
                            "statement": "Rent is due monthly.",
                            "claim_type": "temporal",
                            "confidence": 0.95,
                            "supporting_spans": [
                                {"source_uri": uri, "char_span": [0, 0], "quote": quote}
                            ],
                        }
                    ],
                }
            }
        else:  # nothing in the corpus supports the question -> refuse
            payload = {
                "result": {
                    "kind": "insufficient_evidence",
                    "reason": "The corpus does not address that question.",
                    "attempted_claims": [],
                    "missing": ["the requested topic"],
                }
            }
    else:
        payload = {"response": "See the cited answer above."}

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


async def ask(agent: ResearchAgent, question: str, session: str) -> str:
    response = await agent.turn(question, session)
    return response.text


async def main() -> tuple[str, str]:
    runtime = KaosRuntime.test_mode()  # in-memory, isolated
    memory = SessionMemory("research-demo")

    with offline_model() as model:
        agent = ResearchAgent(runtime.vfs, model=model, max_react_iterations=2)
        for uri, text in CORPUS.items():
            agent.load_document(memory, uri, text)
        await SessionStore(runtime.vfs).save(memory)

        # 1. A question the corpus answers -> grounded, verified citation.
        grounded = await ask(agent, "When is rent due?", "research-demo")
        # 2. A question nothing in the corpus addresses -> typed refusal.
        refused = await ask(agent, "What are the patent infringement damages?", "research-demo")

    print("Q: When is rent due?")
    print(f"   {grounded}\n")
    print("Q: What are the patent infringement damages?")
    print(f"   {refused}")
    return grounded, refused


if __name__ == "__main__":
    grounded, refused = asyncio.run(main())
    if not os.environ.get("KAOS_LEARN_LIVE"):
        # The answerable question is grounded with a verified citation...
        assert "Verified" in grounded, grounded
        # ...and the unanswerable one is refused, not fabricated.
        assert "sufficient evidence" in refused.lower(), refused
        assert "patent" not in refused.lower(), "must not fabricate a patent answer"
