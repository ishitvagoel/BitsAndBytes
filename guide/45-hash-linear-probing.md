---
title: Hash tables with linear probing
slug: hash-linear-probing
order: 45
status: present
module: bitsandbytes.hash_tables.linear_probing
---

## The idea

Linear probing stores one key in each slot of an array. The hash picks a start slot. If that slot is occupied by a different key, the insert tries the next slot, then the next, wrapping at the end of the array. A LinearProbingHashTable with capacity 4 stores key 0 in slot 0. Key 4 has the same start slot, finds it full, and takes slot 1. Lookup of 4 repeats that probe and returns 2. Deleting 0 does not write an empty slot. It writes a tombstone. Lookup of 4 must skip the tombstone and continue, otherwise it would stop and miss a key that sits further along the same probe. An empty slot still means the key is absent. The table rehashes when the number of live keys would reach half the capacity, which keeps clusters shorter.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Probe | capacity = 4 | Key 4 finds slot 0 full and takes the next slot. |
| Tombstone | found = 2 | Deleting 0 leaves a marker so the probe can still reach 4. |

## Why it is correct

The probe is a deterministic walk, so insert and lookup that start from the same hash follow the same slots. A tombstone is a slot that used to hold a key. It is not empty, because a later key may have stepped over it. Stopping at a tombstone would hide that later key. Stopping at an empty slot is safe, because an insert would have taken the first empty slot it saw. Rehashing copies every live key into a larger array and drops tombstones. The load factor is the number of live keys divided by the capacity.

## What it costs

One probe is constant time when clusters stay short, and linear in the worst case when keys pile into one run. Primary clustering is that pile. A collision does not stay in one slot. It makes the next inserts more likely to collide too. Extra memory is the slot arrays, one per capacity, plus the tombstones that still occupy slots until a rehash. Keep the load factor bounded if you want the expected constant probe.

## Run it

```python
from bitsandbytes.hash_tables.linear_probing import LinearProbingHashTable
table = LinearProbingHashTable(capacity=4)
table[0] = 1
table[4] = 2
del table[0]
print(table[4])
# prints: 2
```

## Practice and next step

Answer the checkpoint on this page, then use Next for the following lesson. The checkpoint stays in this browser.
