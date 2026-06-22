#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-names>=0.1.0a5,<0.2"]
# ///
"""Generate friendly, legal-flavored handles for sessions and agents.

`kaos-names` produces readable identifiers like `silky-commissioner-04` —
nicer than a UUID in logs and UIs. Pass a seeded `random.Random` and the
output is fully deterministic, which is exactly what you want in tests.

Run it:

    uv run examples/names-seeded.py
"""

from __future__ import annotations

import random

from kaos_names import generate_name


def main() -> tuple[str, str]:
    # A fresh, random handle (different every run):
    print(f"random handle:     {generate_name()}")

    # A *deterministic* handle — same seed, same name, every time:
    seeded = generate_name(rng=random.Random(42))
    print(f"seeded(42) handle: {seeded}")
    again = generate_name(rng=random.Random(42))
    print(f"seeded(42) again:  {again}")

    return seeded, again


if __name__ == "__main__":
    seeded, again = main()
    # Determinism is the testable property: same seed -> same handle.
    assert seeded == again == "silky-commissioner-04", seeded
