---
title: Hash tables with linear probing
slug: hash-linear-probing
order: 45
status: present
module: bitsandbytes.hash_tables.linear_probing
---

## Resolve collisions by probing nearby slots

Open addressing stores entries inside the table array. With linear probing, a collision checks the next slot, wrapping around, until it finds the key or an empty position.

**By the end of this overview, you can** trace a probe sequence and explain why a deleted slot needs a tombstone.

Search stops at a never-used empty slot, but a tombstone cannot end search: a key farther along the same probe chain may still be present. Insertion can reuse a tombstone after confirming that the key does not already occur later in the chain. As the table fills, long clusters make operations slower, so resizing and load-factor policy matter.

Expected O(1) behavior depends on a distribution of hashes and a controlled load factor. A degenerate hash can force O(n) probes. Track the slot state carefully: empty, occupied and deleted mean different things.

## Practice and next step

Insert three keys whose initial slot is 2 into a table of size 5. Delete the middle key, then search for the last. Explain why stopping at its tombstone would be wrong. See [the repository hash-table tests](https://github.com/ishitvagoel/BitsAndBytes/blob/master/tests/test_hash_tables.py).
