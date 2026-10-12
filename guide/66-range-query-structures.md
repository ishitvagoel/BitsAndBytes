---
title: Range-query structures
slug: range-query-structures
order: 66
status: present
module: bitsandbytes.range_queries.structures
---

## The idea

A Fenwick tree that adds 1, 2, and 3 reports prefix 6.

Prefix sums answer a range in constant time until the array changes. A point update then costs a rebuild. A Fenwick tree and a segment tree keep the update logarithmic. FenwickTree of length 4, after add 1 at index 0, add 2 at index 1. Add 3 at index 2, reports prefix_sum(2) equal to 6. The structure stores partial sums on ranges whose length is a power of two. A point add walks those ranges. A prefix query walks a different set and sums them. SegmentTree on 1, 2, 3, 4 can add 5 to the inclusive span from index 1 to index 2. point_query(1) becomes 7 and point_query(0) stays 1. The lazy tag records the addition on a segment node and pushes it to children only when a later query needs them. SparseTable on 1, 3, 2, 4 answers range_min(1, 3) with 2. The range is inclusive. The table does not support updates. It precomputes the minimum of every power-of-two span.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Add | sum = 1 | Add 1 at index 0. The prefix through that index is 1. |
| Add | sum = 3 | Add 2 at index 1. The prefix through that index is 3. |
| Add | sum = 6 | Add 3 at index 2. The prefix through that index is 6. |

## Why it is correct

The Fenwick prefix is the sum of disjoint blocks that cover [0, index]. Each add updates every block that contains the index. Those two walks are why a query sees the latest adds. The segment tree's lazy tag is correct because a node tag means every leaf under it should receive the delta. Pushing the tag to the two children and clearing the parent preserves that meaning. The sparse table uses the fact that minimum is idempotent. The minimum of two overlapping blocks is still the minimum of the union, so a query can cover a range with two precomputed blocks.

## A common mistake

A static prefix array must be rebuilt after a point update. The tree does not.

## What it costs

A Fenwick add or prefix is logarithmic in the length. A segment update or point query is logarithmic. The sparse table builds in n log n and answers a minimum in constant time, with no updates. Extra memory is linear for the Fenwick tree, linear for the segment tree's nodes and tags, and n log n for the sparse table. Choose from the mix of updates and queries you actually have. A static array does not need the heavier tree. A Fenwick update is Θ(log n) time, and the tree uses Θ(n) extra memory.

## Run it

```python
from bitsandbytes.range_queries.structures import FenwickTree
tree = FenwickTree(4)
tree.add(0, 1)
tree.add(1, 2)
tree.add(2, 3)
print(tree.prefix_sum(2))
# prints: 6
```

## Practice and next step

Open Approximate membership structures next. A Bloom filter spends a false positive so a miss can stay definite.
