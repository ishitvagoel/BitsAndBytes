---
title: Directed acyclic graphs and topological order
slug: topological-order
order: 55
status: present
module: bitsandbytes.graphs.algorithms
---

## Respect every dependency edge

A topological ordering places each vertex before all vertices it points to. It exists exactly when the directed graph has no cycle. Kahn's algorithm repeatedly removes a zero-indegree vertex and reduces the indegree of its outgoing neighbors.

## Detect a cycle by the remaining count

If fewer than V vertices are removed, the remaining subgraph has no zero-indegree vertex and contains a directed cycle. Different valid choices among zero-indegree vertices can produce different valid orderings.

## Practice

Given course prerequisites as directed edges, compute indegrees, trace the queue, and decide whether a full schedule exists.

Source: [`algorithms.py`](../bitsandbytes/graphs/algorithms.py).
