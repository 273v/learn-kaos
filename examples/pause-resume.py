#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-agents>=0.1.28,<0.2"]
# ///
"""Pause an agent on a sensitive action and resume after approval.

When an agent wants to run a tool the [permission policy](configure-permissions)
marks ASK, the turn pauses and emits `ToolCallApprovalRequired` with a durable
`RunState`. That state serializes to JSON, so the run can wait for a human — even
across a process restart — and then `Runner.resume(state, approved=...)` either
runs the tool or skips it.

This example builds and round-trips that pause state (the offline-testable core
of the flow). Deterministic.

Run it:

    uv run examples/pause-resume.py
"""

from __future__ import annotations

from kaos_agents.runtime.interrupts import PendingToolCall, RunState


def main() -> RunState:
    # An agent paused, wanting to run a destructive tool — captured as a durable
    # RunState the host can persist and review.
    pending = PendingToolCall(
        call_id="tc_01",
        tool_name="kaos-source-delete",
        arguments=(("path", "/matter/acme/draft.docx"),),
        reason="destructive: deletes a file",
    )
    state = RunState(
        run_id="run_42",
        session_id="acme-review",
        event_count=7,
        original_message="Clean up the old drafts.",
        pending_tool_call=pending,
    )

    # Persist it (e.g. to a queue/DB) — survives a process restart.
    blob = state.to_json()
    print(f"paused run serialized to {len(blob)} bytes of JSON")

    # Later — possibly in a different process — restore and review it.
    restored = RunState.from_json(blob)
    p = restored.pending_tool_call
    print(f"awaiting approval: tool={p.tool_name!r} reason={p.reason!r}")
    print(f"  run={restored.run_id} session={restored.session_id}")
    print("operator decides → Runner.resume(state, approved=True)  runs the tool")
    print("                 → Runner.resume(state, approved=False) skips it")
    return restored


if __name__ == "__main__":
    restored = main()
    # The pending tool call survives serialization intact — that's what lets a
    # paused run wait for a human across a restart.
    assert restored.pending_tool_call.tool_name == "kaos-source-delete"
    assert restored.run_id == "run_42"
    assert dict(restored.pending_tool_call.arguments)["path"].endswith("draft.docx")
