---
title: Heap operations
slug: heap-operations
order: 49
status: present
module: bitsandbytes.heaps.heapsort
---

## Keep a partial order in an array

A binary min-heap places the smallest value at the root. Each parent is no greater than either child; the rest of the array is not fully sorted. Array indexes encode parent and child relationships.

**By the end of this overview, you can** state the heap invariant and explain bottom-up heapify's linear work.

Restoring the invariant after one push or root removal follows a path of tree height, O(log n). Bottom-up heapify starts near the leaves, where nodes have little work to move; summing work by height gives O(n), not O(n log n). Heapsort repeatedly moves the root to the end and repairs the remaining heap, taking O(n log n) time and O(1) extra array space. It is not stable.

## Practice and next step

For `[3, 1, 4, 2]`, identify a valid min-heap arrangement and show the swaps needed after removing the root. Compare with [the repository heap tests](https://github.com/ishitvagoel/BitsAndBytes/blob/master/tests/test_heaps.py) and continue to [priority queues](./priority-queues.md).
