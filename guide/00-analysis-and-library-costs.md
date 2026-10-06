---
title: Analysis and library costs
slug: analysis-and-library-costs
order: 0
status: present
module: bitsandbytes.complexity, bitsandbytes.library_costs
---

This legacy page is a short map to the foundation sequence: [input size and operation counts](./input-size-and-operation-counts.md), [asymptotic growth](./asymptotic-growth.md), [cost models](./cost-models.md), [loop invariants](./loop-invariants.md), [array and Python sequence costs](./arrays-and-python-costs.md), and [recursion and recurrences](./recursion-and-recurrences.md).

* `bitsandbytes/complexity.py` — word RAM model, O/Θ/Ω vocabulary, recursion limit, and the three recurrence shapes (merge divide, halving, linear decrement).
* `bitsandbytes/library_costs.py` — why BFS uses `deque`, `heapq.nsmallest`, `bisect.insort`, and Timsort; `list.pop(0)` costs O(n) element moves.

## Industry

A working engineer checks the language cost table before replacing a loop.
Python's time-complexity documentation lists `list.pop(0)` as O(n), because
every later element moves, and says to use a `collections.deque` when both
ends change. That deque documents approximately the same O(1) cost for
appends and pops in either direction.
