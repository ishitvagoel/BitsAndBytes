---
title: Prefix sums
slug: prefix-sums
order: 60
status: present
module: bitsandbytes.patterns.arrays
---

## The idea

A prefix sum array stores the total of every item up to each index. The library PrefixSum on 1, 2, 3, 4 builds those totals once. range_sum(start, end) returns the sum of values[start:end], end exclusive. range_sum(1, 3) is 2 + 3, which is 5. The formula is total[end] minus total[start]. The item at start is included and the item at end is not, matching a Python slice. Any later range on the same array is then a subtraction. Counting subarrays that sum to a target uses the same totals. As you walk the array, a map from a previous prefix to how many times it occurred tells you how many earlier starts would make the current prefix hit the target.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Range | sum = 5 | The half-open slice from 1 to 3 sums to 5. |

## Why it is correct

total[0] is 0, the sum of an empty prefix. total[i + 1] is total[i] plus values[i]. By induction, total[end] is the sum of the first end items. Subtracting total[start] removes the items before the slice and leaves the slice. The half-open interval is why you do not add or drop an endpoint by hand. A target count is the same identity. If the current prefix minus a previous prefix equals the target, the slice between them sums to the target. The frequency map counts how many such previous prefixes exist.

## What it costs

Building the totals is linear time and linear extra memory. Each range query is constant time. n separate queries are therefore linear after the build, not quadratic. The frequency-map walk is linear expected time with a dictionary. Use prefix sums when the array does not change. A point update would force you to rebuild, which is why a later lesson brings a Fenwick tree.

## Run it

```python
from bitsandbytes.patterns.arrays import PrefixSum
print(PrefixSum([1, 2, 3, 4]).range_sum(1, 3))
# prints: 5
```

## Practice and next step

Answer the checkpoint on this page, then use Next for the following lesson. The checkpoint stays in this browser.
