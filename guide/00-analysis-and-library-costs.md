---
title: Analysis and library costs
slug: analysis-and-library-costs
order: 0
status: present
module: bitsandbytes.complexity, bitsandbytes.library_costs
---

* `bitsandbytes/complexity.py` — word RAM model, O/Θ/Ω vocabulary, recursion limit, and the three recurrence shapes (merge divide, halving, linear decrement).
* `bitsandbytes/library_costs.py` — why BFS uses `deque`, `heapq.nsmallest`, `bisect.insort`, and Timsort; `list.pop(0)` costs O(n) element moves.
