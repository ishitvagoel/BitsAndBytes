---
title: Priority queues
slug: priority-queues
order: 50
status: present
module: bitsandbytes.heaps.priority_queue
---

## Retrieve the next item by priority

A priority queue stores items with priorities and returns the smallest or largest priority first. A heap supports this without sorting the whole collection after each update.

**By the end of this overview, you can** relate push, pop and decrease-key to heap height and explain what an index map adds.

Push and pop restore the heap invariant along one path, so they take O(log n) time. Decrease-key must find the item as well as move it upward; an index map provides the location in O(1) expected time, followed by O(log n) repair. Every swap must update the map or later operations may target the wrong item.

Python's [`heapq`](https://docs.python.org/3/library/heapq.html) exposes a list-based min-heap with the minimum at index 0. It does not provide an indexed decrease-key operation directly; a separate map or stale-entry strategy is needed when priorities change.

## Practice and next step

Trace priorities `[7, 2, 5]` through push and pop. Then explain what must change in an index map when two heap items swap. See [the repository priority-queue tests](https://github.com/ishitvagoel/BitsAndBytes/blob/master/tests/test_heaps.py).
