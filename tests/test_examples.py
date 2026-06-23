"""snippets-test: every offline example in the manifest must run green.

Runs each `offline_ok` example via `uv run` (so PEP 723 deps resolve) and
asserts a zero exit and an expected marker in its output. This is the
"tested snippets" guarantee for the gallery: if an example breaks against
the published packages, CI goes red.

Live (`needs_key`) examples are skipped here and covered only on the
opt-in live path (KAOS_LEARN_LIVE=1), never in offline CI.

Run:  uv run --with pytest pytest tests/ -q
"""

from __future__ import annotations

import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "examples" / "index.toml"

# Expected stdout marker per example id (acceptance criteria).
EXPECTED: dict[str, str] = {
    "citations-extract": "347 U.S. 483 (1954)",
    "graph-pagerank": "PageRank (highest first):",
    "first-tool": "word count: 5",
    "build-a-document": "# Lease Agreement",
    "functionclient-chat": "FAKE MODEL SAYS: HELLO, KAOS",
    "typed-call-offline": "parties: ['Acme Corp', 'Globex LLC']",
    "bm25-search": "Rent is due monthly",
    "names-seeded": "silky-commissioner-04",
    "first-agent": "2 user message(s) of history",
    "scaffold-app": "Template 'web:spa' would create",
    "grounded-citations": "REJECTED",
    "sql-analytics": "B. Associate",
    "contract-definitions": "Confidential Information",
    "provider-failover": "answered by the backup provider",
    "office-roundtrip": "Net 30 from invoice.",
    "research-over-corpus": "GROUNDED:",
    "pdf-extract": "retainer is twenty thousand",
    "web-extract": "arbitration clause",
    "embeddings": "256-dim vectors",
    "near-duplicates": "0.812",
    "agent-permissions": "deny",
    "typed-settings": "overriding default 10",
    "email-forensics": "Re: Merger Agreement",
    "knowledge-graph": "parties to Case1: ['Acme', 'Globex']",
    "serve-over-mcp": "would expose over MCP",
    "cluster-documents": "document -> cluster:",
    "research-agent": "[Verified: 1 claim(s), 1 citation(s)]",
    "agent-delegation": "DRAFT: Memo to counsel",
    "optimize-program": "validation metric before",
    "pause-resume": "awaiting approval",
    "export-otel": "agent.turn",
    "cap-cost": "budget_cost",
    "add-template-kind": "report:latex",
    "findings-review": "survived filtering",
    "uc-litigation-triage": "complaint",
    "uc-billing-utbms": "L120",
    "uc-matter-tagging": "M&A",
    "uc-complaint-extract": "Globex Financial",
    "uc-contract-abstract": "Delaware",
    "uc-credit-covenants": "leverage ratio",
    "uc-s1-deal-terms": "ACME",
    "uc-expertise-extract": "Private Equity",
    "uc-regulatory-monitoring": "RELEVANT",
    "uc-matter-pricing": "complexity:",
}

_examples = tomllib.loads(MANIFEST.read_text(encoding="utf-8")).get("example", [])
_offline = [e for e in _examples if e.get("offline_ok")]


@pytest.mark.parametrize("example", _offline, ids=[e["id"] for e in _offline])
def test_offline_example_runs(example: dict) -> None:
    script = ROOT / "examples" / f"{example['id']}.py"
    assert script.is_file(), f"manifest lists {example['id']} but {script} is missing"

    proc = subprocess.run(
        ["uv", "run", str(script)],
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert proc.returncode == 0, f"{script.name} exited {proc.returncode}\n{proc.stderr}"

    marker = EXPECTED.get(example["id"])
    if marker is not None:
        assert marker in proc.stdout, (
            f"{script.name} stdout missing expected marker {marker!r}\n{proc.stdout}"
        )


def test_every_offline_example_has_expected_marker() -> None:
    """Guard: don't add an offline example without an acceptance marker."""
    missing = [e["id"] for e in _offline if e["id"] not in EXPECTED]
    assert not missing, f"offline examples without an EXPECTED marker: {missing}"


def test_manifest_files_exist() -> None:
    for e in _examples:
        assert (ROOT / "examples" / f"{e['id']}.py").is_file(), e["id"]


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
