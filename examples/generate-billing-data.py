#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-names>=0.1.0a5,<0.2"]
# ///
"""Generate synthetic billing data — realistic, labeled, and reproducible.

You can't demo a billing workflow on a real firm's invoices, and you can't test
one without data. So generate it. Following the pattern KAOS uses to build
training corpora (`kaos-embeddings`), this seeds a per-row RNG from a stable hash
(BLAKE2b) so every row is *independently reproducible* — same seed in, identical
dataset out, regardless of order or parallelism. Matter codenames come from
`kaos-names` (its noun pool is legal terms).

This is the synthetic-data-generation use case; `analyze-billing.py` consumes the
output. Fully offline, no model.

Run it:

    uv run examples/generate-billing-data.py
"""

from __future__ import annotations

import hashlib
import random
from datetime import date, timedelta

import kaos_names as kn

# Fixed pools — a real generator would draw these from config.
TIMEKEEPERS = [
    ("Okafor", "Partner", 925), ("Nguyen", "Partner", 880),
    ("Alvarez", "Associate", 520), ("Brandt", "Associate", 470), ("Cohen", "Associate", 440),
    ("Devi", "Paralegal", 240), ("Eriksson", "Paralegal", 215),
]
TASKS = [  # UTBMS litigation task codes + narrative templates
    ("L120", ["Analyze case strategy and key issues", "Develop litigation strategy"]),
    ("L160", ["Confer with client regarding settlement posture", "Draft settlement demand letter"]),
    ("L210", ["Draft motion to dismiss", "Revise answer and affirmative defenses"]),
    ("L240", ["Draft motion for summary judgment", "Research summary judgment standard"]),
    ("L320", ["Review documents produced in discovery", "Prepare privilege log entries"]),
    ("L330", ["Prepare for deposition of fact witness", "Attend and defend deposition"]),
]
PRACTICE_AREAS = ["Litigation", "M&A", "Employment", "Intellectual Property", "Regulatory"]
CLIENTS = ["Acme Corporation", "Globex Industries", "Initech LLC", "Wayne Enterprises"]


def _matters(seed: int, n: int = 6) -> list[dict]:
    rng = random.Random(seed)
    out = []
    for i in range(n):
        codename = kn.generate_session_name(rng=rng, number_min=2026, number_max=2026)
        out.append({
            "matter": f"{codename}",
            "practice_area": rng.choice(PRACTICE_AREAS),
            "client": rng.choice(CLIENTS),
        })
    return out


def generate_billing_rows(seed: int = 42, n: int = 180) -> list[dict]:
    """Generate `n` billing line items. Each row is seeded independently from a
    BLAKE2b hash of (seed, index), so the dataset is fully reproducible."""
    matters = _matters(seed)
    base = date(2026, 1, 1)
    rows = []
    for i in range(n):
        digest = hashlib.blake2b(f"{seed}:{i}".encode(), digest_size=8).digest()
        rng = random.Random(int.from_bytes(digest, "big"))

        matter = rng.choice(matters)
        name, role, rate = rng.choice(TIMEKEEPERS)
        code, narratives = rng.choice(TASKS)
        hours = round(rng.uniform(0.3, 8.0), 1)
        rows.append({
            "entry_id": f"E{i:04d}",
            "date": (base + timedelta(days=rng.randint(0, 89))).isoformat(),
            "matter": matter["matter"],
            "practice_area": matter["practice_area"],
            "client": matter["client"],
            "timekeeper": name,
            "role": role,
            "task_code": code,
            "narrative": rng.choice(narratives),
            "hours": hours,
            "rate": rate,
            "amount": round(hours * rate, 2),
        })
    return rows


def main() -> list[dict]:
    rows = generate_billing_rows()
    total = sum(r["amount"] for r in rows)
    matters = {r["matter"] for r in rows}
    print(f"generated {len(rows)} billing entries across {len(matters)} matters")
    print(f"  date range: {min(r['date'] for r in rows)} .. {max(r['date'] for r in rows)}")
    print(f"  total fees: ${total:,.2f}")
    print(f"  total hours: {sum(r['hours'] for r in rows):,.1f}")
    print("\nsample rows:")
    for r in rows[:3]:
        print(f"  {r['date']}  {r['timekeeper']:9} {r['task_code']}  {r['hours']:>4}h  ${r['amount']:>9,.2f}  {r['matter']}")
    return rows


if __name__ == "__main__":
    rows = main()
    assert 100 <= len(rows) <= 200
    # Reproducible: regenerating with the same seed yields an identical dataset.
    assert generate_billing_rows() == rows
    # ...and a different seed yields a different one.
    assert generate_billing_rows(seed=7) != rows
