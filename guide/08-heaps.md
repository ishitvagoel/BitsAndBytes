---
title: Heaps
slug: heaps
order: 8
status: present
module: bitsandbytes.heaps.heapsort, bitsandbytes.heaps.priority_queue
---

* `heaps/heapsort.py` — `heapify` is O(n); `heapsort` is O(n log n) time and O(1) extra memory. Not stable.
* `heaps/priority_queue.py` — min-heap with `decrease_key` through an index map. Push, pop, and decrease-key are O(log n).

## Industry

A working engineer uses `heapq` as a priority queue. Python documents a
min-heap whose smallest item is always `heap[0]`, with `heapify` in linear
time. Removing that root and restoring the heap is logarithmic, and
repeating the removal sorts in O(n log n). The same page notes that this
heapsort is not stable, which is also true of `heapsort` here.
