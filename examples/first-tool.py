#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-core>=0.1.4,<0.2"]
# ///
"""Author, register, and execute your first KAOS tool.

`kaos-core` is the dependency-light runtime every other package builds on.
A *tool* is a typed, MCP-native unit of work: you write an async function,
decorate it with `@kaos_tool`, register it on a `KaosRuntime`, and execute
it. The runtime derives the input schema from your type hints.

Fully offline and deterministic — no key, no network.

Run it:

    uv run examples/first-tool.py
"""

from __future__ import annotations

import asyncio

from kaos_core import (
    KaosRuntime,
    ToolAnnotations,
    ToolCapability,
    ToolCategory,
    kaos_tool,
)


@kaos_tool(
    name="kaos-learn-wordcount",
    description="Count the words in a piece of text.",
    category=ToolCategory.DATA,
    capability=ToolCapability.ANALYZE,
    # readOnly + idempotent: safe to call anytime; an agent may auto-allow it.
    annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True),
    auto_register=False,
)
async def word_count(text: str) -> int:
    return len(text.split())


async def main() -> str:
    runtime = KaosRuntime()
    runtime.tools.register_tool(word_count)

    tool = runtime.tools.get_tool("kaos-learn-wordcount")
    result = await tool.execute({"text": "the quick brown fox jumps"})

    # ToolResult wraps the return value; `.text` is the rendered output.
    print(f"word count: {result.text}")
    return result.text


if __name__ == "__main__":
    out = asyncio.run(main())
    assert out == "5", f"expected 5, got {out!r}"
