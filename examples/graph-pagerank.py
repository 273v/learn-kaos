#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-graph>=0.1.4,<0.2"]
# ///
"""Build a tiny directed graph and rank its nodes with PageRank.

Fully offline and deterministic — `kaos-graph` is a Rust (petgraph)
engine behind a thin Python API, so ranks are byte-for-byte stable.

Run it:

    uv run examples/graph-pagerank.py
"""

from __future__ import annotations

import kaos_graph as kg
from kaos_graph.algorithms import pagerank


def build() -> kg.Graph:
    g = kg.Graph()
    for node in ("a", "b", "c"):
        g.add_node(node)
    # a -> b -> c -> a, plus a -> c (so c is pointed at twice)
    g.add_edge("a", "b")
    g.add_edge("b", "c")
    g.add_edge("c", "a")
    g.add_edge("a", "c")
    return g


def main() -> list:
    g = build()
    ranks = pagerank(g)  # list[NodeRank(node_id, score)], highest first
    print("PageRank (highest first):\n")
    for r in ranks:
        print(f"  {r.node_id}  {r.score:.3f}")
    return ranks


if __name__ == "__main__":
    result = main()
    # Self-check: 'c' has two in-edges, so it ranks first.
    assert result[0].node_id == "c", f"expected 'c' on top, got {result[0].node_id!r}"
