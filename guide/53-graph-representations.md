---
title: Graph representations
slug: graph-representations
order: 53
status: present
module: bitsandbytes.graphs.adjacency_list
---

## The idea

A graph can be stored as an adjacency list or as a matrix. The library Graph is a dictionary from each vertex to a list of neighbor and weight pairs. Add A to B, A to C, and B to D. The graph has 4 vertices and 3 outgoing pairs. A matrix for the same vertices has 16 cells, one for every ordered pair, almost all of them empty. The list stores only the edges you added. A sparse graph is one where the edge count is much smaller than the square of the vertex count. Breadth-first search on that shape should use a queue with constant-time ends. Python's collections.deque is the usual choice. The library's own breadth-first search uses its linked queue for the same reason. Scanning a matrix row to find neighbors costs a full vertex scan even when a vertex has one edge.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Edges | vertices = 4 | Three adjacency-list pairs store this graph. |

## Why it is correct

The list answers 'who are my neighbors' by reading one list. The matrix answers the same question by scanning a row. Both can answer 'is there an edge from u to v', and the matrix does it in constant time while the list scans u's neighbors. Space follows the same split. The list is proportional to vertices plus edges. The matrix is proportional to vertices squared, whether or not the edges exist. Choose the representation for the operation you repeat, not for the picture you draw.

## What it costs

Building the list is proportional to the number of edges. A traversal that walks each list once is proportional to vertices plus edges. The same traversal on a matrix is proportional to vertices squared. Extra memory for the search is still the queue or the stack, proportional to the vertices. Use a matrix only when the graph is dense or you need constant-time edge tests in the inner loop.

## Run it

```python
from bitsandbytes.graphs.adjacency_list import Graph
graph = Graph()
graph.add_edge('A', 'B', 1)
graph.add_edge('A', 'C', 1)
graph.add_edge('B', 'D', 1)
print(sum(len(graph.neighbors(vertex)) for vertex in graph.vertices()))
# prints: 3
```

## Practice and next step

Answer the checkpoint on this page, then use Next for the following lesson. The checkpoint stays in this browser.
