---
title: Prefix sums
slug: prefix-sums
order: 60
status: present
module: bitsandbytes.patterns.arrays
---

## The idea

PrefixSum on 1, 2, 3, 4 answers range_sum(1, 3) with 5.

A prefix sum array stores the total of every item up to each index. The library PrefixSum on 1, 2, 3, 4 builds those totals once. range_sum(start, end) returns the sum of values[start:end], end exclusive. range_sum(1, 3) is 2 + 3, which is 5. The formula is total[end] minus total[start]. The item at start is included and the item at end is not, matching a Python slice. Any later range on the same array is then a subtraction. Counting subarrays that sum to a target uses the same totals. As you walk the array. A map from a previous prefix. To how many times it occurred tells you how many earlier starts would make the current prefix hit the target.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Prefix | sum = 1 | range_sum from 0 to 1 returns 1. |
| Prefix | sum = 3 | range_sum from 0 to 2 returns 3. |
| Prefix | sum = 10 | range_sum from 0 to 4 returns 10. |
| Slice | sum = 5 | range_sum from 1 to 3 returns 5, which is 2 + 3. |

## Why it is correct

total[0] is 0, the sum of an empty prefix. total[i + 1] is total[i] plus values[i]. By induction, total[end] is the sum of the first end items. Subtracting total[start] removes the items before the slice and leaves the slice. The half-open interval is why you do not add or drop an endpoint by hand. A target count is the same identity. If the current prefix minus a previous prefix equals the target, the slice between them sums to the target. The frequency map counts how many such previous prefixes exist.

## A common mistake

The end index is exclusive. Including it adds the value at that index.

## What it costs

Building the totals is linear time and linear extra memory. Each range query is constant time. n separate queries are therefore linear after the build, not quadratic. The frequency-map walk is linear expected time with a dictionary. Use prefix sums when the array does not change. A point update would force you to rebuild, which is why a later lesson brings a Fenwick tree. The build is Θ(n) time and uses Θ(n) extra memory.

## Run it

```python
from bitsandbytes.patterns.arrays import PrefixSum
print(PrefixSum([1, 2, 3, 4]).range_sum(1, 3))
# prints: 5
```

## Practice and next step

Open Backtracking search next. Backtracking searches a tree of choices and undoes each choice before the next sibling.
