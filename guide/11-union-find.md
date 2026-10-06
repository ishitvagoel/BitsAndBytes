---
title: Union-find
slug: union-find
order: 11
status: present
module: bitsandbytes.union_find.disjoint_set, bitsandbytes.union_find.percolation
---

* `union_find/disjoint_set.py` — with and without union-by-rank and path compression.
* `union_find/percolation.py` — grid connectivity as a client.

## Industry

A working engineer uses a disjoint set when the only updates are merges and
the question is whether two items are already connected. Kruskal's minimum
spanning tree, which this course schedules after union-find, sorts the edges
and then unions endpoints that are still in different sets.
