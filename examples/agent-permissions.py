#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-agents>=0.1.28,<0.2", "kaos-core>=0.1.4,<0.2"]
# ///
"""Decide which tool calls an agent may make — allow, ask, or deny.

Before an agent runs a tool, its `PermissionPolicy` decides what's allowed. The
default-safe policy auto-allows read-only tools and auto-asks for destructive
ones; you add glob rules to allow/deny specific tools. Evaluating a policy needs
no LLM, so this is fully offline and deterministic.

Run it:

    uv run examples/agent-permissions.py
"""

from __future__ import annotations

from kaos_core.types.metadata import ToolAnnotations

from kaos_agents.runtime.permissions import (
    PermissionDecision,
    PermissionPolicy,
    PermissionRule,
)

READ_ONLY = ToolAnnotations(readOnlyHint=True)
DESTRUCTIVE = ToolAnnotations(destructiveHint=True)


def main() -> dict[str, str]:
    # 1. The default-safe policy: read-only auto-allowed, destructive auto-asked.
    safe = PermissionPolicy.default_safe()
    d_read = safe.evaluate("kaos-pdf-extract", READ_ONLY)
    d_destroy = safe.evaluate("kaos-agent-memory-clear", DESTRUCTIVE)

    # 2. A custom policy: explicitly deny anything matching *-delete*,
    #    and allow the web fetch tools outright.
    strict = PermissionPolicy(
        rules=(
            PermissionRule("*-delete*", PermissionDecision.DENY, "no deletes"),
            PermissionRule("kaos-web-*", PermissionDecision.ALLOW, "web reads ok"),
        )
    )
    d_delete = strict.evaluate("kaos-source-delete", DESTRUCTIVE)
    d_fetch = strict.evaluate("kaos-web-fetch", READ_ONLY)

    decisions = {
        "default-safe: read-only tool": str(d_read),
        "default-safe: destructive tool": str(d_destroy),
        "strict: *-delete* tool": str(d_delete),
        "strict: kaos-web-* tool": str(d_fetch),
    }
    for label, decision in decisions.items():
        print(f"  {decision:<5}  {label}")
    return decisions


if __name__ == "__main__":
    d = main()
    assert d["default-safe: read-only tool"] == "allow"
    assert d["default-safe: destructive tool"] == "ask"
    assert d["strict: *-delete* tool"] == "deny"
    assert d["strict: kaos-web-* tool"] == "allow"
