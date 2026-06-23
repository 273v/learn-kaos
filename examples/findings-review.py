#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "kaos-agents>=0.1.28,<0.2",
#   "kaos-office>=0.1.0,<0.2",
#   "kaos-content>=0.1.6,<0.2",
#   "kaos-nlp-core>=0.1.6,<0.2",
#   "kaos-llm-client>=0.1.9,<0.2",
#   "kaos-llm-core>=0.1.12,<0.2",
# ]
# ///
"""Review a real contract for issues with a recall-first FindingsAgent.

This is the NDA-review workflow KAOS was built for, run over a **real** mutual NDA
that ships with `kaos-agents`. A `FindingsAgent` enumerates every candidate
sentence, filters them for relevance to your question, and synthesizes the
survivors into an answer — a recall-first pipeline so a careful reviewer doesn't
miss a clause. It runs under a cost cap.

Offline via the FunctionClient substitution: the fake model reads each candidate
out of its own prompt and flags the ones mentioning confidentiality terms, so the
pipeline genuinely flows end to end over the real document. Set `KAOS_LEARN_LIVE=1`
+ a key for a real review.

Run it:

    uv run examples/findings-review.py
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import os
import re
from importlib.resources import files

from kaos_agents.patterns.findings import FindingsAgent, every_sentence_selector
from kaos_content.views import DocumentView
from kaos_nlp_core._defaults import get_default_punkt_tokenizer
from kaos_office import parse_docx

# Terms a confidentiality reviewer cares about.
FLAGS = ("confidential", "disclos", "term", "years", "survive", "return", "destroy")


def _fake_model(messages: list[dict], profile):
    from kaos_llm_client.types import ContentPart, ProviderResponse

    blob = " ".join(str(m.get("content", "")) for m in messages)
    if "survivors" in blob.lower():
        # Each candidate is <untrusted_document_content finding_id="X">TEXT</...>.
        pairs = re.findall(
            r'<untrusted_document_content finding_id="([^"]+)"[^>]*>(.*?)</untrusted_document_content>',
            blob,
            re.DOTALL,
        )
        survivors = [
            {"finding_id": fid, "relevance": 0.9, "reasoning": "confidentiality term"}
            for fid, text in pairs
            if fid != "..." and any(k in text.lower() for k in FLAGS)
        ]
        payload = {"survivors": survivors}
    elif "answer" in blob.lower():
        payload = {"answer": "The NDA's confidentiality scope, term, and return/destroy "
                   "obligations are the clauses to review."}
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


def load_real_nda() -> DocumentView:
    # A real mutual NDA bundled with kaos-agents.
    ndas = files("kaos_agents.examples.nda_review").joinpath("ndas")
    path = next(f for f in sorted(ndas.iterdir(), key=lambda p: p.name) if f.name.endswith(".docx"))
    print(f"reviewing: {path.name}\n")
    return DocumentView(parse_docx(str(path)), sentence_segmenter=get_default_punkt_tokenizer())


async def main():
    view = load_real_nda()

    with offline_model() as model:
        agent = FindingsAgent(
            selector=every_sentence_selector,
            filter_model=model,
            synthesis_model=model,
            max_cost_usd=0.50,  # cost cap as a contract
        )
        result = await agent.run("Find the confidentiality terms a reviewer should check.", view)

    print(f"enumerated {result.total_enumerated} candidate sentence(s), "
          f"{result.total_filtered} flagged for review\n")
    for f in result.findings[:8]:
        print(f"  • ({f.relevance:.1f}) {f.reasoning}")
    print(f"\n  synthesis: {result.answer}")
    print(f"  cost (offline): ${result.filter_cost_usd + result.synthesis_cost_usd:.4f}")
    return result


if __name__ == "__main__":
    result = asyncio.run(main())
    if not os.environ.get("KAOS_LEARN_LIVE"):
        # The real NDA has many sentences; several mention confidentiality terms.
        assert result.total_enumerated > 10, "should enumerate a real multi-clause NDA"
        assert result.total_filtered >= 1, "expected at least one flagged clause"
