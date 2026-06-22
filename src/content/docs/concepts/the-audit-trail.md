---
title: The audit trail
description: Why a KAOS agent keeps a durable, redacted record of what it did and why.
---

For agents doing legal and financial work, "what did it do, and why?" isn't a nice-to-have
— it's a requirement. KAOS agents keep an **audit trail**: a durable, secondary record of
the turn, captured from the same [event stream](/concepts/events-and-spans) that drives
the live response.

## A separate data plane

The audit trail is not the response and not the memory — it's a third thing, recorded
alongside them. As a turn runs, a recorder writes its events (tool calls, steps, citations,
usage, refusals, errors) to a structured, append-only log. Because it's derived from the
typed event stream, it captures the *reasoning shape* of the turn, not just the final text.

The kaos-agents examples ship an HTML viewer that renders these JSONL audit records — you
can replay exactly what the agent did, step by step.

## Built for trust, with redaction

Two properties make the audit trail safe to keep:

- **Redaction.** Secrets, credentials, and sensitive payloads are kept out of the record —
  the trail is designed to be retained and reviewed without leaking what shouldn't be in it.
- **Honest coverage.** Not every internal is captured, and the docs are candid about the
  gaps rather than implying total coverage. A trail you can trust is one whose limits are
  documented.

## Why it matters

- **Accountability.** You can answer "why did the agent cite this / call that tool / refuse
  here?" after the fact.
- **Debugging.** A failed or surprising turn can be replayed from its record instead of
  reproduced live.
- **Review.** Compliance and security reviewers get an evidence trail without having to
  instrument the agent themselves.

This is the same stance as the [refusal contract](/concepts/the-refusal-contract) and
[cost as a contract](/concepts/cost-as-a-contract): make the trustworthy thing structural,
observable, and honest about its limits.
