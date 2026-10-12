---
title: Graph traversals
slug: graph-traversals
order: 54
status: present
module: bitsandbytes.graphs.algorithms
---

## The idea

Breadth-first search from A on edges to B, C, and D visits A, B, C, D.

Breadth-first search uses a queue. Depth-first search uses a stack, or the call stack. Both mark a vertex when they first discover it so an edge back to a visited vertex does not enqueue it again. On the directed graph A→B, A→C, B→D, breadth-first order from A is A, B, C, D. B and C are both neighbors of A, and B is enqueued first because it is the first edge. D is discovered from B, so it waits behind C. The library function breadth_first_order returns that list.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| enqueue | vertex = A | The search marks A during enqueue. |
| dequeue | vertex = A | The search marks A during dequeue. |
| enqueue | vertex = B | The search marks B during enqueue. |
| enqueue | vertex = C | The search marks C during enqueue. |
| dequeue | vertex = B | The search marks B during dequeue. |
| enqueue | vertex = D | The search marks D during enqueue. |
| dequeue | vertex = C | The search marks C during dequeue. |
| dequeue | vertex = D | The search marks D during dequeue. |

## Why it is correct

The queue's FIFO order is the reason BFS visits vertices in order of distance from the start. When A is dequeued, its neighbors are one edge away and they enter the queue together. The next dequeues are those neighbors, and their new neighbors are two edges away. A vertex is marked visited when it is enqueued, not when it is dequeued. A later edge cannot place it in the queue a second time. DFS would push neighbors on a stack and could visit D before C, because the most recently pushed neighbor is popped first.

## A common mistake

A stack visits a different order. The container chooses the visit order.

## What it costs

Each vertex is enqueued once and each edge is inspected once. The time is Θ(V + E) for the vertices and edges reachable from the start. The queue holds at most V vertices, so extra memory is Θ(V). An adjacency matrix would make the neighbor scan Θ(V) per vertex even when the graph is sparse, which is Θ(V²). The adjacency list is why the bound can mention E.

The same graph searched depth-first from A can visit D before C, because D is pushed after C and a stack pops D first. If your test expected BFS order and the code used a stack, this is the mismatch. The container is the algorithm.

## Run it

```python
from bitsandbytes.graphs.adjacency_list import Graph, breadth_first_order
graph = Graph()
graph.add_edge('A', 'B', 1)
graph.add_edge('A', 'C', 1)
graph.add_edge('B', 'D', 1)
print(breadth_first_order(graph, 'A'))
# prints: ['A', 'B', 'C', 'D']
```

## Practice and next step

Open Directed acyclic graphs and topological order next. Topological order needs a directed acyclic graph and emits sources first.
