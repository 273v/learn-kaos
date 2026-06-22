---
title: Install
description: Install the one tool you need to run KAOS examples — uv — and verify your Python.
---

You need exactly **one** tool to run every example on this site: **[uv](https://docs.astral.sh/uv/)**,
the fast Python package manager. The examples are self-contained
[PEP 723](https://peps.python.org/pep-0723/) scripts that declare their own
dependencies, so `uv` resolves and runs them in an isolated, cached environment —
no manual virtualenv, no `pip install`.

## 1. Install uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify:

```bash
uv --version
```

## 2. Python

KAOS packages require **Python 3.13 or newer**. You don't need to install it
yourself — `uv` will fetch a matching interpreter on demand. To check what you
have:

```bash
uv python list
```

## 3. Run an example

That's the whole setup. Every example runs with one command:

```bash
uv run https://raw.githubusercontent.com/273v/learn-kaos/main/examples/citations-extract.py
```

…or, if you've cloned the repo:

```bash
uv run examples/citations-extract.py
```

The first run downloads dependencies (cached afterward), then prints the result.
Head to [your first example](/get-started/first-example) for the walkthrough.

:::tip[No API key needed]
Every example on the golden path runs **offline** — deterministic packages run as
themselves, and LLM examples use a built-in fake model. You only need a provider
API key for the optional *live* examples, which are clearly badged.
:::
