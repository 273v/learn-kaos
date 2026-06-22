#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-tabular>=0.1.3,<0.2"]
# ///
"""Run SQL analytics over tabular data — invoice/billing rollups, offline.

`kaos-tabular` is a DuckDB-powered engine: register a CSV / Parquet / JSON /
XLSX / SQLite file as a table, then run real SQL. This example rolls up legal
billing data by timekeeper — the kind of post-bill analytics a firm runs over
LEDES invoices, here on a tiny synthetic file.

Fully offline and deterministic — no key, no network.

Run it:

    uv run examples/sql-analytics.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import kaos_tabular as kt

INVOICES_CSV = """\
timekeeper,task_code,hours,amount
A. Partner,L120,3.5,1750
B. Associate,L120,8.0,2400
A. Partner,L160,2.0,1000
C. Paralegal,L140,5.0,750
B. Associate,L160,4.0,1200
"""


def main() -> list:
    with tempfile.TemporaryDirectory() as d:
        csv_path = Path(d) / "invoices.csv"
        csv_path.write_text(INVOICES_CSV, encoding="utf-8")

        engine = kt.TabularEngine()
        engine.register_file(csv_path, table_name="invoices")

        table = engine.execute(
            """
            SELECT timekeeper,
                   ROUND(SUM(hours), 1) AS total_hours,
                   SUM(amount)          AS total_billed
            FROM invoices
            GROUP BY timekeeper
            ORDER BY total_billed DESC
            """
        )
        print(f"{'timekeeper':<14} {'hours':>6} {'billed':>8}")
        for tk, hrs, amt in table.rows:
            print(f"{tk:<14} {hrs:>6} {amt:>8}")
        return list(table.rows)


if __name__ == "__main__":
    rows = main()
    # Deterministic rollup, ordered by amount: B. Associate bills the most
    # (12.0h / $3600), then A. Partner ($2750), then C. Paralegal ($750).
    assert rows[0][0] == "B. Associate" and rows[0][2] == 3600, rows[0]
    assert len(rows) == 3
