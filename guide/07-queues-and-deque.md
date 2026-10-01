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
