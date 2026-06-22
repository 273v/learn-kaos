#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-llm-core>=0.1.12,<0.2"]
# ///
"""Cap LLM spend with a Budget — refuse further work at the ceiling.

A multi-step program or agent can make many model calls; a `Budget` bounds the
run by cost, tokens, trials, or wall-clock time and enforces it *before* spend
happens. The run stops at the ceiling rather than blowing past it. Here we drive
a `BudgetTracker` directly to show the enforcement; in a program you pass the
`Budget` and the framework consumes it for you.

Fully offline and deterministic.

Run it:

    uv run examples/cap-cost.py
"""

from __future__ import annotations

from kaos_llm_core import Budget


def main():
    # A $0.10 ceiling for this run.
    tracker = Budget(max_cost_usd=0.10).make_tracker()

    # Each "step" spends a little. The framework calls consume() per model call;
    # we simulate three calls at $0.04 each. `exhausted()` returns a StopReason
    # (e.g. `budget_cost`) once a limit is crossed, or None while there's room.
    stop = None
    for i in range(1, 4):
        tracker.consume(cost_usd=0.04)
        stop = tracker.exhausted()
        status = f"{stop} — stop" if stop else "ok, continue"
        print(f"  after call {i}: spent ${tracker.cost_usd:.2f} / $0.10  -> {status}")

    return stop


if __name__ == "__main__":
    stop = main()
    # $0.12 spent exceeds the $0.10 cap, so the budget is exhausted with a
    # cost stop-reason: the run would refuse a 4th call rather than overspend.
    assert stop is not None, "budget should be exhausted"
    assert "cost" in str(stop).lower()
