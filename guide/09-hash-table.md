---
title: Hash table
slug: hash-table
order: 9
status: present
module: bitsandbytes.hash_tables.chaining, bitsandbytes.hash_tables.linear_probing
---

* `hash_tables/chaining.py` — separate chaining. Expected O(1) lookup and insert; rehash is O(n) but amortized.
* `hash_tables/linear_probing.py` — open addressing with tombstones. `degenerate_chain_length` explains a one-bucket table.
