---
title: Directed acyclic graphs and topological order
slug: topological-order
order: 55
status: present
module: bitsandbytes.graphs.algorithms
---

## The idea

A topological order is a list of the vertices of a directed graph such that every edge points forward in the list. topological_order on edges A to B, A to C, B to D, and C to D returns A, B, C, D. Kahn's algorithm computes an indegree for each vertex. It starts a queue with every vertex whose indegree is zero. A is the only such vertex here. When a vertex leaves the queue, each outgoing edge reduces a neighbor's indegree. A neighbor enters the queue when its indegree hits zero. B and C both become ready after A, and D waits until both of its incoming edges have been counted. has_directed_cycle on this graph is false. On a two-cycle from A to B and back, it is true, and topological_order raises ValueError. Because the queue runs dry before every vertex has been emitted.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Order | start = A | Kahn's algorithm emits every vertex once. |

## Why it is correct

A vertex enters the queue only when every predecessor has already been emitted. Every edge out of an emitted vertex has been relaxed, so a later position cannot be a predecessor of an earlier one. If the graph has a cycle, some vertex on the cycle always has indegree left, because its predecessor on the cycle was never emitted. The queue empties and the output is shorter than the vertex list. That length check is the cycle test inside this function. A depth-first version records a vertex after its descendants and reverses that finish order. Both reject a back edge.

## What it costs

Each vertex is enqueued once and each edge is inspected once, so the time is proportional to vertices plus edges. Extra memory is the indegree map and the queue, proportional to the vertices. Use this order before dynamic programming on a dag, and before scheduling jobs that depend on other jobs. Do not call it on a graph that might contain a cycle unless you catch the error.

## Run it

```python
from bitsandbytes.graphs.adjacency_list import Graph
from bitsandbytes.graphs.algorithms import topological_order
graph = Graph()
graph.add_edge('A', 'B', 1)
graph.add_edge('A', 'C', 1)
graph.add_edge('B', 'D', 1)
graph.add_edge('C', 'D', 1)
print(topological_order(graph))
# prints: ['A', 'B', 'C', 'D']
```

## Practice and next step

Answer the checkpoints, then open Shortest paths. The checkpoint stays in this browser.
