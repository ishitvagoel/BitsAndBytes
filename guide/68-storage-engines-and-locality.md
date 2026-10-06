---
title: Storage engines and locality
slug: storage-engines-and-locality
order: 68
status: present
module: bitsandbytes.storage.engines
---

## Organize work around the storage medium

B-trees keep sorted keys in high-fanout nodes to reduce page reads. Log-structured merge designs buffer writes and merge sorted runs later; Bloom filters can avoid reads for keys absent from a run. Each design shifts cost among reads, writes, memory and compaction.

## Measure locality, not only operation counts

Two O(log n) structures can have different cache and disk behavior. Sequential scans and contiguous storage use locality; pointer-heavy access can trigger more cache misses or page reads. Treat the repository's engines as teaching models rather than production databases.

## Practice

Compare a B-tree lookup with an LSM lookup that checks several runs. Identify the conditions where a Bloom filter saves I/O and where compaction costs appear.

Source: [`engines.py`](../bitsandbytes/storage/engines.py).
