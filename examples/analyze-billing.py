#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-names>=0.1.0a5,<0.2", "kaos-tabular>=0.1.0,<0.2"]
# ///
"""Analyze a firm's billing — on synthetic data generated for the demo.

This is the post-bill analytics use case. It generates ~180 synthetic billing
line items (see generate-billing-data.py for the technique), loads them into
`kaos-tabular`'s DuckDB engine, and runs the rollups a billing partner actually
wants: spend by matter, blended rate by role, and spend by UTBMS task code.
Fully offline, deterministic, no model.

Run it:

    uv run examples/analyze-billing.py
"""

from __future__ import annotations

import csv
import hashlib
import random
import tempfile
from datetime import date, timedelta
from pathlib import Path

import kaos_names as kn
from kaos_tabular.engine import TabularEngine

TIMEKEEPERS = [
    ("Okafor", "Partner", 925), ("Nguyen", "Partner", 880),
    ("Alvarez", "Associate", 520), ("Brandt", "Associate", 470), ("Cohen", "Associate", 440),
    ("Devi", "Paralegal", 240), ("Eriksson", "Paralegal", 215),
]
TASKS = ["L120", "L160", "L210", "L240", "L320", "L330"]
PRACTICE_AREAS = ["Litigation", "M&A", "Employment", "Intellectual Property", "Regulatory"]


def generate_billing_rows(seed: int = 42, n: int = 180) -> list[dict]:
    mrng = random.Random(seed)
    matters = [
        {"matter": kn.generate_session_name(rng=mrng, number_min=2026, number_max=2026),
         "practice_area": mrng.choice(PRACTICE_AREAS)}
        for _ in range(6)
    ]
    base = date(2026, 1, 1)
    rows = []
    for i in range(n):
        digest = hashlib.blake2b(f"{seed}:{i}".encode(), digest_size=8).digest()
        rng = random.Random(int.from_bytes(digest, "big"))
        matter = rng.choice(matters)
        name, role, rate = rng.choice(TIMEKEEPERS)
        hours = round(rng.uniform(0.3, 8.0), 1)
        rows.append({
            "entry_id": f"E{i:04d}",
            "date": (base + timedelta(days=rng.randint(0, 89))).isoformat(),
            "matter": matter["matter"], "practice_area": matter["practice_area"],
            "timekeeper": name, "role": role, "task_code": rng.choice(TASKS),
            "hours": hours, "rate": rate, "amount": round(hours * rate, 2),
        })
    return rows


def write_csv(rows: list[dict]) -> Path:
    path = Path(tempfile.mkdtemp()) / "billing.csv"
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return path


def main():
    rows = generate_billing_rows()
    engine = TabularEngine()
    engine.register_file(write_csv(rows), table_name="billing")

    total_fees = sum(r["amount"] for r in rows)
    total_hours = sum(r["hours"] for r in rows)
    print(f"{len(rows)} entries  |  ${total_fees:,.0f} fees  |  "
          f"{total_hours:,.0f} hours  |  blended ${total_fees / total_hours:,.0f}/hr\n")

    # Top matters by spend.
    by_matter = engine.aggregate(
        "billing",
        aggregates=[("sum", "amount", "fees"), ("sum", "hours", "hrs")],
        group_by=["matter"], order_by=[("fees", "desc")], limit=5,
    )
    print("top matters by fees:")
    for matter, fees, hrs in by_matter.rows:
        print(f"  {matter:24} ${fees:>10,.0f}  ({hrs:>5,.0f} hrs)")

    # Blended rate by role.
    by_role = engine.aggregate(
        "billing",
        aggregates=[("sum", "amount", "fees"), ("sum", "hours", "hrs")],
        group_by=["role"], order_by=[("fees", "desc")],
    )
    print("\nrealized rate by role:")
    for role, fees, hrs in by_role.rows:
        print(f"  {role:12} ${fees:>10,.0f}  @ ${fees / hrs:>5,.0f}/hr")

    # Spend by UTBMS task code.
    by_task = engine.aggregate(
        "billing",
        aggregates=[("sum", "amount", "fees")],
        group_by=["task_code"], order_by=[("fees", "desc")],
    )
    print("\nspend by UTBMS task code:")
    for code, fees in by_task.rows:
        print(f"  {code}  ${fees:>10,.0f}")

    return by_matter, by_role, by_task


if __name__ == "__main__":
    by_matter, by_role, by_task = main()
    # The rollups are well-formed and complete.
    assert by_matter.row_count == 5
    assert {r[0] for r in by_role.rows} == {"Partner", "Associate", "Paralegal"}
    assert by_task.row_count == len(TASKS)
