---
title: Approximation guarantees
slug: approximation-guarantees
order: 69
status: present
module: bitsandbytes.limits.approximation
---

## The idea

Two disjoint edges produce a cover of 4 endpoints. An optimum cover has size 2.

Some problems have no known exact algorithm that is fast on every input. An approximation algorithm returns a legal answer whose cost is provably close to the best cost. vertex_cover_two_approximation scans edges and, when neither endpoint is already chosen, adds both. On a graph with only the edges A-B and C-D, the cover is the set A, B, C, D. The cover is feasible because every edge has both ends selected, so it certainly has one. An optimum cover can pick one end from each edge, so its size is 2. The algorithm returned 4, which is twice the optimum. The proof is the pairing. Each time the algorithm adds two vertices, it does so for an edge whose ends were both still free. Those edges do not share vertices. Any cover must pick at least one vertex from each such edge. The algorithm picked two. The ratio is therefore at most 2 on every graph, not only on this one.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| start | cover = [] | The cover starts empty. No edge has been scanned. |
| pair | cover = ['A', 'B'] | The edge A to B adds both ends. |
| pair | cover = ['A', 'B', 'C', 'D'] | The edge C to D adds both ends. |

## Why it is correct

Feasibility is the first half. Every edge is either selected as a pair or already touched by an earlier pair, so no edge is left uncovered. The ratio is the second half. Let the selected edges be the ones that contributed a pair. They are vertex-disjoint, so the optimum is at least the number of those edges. The algorithm's cover has two vertices per selected edge, plus nothing else from this rule. Twice the optimum is therefore an upper bound on the size of the cover. A single example that happens to be close is not this proof. The proof counts the disjoint edges.

## A common mistake

A cover that happens to look small on one graph is not the ratio proof.

## What it costs

The scan looks at each adjacency-list entry once, so the time is proportional to vertices plus edges. Extra memory is the cover set, which is at most the vertices. The guarantee does not say the cover is the smallest possible. It says you can bound how far it is from the smallest. Use that bound when an exact cover would require a search you cannot afford. The scan is Θ(V + E) time, and the cover uses O(V) extra memory.

## Run it

```python
from bitsandbytes.limits.approximation import vertex_cover_two_approximation
from bitsandbytes.graphs.adjacency_list import Graph
graph = Graph()
graph.add_edge('A', 'B', 1)
graph.add_edge('C', 'D', 1)
print(sorted(vertex_cover_two_approximation(graph)))
# prints: ['A', 'B', 'C', 'D']
```

## Practice and next step

Open Analysis and library costs next.
