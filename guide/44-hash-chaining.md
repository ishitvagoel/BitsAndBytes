---
title: Hash tables with chaining
slug: hash-chaining
order: 44
status: present
module: bitsandbytes.hash_tables.chaining
---

## The idea

Separate chaining stores a list of key-value pairs in each bucket. The hash of the key picks the bucket. Insert appends a pair, or replaces the value if the key is already in that list. Lookup scans the list and compares keys. With a 4-bucket table, hash(0) % 4 and hash(4) % 4 are both 0, so inserting 0 and then 4 places both pairs in one chain. A later lookup of 0 walks that chain and returns 1. The library ChainingHashTable does this, and len stays 2 because the keys differ.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Empty | size = 0 | Four buckets, no pairs. |
| Insert 0 | size = 1 | The pair (0, 1) is the only item in bucket 0. |
| Insert 4 | size = 2 | 4 hashes to bucket 0 and is appended. |
| Lookup 0 | found = 1 | The scan sees 0 first and returns 1. |

## Why it is correct

The hash is only a suggestion of where to look. Equality of keys is the real test, so two keys that share a bucket remain distinct as long as the chain stores both pairs and lookup does not stop at the first pair. Insert of a new key appends, which preserves the pairs already there. Insert of an existing key overwrites that pair's value instead of appending a duplicate. That is why a lookup that scans from the front finds the current value.

## What it costs

With n keys and b buckets the average chain is n / b, the load factor. One lookup is Θ(1 + n / b) comparisons when keys spread evenly, and Θ(n) when every key lands in one bucket. Resizing when the load factor grows keeps the average chain short, and the resize itself copies every pair once. Extra memory is Θ(n + b) for the pairs and the bucket lists. Expected Θ(1) is not a worst-case promise.

Keys 0 and 4 share a bucket because the bucket count is 4 and both hashes are multiples of 4. A third key 8 would append behind them. Lookup of 0 would then compare 0, skip 4, and skip 8 only if 0 were missing. The chain length is the cost you pay.

## Practice and next step

Answer the checkpoint on this page, then use Next for the following lesson. The checkpoint stays in this browser.
