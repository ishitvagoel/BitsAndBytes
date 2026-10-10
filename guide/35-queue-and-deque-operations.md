---
title: Queue and deque operations
slug: queue-and-deque-operations
order: 35
status: present
module: bitsandbytes.queues.linked_queue, bitsandbytes.queues.circular_queue, bitsandbytes.deques.linked_deque
---

## The idea

A queue is first-in, first-out. enqueue adds at the back and dequeue removes from the front. The linked queue in this repository uses a doubly linked list with a cached tail, so both ends are Θ(1). A ring buffer stores the same order in an array with a head index and a tail index. A deque allows add and remove at both ends. The order promise is the part to learn first. After enqueue a, b, c, two dequeues return a and then b.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Enqueue a | front = a, size = 1 | a is both front and back. |
| Enqueue b | front = a, size = 2 | b joins the back. a stays at the front. |
| Enqueue c | front = a, size = 3 | c joins the back. |
| Dequeue twice | returned = b, front = c | The first dequeue returns a. The second returns b. c remains. |

## Why it is correct

The front is the earliest item that has not been dequeued. Enqueue does not change the front unless the queue was empty, in which case the new item is both front and back. Dequeue advances the front to the next node and returns the old one. That is why the exit order matches the arrival order. A stack would have returned c first. Mixing the two is the usual bug when a graph search asks for a queue and the code uses a list with pop() at the end and insert at the end.

## What it costs

Linked enqueue and dequeue are Θ(1) time and one new node of memory. A circular array is Θ(1) at both ends until it resizes, and then one resize copies the live items. n operations are Θ(n) total either way. Indexing the middle of a linked queue is Θ(n). If the algorithm needs the middle, an array is the better store.

Breadth-first search is the payoff. It is correct only when the frontier removes the oldest vertex. A list used as a stack visits a different order and the distance claim fails. The queue lesson is the reason that search works.

## Practice and next step

Answer the checkpoint on this page, then use Next for the following lesson. The checkpoint stays in this browser.
