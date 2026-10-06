---
title: Doubly linked-list operations
slug: doubly-linked-list-operations
order: 51
status: present
module: bitsandbytes.doubly_linked_list
---

## Update both directions

A doubly linked node stores `prev` and `next`. A list with head and tail sentinels can unlink a known node by connecting its neighbors, then clear the removed node's links.

**By the end of this overview, you can** trace an unlink and state the sentinel/list-size invariants that must remain true.

Unlinking or inserting beside a known node takes O(1) pointer updates. Finding a node by value still takes O(n), unless another structure stores its location. Every insertion must update four neighboring references; missing one direction can leave forward and backward walks disagreeing. Sentinels simplify empty and endpoint cases because real nodes always have neighbors.

## Practice and next step

Draw head sentinel → A ↔ B → tail sentinel. Remove A by writing every changed pointer. Check the list in both directions, then test an empty list and a one-node list. Compare with [the repository linked-list tests](https://github.com/ishitvagoel/BitsAndBytes/blob/master/tests/test_linked_list.py) and continue to [the LRU cache](./lru-cache.md).
