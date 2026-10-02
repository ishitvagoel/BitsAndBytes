---
title: Range queries and approximate structures
slug: range-queries-and-approximate-structures
order: 18
status: present
module: bitsandbytes.range_queries.structures, bitsandbytes.approximate.structures
---

* `range_queries/structures.py` — Fenwick tree, lazy segment tree, sparse table for RMQ.
* `approximate/structures.py` — Bloom filter, skip list, persistent stack frames.

## Industry

A working engineer uses a Bloom filter when a definite miss is enough to
skip a lookup. Redis documents `BF.ADD` to add an item and `BF.EXISTS` to
test one: a hit means the item was probably added, and a miss means it was
definitely not. A Fenwick tree or a segment tree is the structure in this
lesson when the answer has to be an exact prefix or an exact range.
