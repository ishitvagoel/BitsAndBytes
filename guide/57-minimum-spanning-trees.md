---
title: Minimum spanning trees
slug: minimum-spanning-trees
order: 57
status: present
module: bitsandbytes.graphs.algorithms
---

## The idea

Weights 1, 2, and 4. Both algorithms return total weight 3 and reject 4.

A minimum spanning tree connects every vertex of an undirected weighted graph and has the smallest total edge weight. Prim and Kruskal both return 3 on the triangle A-B weight 1, B-C weight 2, and A-C weight 4. Kruskal sorts edges by weight and adds an edge when its ends lie in different components. The weight-4 edge finds A and C already connected through B, so the union-find cycle check rejects it. Prim grows one tree from A. It adds the cheapest edge that leaves the visited set. That is A-B, then B-C. The edge back to A is ignored because A is already visited. The two algorithms can pick different edges when weights tie. They do not pick different totals on this graph.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| take | total = 1 | Take weight 1. The total is 1. |
| take | total = 3 | Take weight 2. The total is 3. |
| reject | total = 3 | Reject weight 4. The total is 3. |

## Why it is correct

Kruskal's accepted edges never form a cycle because union refuses an edge whose ends already share a root. A set of n - 1 such edges on n vertices is a tree. It is spanning because every vertex in an edge was merged. The cut property says the cheapest edge leaving a set of visited vertices is safe to add. Prim always adds such an edge. Replacing it with a heavier edge across the same cut would not reduce the total. The rejected weight-4 edge is the unique heaviest edge on the only cycle, which is why both algorithms drop it.

## A common mistake

Adding the rejected edge closes the only cycle. A tree on n vertices has n - 1 edges.

## What it costs

Kruskal sorts the edges, which is E log E, and then runs a union-find almost-constant find per edge. Prim with a binary heap is proportional to vertices plus edges, times a log. Extra memory is the parent array or the heap, both linear in the vertices for a connected graph. Use either algorithm when the graph is undirected and you want a cheapest connection, not a shortest path from one source. Kruskal is O(E log E) time and uses O(V) extra memory.

## Run it

```python
from bitsandbytes.graphs.algorithms import UndirectedGraph, prim_minimum_spanning_weight
graph = UndirectedGraph()
graph.add_edge('A', 'B', 1)
graph.add_edge('B', 'C', 2)
graph.add_edge('A', 'C', 4)
print(prim_minimum_spanning_weight(graph, 'A'))
# prints: 3
```

## Practice and next step

Open Two-pointer patterns next. Two pointers scan a sorted array from both ends and move only one index at a time.
