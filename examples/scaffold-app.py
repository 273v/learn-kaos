#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-ui>=0.1.0a15,<0.2"]
# ///
"""The capstone: scaffold a full KAOS application.

`kaos-ui` generates production-shaped projects wired to the rest of KAOS. The
`web:spa` template is a complete app: a FastAPI backend on `kaos-agents` with
SSE streaming and bearer auth, plus a Vite + React frontend — Makefile, Docker,
Caddy, and pre-commit included.

This example uses **dry-run** mode, which reports exactly what *would* be written
without touching the filesystem — deterministic and offline. To actually create
the project, drop `dry_run=True` (or run `kaos-ui new web:spa my-app`).

Run it:

    uv run examples/scaffold-app.py
"""

from __future__ import annotations

import kaos_ui


def main() -> "kaos_ui.ScaffoldResult":
    result = kaos_ui.scaffold("web:spa", "my-legal-app", dry_run=True)

    files = sorted(str(f) for f in result.files)
    print(f"Template '{result.template}' would create {len(files)} files, including:\n")
    for f in files[:8]:
        print(f"  {f}")
    print("  ...")
    print(f"\nAvailable templates: {', '.join(kaos_ui.kinds())}")
    return result


if __name__ == "__main__":
    result = main()
    names = {str(f) for f in result.files}
    # A real, non-trivial project: backend + tooling are all present.
    assert len(result.files) >= 20, f"only {len(result.files)} files"
    assert "Makefile" in names and ".env.example" in names
    assert result.dry_run is True  # we wrote nothing to disk
