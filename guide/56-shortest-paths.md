---
title: Shortest paths
slug: shortest-paths
order: 56
status: present
module: bitsandbytes.graphs.algorithms
---

## Match the algorithm to edge weights

BFS gives shortest edge-count paths when all edges have equal weight. Dijkstra's algorithm handles nonnegative weights by repeatedly finalizing the unsettled vertex with smallest tentative distance. Negative edges break that greedy guarantee.

## Account for the implementation

Relax an edge u→v when dist[u] + weight improves dist[v]. A binary heap with lazy duplicate entries gives O((V + E) log V) in the usual adjacency-list implementation. This repository's teaching version scans all unsettled vertices at each step, so its Dijkstra routine is O(V²); describe the code that exists, not an imagined heap implementation.

## Practice

Trace relaxations on a weighted graph. Explain why the first discovered route to a vertex need not be its shortest route.

Source: [`algorithms.py`](../bitsandbytes/graphs/algorithms.py).
