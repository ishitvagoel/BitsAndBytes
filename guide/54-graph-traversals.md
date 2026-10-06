---
title: Graph traversals
slug: graph-traversals
order: 54
status: present
module: bitsandbytes.graphs.algorithms
---

## Track discovered vertices

Depth-first search follows one branch before backtracking. Breadth-first search uses a FIFO queue and visits vertices in nondecreasing edge distance from the start in an unweighted graph. Mark a vertex discovered when it is added to the worklist so cycles do not enqueue it repeatedly.

## Trace a component

Starting from one vertex only reaches its connected component. To visit every component, scan all vertices and start a traversal at each still-unvisited one. With adjacency lists, each vertex and edge is processed O(1) times, for O(V + E) total work.

## Practice

Trace BFS and DFS on a cyclic graph. Record when each vertex becomes discovered and explain why marking on insertion prevents duplicate work.

Source: [`algorithms.py`](../bitsandbytes/graphs/algorithms.py).
