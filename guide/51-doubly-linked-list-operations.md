---
title: Doubly linked-list operations
slug: doubly-linked-list-operations
order: 51
status: present
module: bitsandbytes.doubly_linked_list
---

## The idea

A doubly linked node stores prev and next. If you already hold the node, you do not walk from the head to find its neighbors. remove_node on the node for a, in a list that also holds b, returns a and leaves b. The unlink follows prev and next and rewires those neighbors to each other. insert_after splices a new node between a known node and that node's next. Both directions must be written. A missing reverse link makes a forward walk and a backward walk disagree. Finding a node by value is still linear, unless another structure stores the node. Sentinels are one way to make every real node have neighbors, including the empty list. This list keeps a head and a tail instead, and the endpoint cases update those caches.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Unlink | removed = a | Removing a known node does not walk the list. |

## Why it is correct

The known-node claim is that the predecessor and the successor are fields, not search results. Rewiring them restores a single chain. The forward neighbor's prev and the backward neighbor's next must both change, or one direction still points at the removed node. insert_after writes the new node's two links and the two neighboring links that should point at it. That is four pointers when both neighbors exist. An endpoint has a missing neighbor, so the list updates head or tail instead of a second node. The size cache changes by one. After the edit, a walk from the head and a walk from the tail must list the same nodes in opposite orders.

## What it costs

Unlinking or inserting beside a known node is a constant number of pointer writes. It is constant time. A singly linked delete of an arbitrary node is linear, because the predecessor must be found from the head. A search by value on this list is still linear. n such searches are quadratic if you repeat them. Extra memory is one node per item plus the list caches. Draw both directions after a removal. Then test an empty list and a one-node list, and check that head and tail still agree.

## Run it

```python
from bitsandbytes.doubly_linked_list import DoublyLinkedList
chain = DoublyLinkedList()
first = chain.append('a')
chain.append('b')
print(chain.remove_node(first))
# prints: a
```

## Practice and next step

Answer the checkpoints, then open Stack basics. The checkpoint stays in this browser.
