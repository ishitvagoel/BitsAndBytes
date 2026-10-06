---
title: Graph representations
slug: graph-representations
order: 53
status: present
module: bitsandbytes.graphs.adjacency_list
---

## Choose a representation from the operations

A graph has vertices and edges. An adjacency list stores, for each vertex, the vertices it connects to. It uses O(V + E) space and lets a traversal visit the graph in O(V + E). An adjacency matrix uses O(V²) space but answers whether an edge exists in O(1).

## Keep direction and weight explicit

For an undirected edge, add each endpoint to the other's neighbor list. A directed edge appears only in its source's list. Weighted edges store a neighbor and a weight together. Confusing direction or adding an undirected edge twice changes the represented problem.

## Practice

Draw an adjacency list and matrix for a four-vertex graph. Count the space each uses and decide which representation fits repeated edge-existence queries.

Source: [`adjacency_list.py`](../bitsandbytes/graphs/adjacency_list.py).
