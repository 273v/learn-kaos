#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-mcp>=0.1.3,<0.2", "kaos-core>=0.1.4,<0.2"]
# ///
"""Expose a KAOS runtime's tools over the Model Context Protocol.

`kaos-mcp` is the bridge that serves *any* runtime's tools to an MCP client
(Claude Code, Codex, ...). It holds no tools of its own — it exposes whatever you
mount on it. This example registers tools on a runtime and builds the bridge,
showing exactly which tools it would serve. (It doesn't start the long-running
server, so it stays a one-shot offline example; in practice you'd call
`server.run_stdio()` or `--http`.)

Run it:

    uv run examples/serve-over-mcp.py
"""

from __future__ import annotations

from kaos_core import (
    KaosRuntime,
    ToolAnnotations,
    ToolCapability,
    ToolCategory,
    kaos_tool,
)
from kaos_mcp import KaosMCPServer


@kaos_tool(
    name="kaos-demo-echo",
    description="Echo the input text.",
    category=ToolCategory.DATA,
    capability=ToolCapability.TRANSFORM,
    annotations=ToolAnnotations(readOnlyHint=True),
    auto_register=False,
)
async def echo(text: str) -> str:
    return text


@kaos_tool(
    name="kaos-demo-wordcount",
    description="Count words.",
    category=ToolCategory.DATA,
    capability=ToolCapability.ANALYZE,
    annotations=ToolAnnotations(readOnlyHint=True),
    auto_register=False,
)
async def word_count(text: str) -> int:
    return len(text.split())


def main() -> list[str]:
    runtime = KaosRuntime()
    runtime.tools.register_tool(echo)
    runtime.tools.register_tool(word_count)

    tool_names = runtime.tools.list_tools()
    print(f"runtime has {len(tool_names)} tool(s): {tool_names}")

    # Mount the runtime on the MCP bridge — these tools become available to any
    # MCP client once you run the server.
    server = KaosMCPServer(runtime)
    print("bridge built; to serve them, call server.run_stdio() (or --http).")
    print(f"would expose over MCP: {tool_names}")
    assert server is not None
    return tool_names


if __name__ == "__main__":
    names = main()
    assert "kaos-demo-echo" in names
    assert "kaos-demo-wordcount" in names
    assert len(names) == 2
