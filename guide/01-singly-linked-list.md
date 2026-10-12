---
title: Singly linked list
slug: singly-linked-list
order: 1
status: present
module: bitsandbytes.linked_list
---

## The idea

Append a, then b, then c. Removing b visits a and then b.

A singly linked list stores each value in a node whose next reference points at the following node. The list keeps a head, a cached tail, and a size. The invariant is that following next from the head visits exactly size nodes and ends at the cached tail, whose next is empty. Prepending changes the head in Θ(1) time. Appending with a cached tail changes the old tail's next and moves the tail pointer in Θ(1) time. Reading an index walks from the head, so it is Θ(n). Removing the tail is also Θ(n), because the predecessor is not stored.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Append | head = a | Append a. The head and the tail are both a. |
| Append | tail = b | Append b. The tail moves to b. |
| Append | size = 3 | Append c. The chain is a, b, c. |
| Visit | node = a | The scan visits a while looking for b. |
| Visit | node = b | The scan visits b while looking for b. |

## Why it is correct

The invariant is preserved by each edit that updates the cached fields together with the links. Append writes the new node, points the old tail at it, and then moves the tail cache. If it moved the cache first, the old tail would be unreachable and the invariant would fail. A search that starts at the head and follows next i times lands on index i. The nodes form a single chain with no extra forward jumps. There is no predecessor pointer, so the only way to find the node before the tail is to walk until next is the tail.

## A common mistake

A cached tail finds the last node. It does not find the node that points at the last node.

## What it costs

Append and prepend are Θ(1). Index lookup and tail removal are Θ(n). len is Θ(1) because size is cached. Extra memory is one node per item plus the three list fields. A Python list is the better default when you need list[i]. The linked list earns its place when you already hold the node you want to relink.

## Run it

```python
from bitsandbytes.linked_list import LinkedList
chain = LinkedList()
chain.append('a')
print(list(chain))
# prints: ['a']
```

## Practice and next step

Open Fast and slow pointers next. Fast and slow pointers replace an index when the chain has no random access.
