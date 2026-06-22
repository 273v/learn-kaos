---
title: Graph algorithms
description: The algorithms kaos-graph exposes, by category.
---

`kaos-graph` is a Rust (petgraph) engine with 40+ algorithms over a single `Graph`. Import
them from `kaos_graph.algorithms` (you used `pagerank` in
[build and rank a graph](/how-to/rank-a-graph)). Each takes the graph and returns typed
results.

## Traversal

`bfs` · `dfs` · `bfs_with_depth` · `bfs_at_depth` · `dfs_events`

## Paths

`shortest_paths` · `shortest_path_length` · `has_path` · `astar_path` ·
`bellman_ford_paths` · `all_simple_paths` · `longest_path`

## Cycles

`find_cycles` · `find_cycle_paths`

## Components & connectivity

`strongly_connected_components` · `weakly_connected_components` ·
`num_connected_components` · `connected_components_from_edges` ·
`is_strongly_connected` · `is_weakly_connected` · `condensation` ·
`articulation_points` · `bridges`

## Ordering & reachability

`topological_sort` · `ancestors` · `descendants` · `transitive_closure`

## Centrality

`pagerank` · `degree_centrality` · `in_degree_centrality` · `out_degree_centrality` ·
`betweenness_centrality` · `closeness_centrality` · `eigenvector_centrality`

## Communities & cliques

`louvain_communities` · `label_propagation` · `k_clique_communities` · `maximal_cliques`

## Matching & structure

`greedy_matching` · `maximum_matching` · `density` · `is_bipartite`

---

Beyond algorithms, `kaos-graph` includes an RDF/SPARQL layer (behind the `[rdf]` extra)
and knowledge-graph tooling. Run `kaos-graph --help` and see the
[package reference](/reference/packages).
