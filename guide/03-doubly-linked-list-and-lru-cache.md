---
title: Doubly linked list and the LRU cache
slug: doubly-linked-list-and-lru-cache
order: 3
status: present
module: bitsandbytes.doubly_linked_list, bitsandbytes.linked_lists.random_pointer, bitsandbytes.linked_lists.lru_cache
---

* `bitsandbytes/doubly_linked_list.py` — `prev` makes unlink and insert-beside-a-node O(1). Reversal is O(n) time and O(1) extra memory.
* `linked_lists/random_pointer.py` — dictionary clone expected O(n) time and O(n) extra memory; interleaved clone O(n) time and O(1) scratch besides the copy.
* `linked_lists/lru_cache.py` — dictionary plus doubly linked list. `get` and `put` are expected O(1). Resident memory is O(capacity). The hash table chapter explains why the dictionary lookup is expected O(1).

## Industry

A working engineer caches the most recent calls with `functools.lru_cache`,
which saves up to `maxsize` most recent calls. This course builds that
policy as a hash table plus an order list: the dictionary finds the key, and
the doubly linked list unlinks that node and moves it to the front without a
scan. A singly linked order list would have to walk from the head to find
the predecessor.
