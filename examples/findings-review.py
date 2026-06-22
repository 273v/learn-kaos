#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "kaos-agents>=0.1.28,<0.2",
#   "kaos-content>=0.1.6,<0.2",
#   "kaos-nlp-core>=0.1.6,<0.2",
#   "kaos-llm-client>=0.1.9,<0.2",
#   "kaos-llm-core>=0.1.12,<0.2",
# ]
# ///
"""Review a contract for issues with a recall-first FindingsAgent.

This is the NDA-review workflow KAOS was built for. A `FindingsAgent` enumerates
every candidate sentence, filters them for relevance to your question, and
synthesizes the survivors into an answer — a recall-first pipeline tuned so a
careful reviewer doesn't miss a clause. It runs under a cost cap.

Offline via the FunctionClient substitution: the fake model parses the real
candidate ids out of its own prompt and scores them, so the pipeline genuinely
flows end to end. Set `KAOS_LEARN_LIVE=1` + a key for a real review.

Run it:

    uv run examples/findings-review.py
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import os
import re

import kaos_content as kc
from kaos_agents.patterns.findings import FindingsAgent, every_sentence_selector
from kaos_content.views import DocumentView
from kaos_nlp_core._defaults import get_default_punkt_tokenizer


def _fake_model(messages: list[dict], profile):
    from kaos_llm_client.types import ContentPart, ProviderResponse

    blob = " ".join(str(m.get("content", "")) for m in messages)
    # The candidate ids are the tag attributes (ignore the prompt's "..." example).
    ids = [i for i in re.findall(r'finding_id="([^"]+)"', blob) if i != "..."]
    if "survivors" in blob.lower():
        # Mark every real candidate relevant (a real model would score them).
        payload = {
            "survivors": [
                {"finding_id": i, "relevance": 0.9, "reasoning": "an unusual term"}
                for i in ids
            ]
        }
    elif "answer" in blob.lower():
        payload = {
            "answer": "The NDA's ten-year confidentiality survival period and "
            "five-year non-solicit are both unusually long."
        }
    else:
        payload = {"answer": "See findings."}
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


def build_nda() -> kc.ContentDocument:
    b = kc.DocumentBuilder()
    b.heading(1, "Mutual Non-Disclosure Agreement")
    b.paragraph("Confidential Information must be protected for ten years following disclosure.")
    b.paragraph("The receiving party shall not solicit employees for five years.")
    return b.build()


async def main():
    view = DocumentView(build_nda(), sentence_segmenter=get_default_punkt_tokenizer())

    with offline_model() as model:
        agent = FindingsAgent(
            selector=every_sentence_selector,
            filter_model=model,
            synthesis_model=model,
            max_cost_usd=0.50,  # cost cap as a contract
        )
        result = await agent.run("Find unusual clauses a reviewer should flag.", view)

    print(f"enumerated {result.total_enumerated} candidate(s), "
          f"{result.total_filtered} survived filtering\n")
    for f in result.findings:
        print(f"  • ({f.relevance:.1f}) {f.reasoning}")
    print(f"\n  synthesis: {result.answer}")
    print(f"  cost (offline): ${result.filter_cost_usd + result.synthesis_cost_usd:.4f}")
    return result


if __name__ == "__main__":
    result = asyncio.run(main())
    if not os.environ.get("KAOS_LEARN_LIVE"):
        assert result.total_filtered >= 1, "expected at least one finding"
        assert "unusually long" in result.answer
