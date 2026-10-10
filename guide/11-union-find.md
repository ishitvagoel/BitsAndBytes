---
title: Union-find
slug: union-find
order: 11
status: present
module: bitsandbytes.union_find.disjoint_set, bitsandbytes.union_find.percolation
---

## The idea

A disjoint-set forest tracks which items are in the same set. Each item stores a parent. The root is the item whose parent is itself, and it names the set. find walks parents to the root. union merges two sets by pointing one root at the other. Without heuristics, union(0, 1) sets parent[1] = 0, and union(1, 2) finds that 1's root is already 0 and sets parent[2] = 0. find(2) and find(0) then return the same root. The library's DisjointSet(3, use_heuristics=False) does this.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Singletons | parent = [0, 1, 2] | Each item is its own parent. |
| Union 0 and 1 | parent = [0, 0, 2] | find(1) is 1. Its parent becomes 0. |
| Union 1 and 2 | parent = [0, 0, 0] | find(1) walks to 0. 2's parent becomes 0. |
| find(2) | root = 0 | 2's parent is already 0, so the walk is one hop and 0 equals find(0). |

## Why it is correct

find returns the same root for two items exactly when they are in the same tree. union joins those trees only when the roots differ, so it does not create a cycle. Linking a root, rather than an arbitrary item, keeps every node on a path to a single root. The naive version can still build a long chain if each new item is hung under the previous leaf and find does not compress. Path compression points every visited node at the root. Union by rank hangs the shorter tree under the taller one. Together they make a long chain unlikely.

## What it costs

Without the heuristics, find is Θ(n) in the worst case on a chain of n items. With union by rank and path compression, the amortized cost of a find is the inverse of the Ackermann function, which is effectively constant for every practical n. Extra memory is the parent array, Θ(n), and a rank array when the heuristic is on. Kruskal's algorithm uses this to skip an edge whose ends are already connected.

## Practice and next step

Answer the checkpoint on this page, then use Next for the following lesson. The checkpoint stays in this browser.
