---
title: Storage engines and locality
slug: storage-engines-and-locality
order: 68
status: present
module: bitsandbytes.storage.engines
---

## The idea

Storage engines place reads and writes in different structures. A B-tree keeps keys ordered in nodes with many children, so a lookup walks a short path. BTree.insert of 2 and then 1 leaves search(1) true and search(9) false. The branching factor is the knob that trades taller trees for fatter nodes. A log-structured merge tree takes the other side of the trade. Writes append to a memory table and a write-ahead log, then flush sorted runs. Reads may check several runs. Compaction merges those runs. The library's sequential_scan_sum of 1, 2, 3 returns 6. That scan touches neighboring items, which is the access pattern real disks and caches reward. A random jump to each key pays the same arithmetic and a worse memory pattern. Locality is why the sum of a tight array is the baseline you compare against.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Scan | sum = 6 | A sequential sum touches 1, 2, and 3 in order. |

## Why it is correct

B-tree search is correct because each node stores its keys in order. The child between two keys holds only the keys that belong between them. A missing key falls out of a leaf. Insert splits a full node so the branching invariant survives. A write-ahead log is correct when a replay reproduces the same committed writes. A sequential scan is correct because addition is applied once per item and the items are exactly the input. The locality claim is not a change in the arithmetic result. It is a claim about how many cache lines or pages that arithmetic touches.

## What it costs

A B-tree search is logarithmic in the number of keys, with a large base when nodes are wide. Extra memory is the nodes. A sequential scan is linear time and constant extra memory, and it is the practical winner when you need every item anyway. A point lookup in a structure built for scans can be slower than the same lookup in a tree. Say which operation is common before you pick the engine. The toy sum is the locality baseline, not a database.

## Run it

```python
from bitsandbytes.storage.engines import sequential_scan_sum
print(sequential_scan_sum([1, 2, 3]))
# prints: 6
```

## Practice and next step

Answer the checkpoints, then open Approximation guarantees. The checkpoint stays in this browser.
