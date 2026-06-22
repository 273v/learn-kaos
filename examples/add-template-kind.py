#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-ui>=0.1.0a15,<0.2"]
# ///
"""Extend the scaffolder with your own template kind.

`kaos-ui` ships six template kinds, but it's an extension point: register a
`TemplateManifest` and your kind becomes available to the CLI *and* to the MCP
tools automatically — the registry is the single source of truth. Here we add a
custom kind and confirm it shows up.

Fully offline and deterministic.

Run it:

    uv run examples/add-template-kind.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import kaos_ui


def main() -> list[str]:
    before = set(kaos_ui.kinds())

    with tempfile.TemporaryDirectory() as d:
        # A real template would have files in this dir; empty is fine to register.
        template_dir = Path(d)

        kaos_ui.register_template(
            kaos_ui.TemplateManifest(
                kind="report:latex",
                description="A LaTeX report generator wired to KAOS extraction.",
                stack="Python + LaTeX",
                template_dir=template_dir,
                required_env=(),
                post_install=("make install",),
                next_steps=("Edit report.tex", "make pdf"),
            )
        )

        kinds = kaos_ui.kinds()
        new = sorted(set(kinds) - before)
        print(f"registered new kind(s): {new}")
        print(f"all kinds now: {sorted(kinds)}")

        manifest = kaos_ui.get_manifest("report:latex")
        print(f"  report:latex -> {manifest.description}")
        return sorted(kinds)


if __name__ == "__main__":
    kinds = main()
    assert "report:latex" in kinds, "the new kind should be registered"
    # The built-ins are still there too.
    assert "web:spa" in kinds and "module" in kinds
