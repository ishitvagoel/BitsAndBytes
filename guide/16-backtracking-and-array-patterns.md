---
title: Backtracking and array patterns
slug: backtracking-and-array-patterns
order: 16
status: present
module: bitsandbytes.backtracking.search, bitsandbytes.patterns.arrays
---

* `backtracking/search.py` — permutations, combinations, subsets, N-queens count.

## Focused lessons

- [Two-pointer patterns](./58-two-pointers.md)
- [Sliding windows](./59-sliding-window.md)
- [Prefix sums](./60-prefix-sums.md)
- [Backtracking search](./61-backtracking.md)
- [Greedy methods](./62-greedy-methods.md)
- [Dynamic programming state and transitions](./63-dp-state-and-transition.md)
* `patterns/arrays.py` — two pointers, sliding window, prefix sums, monotonic-queue window maximum.

## Industry

A working engineer writes a backtracking search when a partial choice can be
rejected, and a forward scan when the constraint is a window. The
sliding-window maximum in this lesson keeps candidate indexes in a
`collections.deque`. Python documents approximately O(1) appends and pops at
either end, so each index can enter the deque and leave it once.
