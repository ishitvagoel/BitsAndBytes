---
title: Hash tables with chaining
slug: hash-chaining
order: 44
status: present
module: bitsandbytes.hash_tables.chaining
---

## Store colliding keys in one bucket

A hash table maps a key to a bucket. With separate chaining, each bucket keeps the entries whose hashes map there. Lookup hashes the query, then searches only that bucket.

**By the end of this overview, you can** explain why load factor affects expected bucket work and why a resize has linear cost.

If hashes distribute keys well and the table keeps the load factor bounded, lookup and insertion are expected O(1). If many keys share one bucket, an operation can degrade to O(n). Growing the table and redistributing entries costs O(n) at that moment, but geometric growth spreads that work across insertions for amortized O(1) rehashing cost.

Hashing is a cost assumption too: very long keys take time to hash, and equal keys must have equal hashes. Do not confuse expected lookup with a worst-case guarantee.

## Practice and next step

Place keys with bucket indexes `[1, 3, 1, 2]` into four buckets, then trace a lookup for the second key in bucket 1. See [the repository hash-table tests](https://github.com/ishitvagoel/BitsAndBytes/blob/master/tests/test_hash_tables.py) and compare with [linear probing](./hash-linear-probing.md).
