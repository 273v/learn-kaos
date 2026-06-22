---
title: Can you depend on KAOS?
description: The public, evidence-backed signals for whether the kaos-* packages are safe to build on.
---

For a security or compliance reviewer, "is this safe to depend on?" needs evidence, not
assurances. The KAOS ecosystem publishes a continuous, evidence-backed answer.

## The compliance dashboard

`kaos-compliance` is a continuously-refreshed dashboard over every public `kaos-*` package,
anchored to industry frameworks — each signal links to a public source (a GitHub Actions
run, PyPI metadata, a sigstore log):

- **OpenSSF Scorecard** — the 19-check supply-chain baseline.
- **SLSA** — build provenance.
- **NIST SSDF (SP 800-218)** — the publicly-evidenceable secure-development subset.
- **CISA SBOM minimum elements** — supply-chain transparency.
- **PEP 740 + sigstore** — the PyPI attestation chain.
- **EU Cyber Resilience Act** — 2027 conformity readiness.

→ **Live dashboard:** <https://273v.github.io/kaos-compliance/>

## What it deliberately is not

- Not a substitute for your own audit, SOC 2, or ISO 27001.
- **Not a vanity score.** It does not invent a single "compliance score out of 100" —
  that pattern rewards gaming cheap signals over expensive ones. It reports the OpenSSF
  aggregate and surfaces the underlying evidence so you can judge for yourself.

## How this site reinforces it

The same honesty runs through these docs: every code sample is
[tested](/concepts/the-offline-seam), counts are generated not hand-typed, and the
limitations (cost gaps, `kaos-ml-core` v0, what a citation does *not* prove) are stated
plainly. Trust is built from verifiable claims, not adjectives.
