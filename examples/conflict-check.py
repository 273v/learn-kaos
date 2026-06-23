#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-nlp-core>=0.1.6,<0.2"]
# ///
"""Check new parties against a client list — fuzzy, for conflicts of interest.

Conflict checking has to catch *near* matches: "Acme Corporaton" (a typo) and
"Initech, LLC" (punctuation) must still hit "Acme Corporation" and "Initech LLC".
`kaos-nlp-core`'s `FstSet` builds a finite-state index of known names and does
edit-distance (`fuzzy_search`) and type-ahead (`prefix_search`) lookups — fast,
deterministic, offline, no model.

Run it:

    uv run examples/conflict-check.py
"""

from __future__ import annotations

from kaos_nlp_core.matching import FstSet

KNOWN_CLIENTS = [
    "Acme Corporation",
    "Globex Industries",
    "Initech LLC",
    "Wayne Enterprises",
]

# Names appearing on a new matter — some are the same parties, spelled loosely.
INCOMING = [
    "Acme Corporaton",     # typo -> Acme Corporation
    "globex industries",   # different case -> Globex Industries
    "Initech, LLC",        # punctuation -> Initech LLC
    "Stark Industries",    # genuinely new -> no conflict
]


def main() -> dict[str, str | None]:
    # Normalize case so a casing difference isn't counted as edits; keep a map
    # back to the canonical client name.
    canonical = {c.lower(): c for c in KNOWN_CLIENTS}
    index = FstSet(sorted(canonical))

    results: dict[str, str | None] = {}
    for name in INCOMING:
        hits = index.fuzzy_search(name.lower(), 2)  # within edit distance 2
        if hits:
            best = min(hits, key=lambda h: h.distance)
            match = canonical[best.key]
            print(f"  CONFLICT  {name!r:22} ~ {match!r} (distance {best.distance})")
            results[name] = match
        else:
            print(f"  clear     {name!r:22} (no known client within distance 2)")
            results[name] = None
    return results


if __name__ == "__main__":
    results = main()
    # The three variants resolve to known clients; the genuinely new party is clear.
    assert results["Acme Corporaton"] == "Acme Corporation"
    assert results["globex industries"] == "Globex Industries"
    assert results["Initech, LLC"] == "Initech LLC"
    assert results["Stark Industries"] is None
