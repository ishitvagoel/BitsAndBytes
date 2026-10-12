---
title: Shortest paths
slug: shortest-paths
order: 56
status: present
module: bitsandbytes.graphs.algorithms
---

## The idea

Dijkstra from A reports distance 3 at C, not the direct weight 4.

The shortest-path algorithm you want depends on the weights. Unweighted edges can use breadth-first search, because the fewest edges is the shortest path. Non-negative weights can use Dijkstra. On edges A to B weight 1, A to C weight 4, and B to C weight 2. Calling dijkstra_distances_heap from A gives C the distance 3. The direct edge is not the best path. Relaxation discovers this. When B is settled, the edge B to C offers 1 + 2, which beats 4.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Settle | distance = 0 | Settle A at distance 0. |
| Settle | distance = 1 | Settle B at distance 1. |
| Settle | distance = 3 | Settle C at distance 3. |

## Why it is correct

Relaxation keeps a tentative distance. An edge u to v of weight w improves v when distance u plus w is smaller than distance v. Breadth-first search is this rule with every weight equal to 1, and the queue order makes the first visit final. Dijkstra makes a visit final when the vertex is dequeued from a non-negative priority queue, because no later path can be cheaper. A negative edge breaks that proof. Bellman-Ford repeats relaxation once per vertex so a simple path has time to propagate. Floyd-Warshall tries every intermediate vertex for every pair. Kosaraju finds mutually reachable sets. It is not a shortest-path algorithm, and it belongs beside these tools because a negative cycle inside a component makes distances undefined.

## A common mistake

The first edge you see is not frozen. A later path can still improve the distance.

## What it costs

Bellman-Ford repeats relaxation so a negative edge can propagate, and it can report a negative cycle. Floyd-Warshall fills every pair. Use them when the weights are not the non-negative case above. The array-scan Dijkstra is proportional to vertices squared. The heap version is proportional to vertices plus edges, times a logarithm, when decrease-key is logarithmic. Bellman-Ford is vertices times edges. Floyd-Warshall is vertices cubed. Zero-one breadth-first search is linear in vertices plus edges when weights are only 0 and 1. Extra memory is the distance map. Pick the algorithm whose weight assumption you can actually state. Heap Dijkstra is O((V + E) log V) time and uses O(V) extra memory.

## Run it

```python
from bitsandbytes.graphs.adjacency_list import Graph
from bitsandbytes.graphs.algorithms import dijkstra_distances_heap
graph = Graph()
graph.add_edge('A', 'B', 1)
graph.add_edge('A', 'C', 4)
graph.add_edge('B', 'C', 2)
print(dijkstra_distances_heap(graph, 'A')['C'])
# prints: 3
```

## Practice and next step

Open Union-find next. Union-find answers whether two vertices are already connected before you add an edge.
