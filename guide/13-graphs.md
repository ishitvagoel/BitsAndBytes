---
title: Graphs
slug: graphs
order: 13
status: present
module: bitsandbytes.graphs.adjacency_list, bitsandbytes.graphs.algorithms
---

* `graphs/adjacency_list.py` — adjacency lists. DFS and BFS are O(V + E). The teaching `dijkstra_distances` scans all unsettled vertices each step, so O(V²) time on dense graphs.
* `graphs/algorithms.py` — BFS distances, topological sort, cycle detection, Kosaraju SCCs, Bellman-Ford, heap Dijkstra, Kruskal, Prim, 0-1 BFS, Floyd-Warshall, bipartite test.
