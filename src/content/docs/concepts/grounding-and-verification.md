---
title: Grounding & verification
description: What a verified citation proves — and, just as importantly, what it does not.
---

A [grounded citation](/tutorials/grounded-citations) is a claim paired with a **span** — a
quote and its location in a source — that is **checked against that source**. It's the
mechanism behind trustworthy answers. But it's important to be precise about what it does
and doesn't guarantee.

## What verification proves

- **The quote exists in the source.** `Span.verify(source)` confirms the cited text really
  appears where the claim says it does. A fabricated quote fails.
- **The answer is anchored.** With `Cited[T]`, a whole structured answer's spans can be
  validated against a corpus at once (`validate_cited_output`).

## What it does NOT prove

- **It is not paraphrase-checking.** Verification checks that a *quote* is present — not
  that the model's surrounding interpretation of that quote is correct. Ground in quotes,
  not summaries.
- **It is not retrieval correctness.** Verification confirms the cited source says what's
  quoted; it doesn't prove that source was the *right* one to consult. Retrieval quality
  (BM25, the corpus) is a separate concern.

## Why the distinction matters

Overclaiming what a citation proves is its own failure mode. KAOS's contract is narrow and
honest: *the quote is really there, or the claim is rejected*. That narrowness is what
makes it reliable — paired with the [refusal contract](/concepts/the-refusal-contract),
the agent quotes-or-refuses rather than paraphrases-and-hopes.
