#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["kaos-graph[rdf]>=0.1.4,<0.2"]
# ///
"""Query a legal knowledge graph with SPARQL.

`kaos-graph` loads RDF and answers SPARQL — the basis of KAOS's per-session
knowledge graphs (parties, cases, citations, counsel as a graph you can query).
Here we load a tiny legal graph from Turtle and run SPARQL queries over it.
Fully offline and deterministic.

Run it:

    uv run examples/knowledge-graph.py
"""

from __future__ import annotations

from kaos_graph.rdf import load_rdf
from kaos_graph.rdf.sparql import query_sparql

TURTLE = """
@prefix ex: <http://example.org/> .

ex:Smith   ex:counselFor ex:Acme .
ex:Acme    ex:partyTo    ex:Case1 .
ex:Globex  ex:partyTo    ex:Case1 .
ex:Case1   ex:cites      ex:Brown .
ex:Case1   ex:cites      ex:Roe .
"""


def main() -> tuple[list[str], list[str]]:
    graph, stats = load_rdf(TURTLE, "turtle")
    print(f"loaded {stats.total_triples} triples ({stats.nodes} nodes)\n")

    # Who are the parties to Case1?  (ORDER BY makes the result deterministic.)
    parties = query_sparql(
        graph,
        "PREFIX ex: <http://example.org/> "
        "SELECT ?p WHERE { ?p ex:partyTo ex:Case1 } ORDER BY ?p",
    )
    party_names = [r["p"].rsplit("/", 1)[-1] for r in parties.rows]
    print(f"  parties to Case1: {party_names}")

    # What does Case1 cite?
    cites = query_sparql(
        graph,
        "PREFIX ex: <http://example.org/> "
        "SELECT ?c WHERE { ex:Case1 ex:cites ?c } ORDER BY ?c",
    )
    cited = [r["c"].rsplit("/", 1)[-1] for r in cites.rows]
    print(f"  Case1 cites:      {cited}")

    return party_names, cited


if __name__ == "__main__":
    parties, cited = main()
    assert parties == ["Acme", "Globex"]
    assert cited == ["Brown", "Roe"]
