---
title: Queues and deque
slug: queues-and-deque
order: 7
status: present
module: bitsandbytes.queues.linked_queue, bitsandbytes.queues.circular_queue, bitsandbytes.linear.dynamic_array, bitsandbytes.deques.linked_deque
---

* `queues/linked_queue.py` — FIFO with a doubly linked list. Enqueue and dequeue are O(1).
* `queues/circular_queue.py` — fixed-capacity ring buffer with an explicit size counter. Enqueue and dequeue are O(1).
* `linear/dynamic_array.py` — geometric doubling; n appends copy O(n) elements in total.
* `deques/linked_deque.py` — O(1) at both ends on a doubly linked list; middle insert is O(n).

## Industry

A working engineer implements a queue with `collections.deque`. The Python
tutorial says a `list` is a poor queue, because an insert or pop at the
beginning shifts every other element, and that `collections.deque` has fast
appends and pops at both ends. The deque documentation states approximately
the same O(1) performance in either direction, which is why `list.pop(0)` is
the operation to avoid.
