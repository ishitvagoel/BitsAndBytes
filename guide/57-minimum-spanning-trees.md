---
title: Minimum spanning trees
slug: minimum-spanning-trees
order: 57
status: present
module: bitsandbytes.graphs.algorithms
---

## Connect every vertex at minimum total edge weight

A spanning tree of a connected undirected graph has V−1 edges and no cycle. Kruskal's algorithm sorts edges by weight and adds an edge only when its endpoints belong to different components; disjoint-set union detects whether it would close a cycle.

## State the graph assumptions

For disconnected input, Kruskal produces a minimum spanning forest. With sorting plus path-compressed, size-balanced union-find, the dominant cost is O(E log E). Equal weights can yield more than one minimum spanning tree.

## Practice

Process edges from lightest to heaviest. For each edge, record whether it joins two components or would form a cycle, then verify the final edge count.

Source: [`algorithms.py`](../bitsandbytes/graphs/algorithms.py).
