---
title: Storage and locality
slug: storage-and-locality
order: 19
status: present
module: bitsandbytes.storage.engines
---

* `storage/engines.py` — in-memory B-tree, write-ahead log, toy LSM with Bloom-filtered runs, scan benchmark, brute-force nearest neighbor.

## Industry

A working engineer stores ordered keys in a B-tree, or buffers writes and
flushes sorted runs. PostgreSQL's documentation makes the B-tree the default
`CREATE INDEX` for equality and range queries. RocksDB's overview describes
the write path this module models: new writes go into a memtable and
optionally a write-ahead log, a full memtable is flushed to a sorted sst
file, and compaction merges files into sorted runs.
