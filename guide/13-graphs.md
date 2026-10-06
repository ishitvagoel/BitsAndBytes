---
title: Graphs
slug: graphs
order: 13
status: present
module: bitsandbytes.graphs.adjacency_list, bitsandbytes.graphs.algorithms
---

* `graphs/adjacency_list.py` — adjacency lists. DFS and BFS are O(V + E). The teaching `dijkstra_distances` scans all unsettled vertices each step, so O(V²) time on dense graphs.

## Focused lessons

- [Graph representations](./53-graph-representations.md)
- [Graph traversals](./54-graph-traversals.md)
- [Directed acyclic graphs and topological order](./55-topological-order.md)
- [Shortest paths](./56-shortest-paths.md)
- [Minimum spanning trees](./57-minimum-spanning-trees.md)
* `graphs/algorithms.py` — BFS distances, topological sort, cycle detection, Kosaraju SCCs, Bellman-Ford, heap Dijkstra, Kruskal, Prim, 0-1 BFS, Floyd-Warshall, bipartite test.

## Industry

A working engineer stores a sparse graph as adjacency lists and searches
with the structure the weights require. Unweighted breadth-first search uses
`collections.deque`, which Python documents with approximately O(1) appends
and pops at either end. Non-negative weights use `heapq`, the min-heap whose
smallest item is the root. The adjacency-list scan is the Dijkstra that heap replaces.
