---
title: Fast and slow pointers
slug: fast-slow-pointer-patterns
order: 22
status: present
module: bitsandbytes.linked_lists.middle, bitsandbytes.linked_lists.cycle, bitsandbytes.linked_lists.remove_cycle, bitsandbytes.linked_lists.nth_from_end, bitsandbytes.linked_lists.palindrome, bitsandbytes.linked_lists.modular_nodes
---

## What this pattern helps you find

Use two pointers that move at different speeds when a linked list does not offer direct indexing. The fast pointer moves two links for every one link the slow pointer moves. This turns a single traversal into a position or cycle test without storing every visited node.

**By the end of this overview, you can** describe how fast/slow movement finds a middle or detects a cycle, and explain when a fixed gap finds a node from the end.

## Follow the pointer relationship

On a linear list, `fast` reaches the end after roughly half as many updates as `slow`; `slow` is then at a middle position. On an even-length list, choosing `fast.next is None` versus `fast.next.next is None` determines which of the two middle nodes is returned. That boundary choice belongs in the function contract.

If links form a cycle, the fast pointer eventually catches the slow pointer because it gains one node per iteration. To locate the cycle entrance, reset one pointer to the head and advance both one step at a time; the meeting geometry makes them meet at the entrance.

For a node `k` positions from the end, first move a lead pointer `k` links ahead. Then move both pointers together. The gap stays `k`, so the trailing pointer reaches the requested position when the lead pointer reaches the end.

## Cost and checks

Each method makes a constant number of passes, so its time is O(n) in the number of links examined and its auxiliary pointer storage is O(1). The recursion or output allocation of a wrapper is separate from the pointer walk and must be included if the wrapper adds it.

Before using one of these methods, specify whether an even list returns the left or right middle, what `k` means at the boundaries, and whether input cycles are allowed. Test empty, one-node, even-length, and cyclic inputs against that contract.

## Practice and next step

Predict where `slow` is after three iterations on a seven-node list. Then trace what happens when the last node links back to the third node. Compare the prediction with the [repository pointer implementations and their tests](https://github.com/ishitvagoel/BitsAndBytes/blob/master/tests/test_linked_list_algorithms.py).

Continue to [linked-list reversal and relinking](./linked-list-reversal-and-relinking.md) to study algorithms that change the links themselves.
