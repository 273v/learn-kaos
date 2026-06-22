#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-llm-client>=0.1.9,<0.2"]
# ///
"""Fall back to a second provider when the first one fails.

Real deployments hedge across providers: if the primary errors (outage, rate
limit, transport failure), retry on a backup. `FallbackClient` wraps an ordered
list of clients and tries the next one when the current raises a recoverable
error — all behind the same `client.chat(...)` interface.

This runs offline: the "primary" is a FunctionClient whose handler raises, and
the "backup" is one that answers. Same shape with real providers.

Run it:

    uv run examples/provider-failover.py
"""

from __future__ import annotations

from kaos_llm_client.errors import KaosLLMProviderError
from kaos_llm_client.providers.fallback import FallbackClient
from kaos_llm_client.providers.function import FunctionClient
from kaos_llm_client.types import ContentPart, ProviderResponse


def failing_handler(messages, profile):
    # Simulate a provider outage / rate limit.
    raise KaosLLMProviderError(
        "primary provider is unavailable", provider="primary", status_code=503
    )


def backup_handler(messages, profile):
    return ProviderResponse(
        provider="function",
        model="backup",
        raw={},
        parts=[ContentPart(type="text", text="answered by the backup provider")],
    )


def main() -> str:
    primary = FunctionClient(model="primary", function=failing_handler)
    backup = FunctionClient(model="backup", function=backup_handler)

    # Try primary first; on a recoverable error, fall back to backup.
    client = FallbackClient([primary, backup])
    response = client.chat([{"role": "user", "content": "hello"}])

    print(f"primary calls attempted: {len(primary.call_history)}")
    print(f"backup calls attempted:  {len(backup.call_history)}")
    print(f"answer: {response.text!r}")
    return response.text


if __name__ == "__main__":
    text = main()
    # The primary failed, so the backup answered.
    assert text == "answered by the backup provider", text
