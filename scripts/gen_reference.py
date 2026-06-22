#!/usr/bin/env python3
"""reference-gen: regenerate the generated Reference pages from source-of-truth.

Per LEARN_KAOS_PLAN.md, every tool/CLI/env-var/count on the Reference
pages is GENERATED, never hand-typed — so the docs cannot drift from the
packages. CI runs this and fails if the committed output is stale
(see .github/workflows/ci.yml `reference-gen`).

M0: no Reference pages exist yet, so this is a structural no-op that
exits 0. The generators (from each package's `inventory.py`, `--help`,
and `ModuleSettings`, plus `kaos-modules/scripts/status.py`) land in M1.8.

Usage: python3 scripts/gen_reference.py [--check]
  (--check is informational here; M0 generates nothing.)
"""

from __future__ import annotations

import sys

# TODO(M1.8): generate
#   reference/mcp-tools  <- each package's scripts/inventory.py
#   reference/cli        <- each `kaos-* --help`
#   reference/env-vars   <- each ModuleSettings subclass
#   reference/compatibility / package counts <- kaos-modules/scripts/status.py
GENERATORS: list = []


def main() -> int:
    if not GENERATORS:
        print("reference-gen: nothing to generate yet (M0); landing in M1.8.")
        return 0
    # M1.8 will run each generator and the CI job will `git diff --exit-code`.
    for gen in GENERATORS:  # pragma: no cover - placeholder
        gen()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
