---
title: Shortest paths
slug: shortest-paths
order: 56
status: present
module: bitsandbytes.graphs.algorithms
---

## The idea

The shortest-path algorithm you want depends on the weights. Unweighted edges can use breadth-first search, because the fewest edges is the shortest path. Non-negative weights can use Dijkstra. Negative weights need Bellman-Ford, which also reports a negative cycle if you ask it to keep relaxing. On edges A to B weight 1, A to C weight 4, and B to C weight 2. Dijkstra_distances_heap from A gives C the distance 3. The direct edge is not the best path. Relaxation is the step that discovers this. When B's distance is final, the edge B to C offers 1 + 2, which beats 4. bellman_ford_distances on A to B weight 1 and B to C weight -2 gives C the distance -1. Dijkstra is not the right call once a weight can be negative. zero_one_bfs_distances on a path of two weight-1 edges gives C the distance 2. floyd_warshall on that path also gives A to C the distance 2, and it fills every pair. is_bipartite is true on the path and false on a directed triangle, which is an odd cycle. kosaraju_strongly_connected_components on that triangle returns one component containing A, C, and B.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Relax | distance = 3 | The path through B beats the direct edge into C. |

## Why it is correct

Relaxation keeps a tentative distance. An edge u to v of weight w improves v when distance u plus w is smaller than distance v. Breadth-first search is this rule with every weight equal to 1, and the queue order makes the first visit final. Dijkstra makes a visit final when the vertex is dequeued from a non-negative priority queue, because no later path can be cheaper. A negative edge breaks that proof. Bellman-Ford repeats relaxation once per vertex so a simple path has time to propagate. Floyd-Warshall tries every intermediate vertex for every pair. Kosaraju finds mutually reachable sets. It is not a shortest-path algorithm, and it belongs beside these tools because a negative cycle inside a component makes distances undefined.

## What it costs

The array-scan Dijkstra is proportional to vertices squared. The heap version is proportional to vertices plus edges, times a logarithm, when decrease-key is logarithmic. Bellman-Ford is vertices times edges. Floyd-Warshall is vertices cubed. Zero-one breadth-first search is linear in vertices plus edges when weights are only 0 and 1. Extra memory is the distance map. Pick the algorithm whose weight assumption you can actually state.

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

Answer the checkpoints, then open Union-find. The checkpoint stays in this browser.
