#!/usr/bin/env python3
"""kaos-learn — list and run the Learn KAOS examples by id.

The examples gallery manifest (examples/index.toml) is the single source
of truth. This launcher makes the samples discoverable and runnable with
one command, shelling out to `uv run` so each PEP 723 script resolves its
own dependencies.

    python3 scripts/kaos_learn.py list
    python3 scripts/kaos_learn.py run citations-extract

(Published later as a `uvx kaos-learn` console script; for now it's a
stdlib-only helper so it runs with no install.)
"""

from __future__ import annotations

import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "examples" / "index.toml"


def load() -> list[dict]:
    data = tomllib.loads(MANIFEST.read_text(encoding="utf-8"))
    return data.get("example", [])


def cmd_list() -> int:
    examples = load()
    width = max((len(e["id"]) for e in examples), default=0)
    for e in examples:
        flag = "offline" if e.get("offline_ok") else "needs-key"
        print(f"  {e['id']:<{width}}  [{flag:<9}] {e['summary']}")
    print(f"\n{len(examples)} example(s). Run one: kaos-learn run <id>")
    return 0


def cmd_run(example_id: str) -> int:
    ids = {e["id"] for e in load()}
    if example_id not in ids:
        print(f"unknown example {example_id!r}; try `kaos-learn list`", file=sys.stderr)
        return 2
    script = ROOT / "examples" / f"{example_id}.py"
    if not script.is_file():
        print(f"manifest lists {example_id!r} but {script} is missing", file=sys.stderr)
        return 1
    return subprocess.call(["uv", "run", str(script)])


def main(argv: list[str]) -> int:
    if len(argv) >= 1 and argv[0] == "list":
        return cmd_list()
    if len(argv) >= 2 and argv[0] == "run":
        return cmd_run(argv[1])
    print(__doc__)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
