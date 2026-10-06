---
title: Hash table
slug: hash-table
order: 9
status: present
module: bitsandbytes.hash_tables.chaining, bitsandbytes.hash_tables.linear_probing
---

This legacy page is the implementation index. Compare [separate chaining](./hash-chaining.md) with [linear probing](./hash-linear-probing.md) to see two ways to resolve collisions.

* `hash_tables/chaining.py` — separate chaining. Expected O(1) lookup and insert; rehash is O(n) but amortized.
* `hash_tables/linear_probing.py` — open addressing with tombstones. `degenerate_chain_length` explains a one-bucket table.

## Industry

A working engineer uses a `dict` for lookup by key. Python's time-complexity
documentation lists average-case get, set, and delete as O(1), and O(n) when
every key hashes to the same bucket. Separate chaining is one bucket's list;
that worst case is why a degenerate hash is part of this lesson.
