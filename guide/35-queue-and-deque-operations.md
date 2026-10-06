---
title: Queue and deque operations
slug: queue-and-deque-operations
order: 35
status: present
module: bitsandbytes.queues.linked_queue, bitsandbytes.queues.circular_queue, bitsandbytes.deques.linked_deque
---

## Choose which end changes

A FIFO queue adds at the back and removes from the front. A deque supports both ends. These operations differ from a stack, which adds and removes at the same end.

**By the end of this overview, you can** trace FIFO order and compare linked and circular-buffer queue invariants.

## Preserve queue order

After enqueueing `A`, then `B`, then `C`, successive dequeues return `A`, `B`, `C`. A linked queue with head and tail references can add and remove at the ends in O(1) time. A fixed-capacity circular queue stores a front index and size; advancing the front wraps modulo capacity. Its invariant keeps the logical queue order even when the physical array wraps.

For a deque, adding or removing at either end can be O(1), while locating an arbitrary middle position is O(n). Python's [`collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque) is a standard choice for a FIFO queue; the documentation describes approximately O(1) operations at either end.

## Practice and next step

In a capacity-five circular queue, enqueue four values, dequeue two, and enqueue three more. Track front, size and occupied slots after every operation. Continue to [dynamic-array growth](./dynamic-array-growth.md) to compare a resizable sequence with a fixed ring buffer.
