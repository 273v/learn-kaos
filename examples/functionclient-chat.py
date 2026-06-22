#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-llm-client>=0.1.9,<0.2"]
# ///
"""The offline LLM seam: a deterministic fake model via FunctionClient.

Every LLM example on this site runs for free in CI with no API key. The
trick is `FunctionClient` — a provider client that runs a Python callable
instead of making an HTTP request, while satisfying the *same* interface
as the real Anthropic / OpenAI / Google clients. So the same code path
(`client.chat(...)`) is exercised; only the model is faked.

By default this runs offline. Set `KAOS_LEARN_LIVE=1` (and an API key) to
hit a real provider instead — the rest of the program is identical.

Run it (offline, no key):

    uv run examples/functionclient-chat.py

Run it live:

    KAOS_LEARN_LIVE=1 ANTHROPIC_API_KEY=sk-... uv run examples/functionclient-chat.py
"""

from __future__ import annotations

import os

from kaos_llm_client.providers.function import FunctionClient
from kaos_llm_client.types import ContentPart, ProviderResponse


def fake_model(messages: list[dict], profile) -> ProviderResponse:
    """A deterministic 'model': echo the user's text back, uppercased.

    A real provider would return a generated completion here; for tests we
    return exactly what we want so assertions are stable.
    """
    user_text = messages[-1]["content"]
    return ProviderResponse(
        provider="function",
        model="function-test",
        raw={},
        parts=[ContentPart(type="text", text=f"FAKE MODEL SAYS: {user_text.upper()}")],
    )


def make_client():
    """Offline by default; a real client when KAOS_LEARN_LIVE is set."""
    if os.environ.get("KAOS_LEARN_LIVE"):
        from kaos_llm_client import create_client

        # Anthropic Haiku is the documented default for live examples.
        return create_client("anthropic:claude-haiku-4-5")
    return FunctionClient(function=fake_model)


def main() -> str:
    client = make_client()
    response = client.chat([{"role": "user", "content": "hello, kaos"}])
    print(f"model said: {response.text!r}")
    # The client records every call — handy for asserting what was sent.
    if isinstance(client, FunctionClient):
        print(f"calls recorded: {len(client.call_history)}")
    return response.text


if __name__ == "__main__":
    text = main()
    if not os.environ.get("KAOS_LEARN_LIVE"):
        # Offline path is fully deterministic.
        assert text == "FAKE MODEL SAYS: HELLO, KAOS", text
