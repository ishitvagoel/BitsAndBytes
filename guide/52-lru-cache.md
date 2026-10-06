---
title: LRU cache
slug: lru-cache
order: 52
status: present
module: bitsandbytes.linked_lists.lru_cache
---

## Combine lookup with recency order

An LRU cache evicts the least recently used item when it reaches capacity. A dictionary finds entries by key; a doubly linked list keeps most-recent at the front and least-recent at the back.

**By the end of this overview, you can** explain how a cache hit and an eviction update both structures.

On a hit, look up the node in expected O(1) time and move it to the front with O(1) link updates. On insertion at capacity, remove the tail node and delete its key from the dictionary. Then add the new node to both structures. Expected get/put time is O(1); resident storage is O(capacity). The dictionary cost is expected rather than worst-case because hash collisions can degrade lookup.

The consistency invariant is that every dictionary entry points to exactly one node in the recency list, and every real list node has exactly one dictionary key. Test capacity zero/one, updates to existing keys, and eviction order.

## Practice and next step

With capacity two, access `A`, `B`, `A`, then insert `C`. Name the evicted key and update both structures after each step. Compare with [the repository LRU tests](https://github.com/ishitvagoel/BitsAndBytes/blob/master/tests/test_linked_list.py).
