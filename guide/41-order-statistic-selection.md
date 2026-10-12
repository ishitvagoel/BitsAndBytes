---
title: Order-statistic selection
slug: order-statistic-selection
order: 41
status: present
module: bitsandbytes.sorting.selection_and_radix
---

## The idea

quickselect on 3, 1, 4, 2 with k = 2 returns 3.

An order statistic is the k-th smallest key, counting from zero. Sorting would find it, and would also order every other key. quickselect stops when the pivot lands on k. On a copy of 3, 1, 4, 2, quickselect with k = 0 returns 1. The same input with k = 2 returns 3, the third smallest key in 1, 2, 3, 4. The library partition always uses the rightmost value as the pivot. It walks the range once, swaps smaller keys toward the left boundary, and writes the pivot into the boundary. If that index is k, the pivot is the answer. If k is smaller, the search continues on the left side only. If k is larger, it continues on the right side only. The discarded side is not sorted.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Partition | index = 1 | Pivot 2 lands at index 1. The array is [1, 2, 4, 3]. |
| Partition | index = 2 | Pivot 3 lands at index 2. The array is [1, 2, 3, 4]. |
| Answer | k = 2 | k is 2, so the value at that index is the answer 3. |

## Why it is correct

The partition invariant matches quicksort. Everything before the boundary is less than or equal to the pivot, and everything after it is greater. The pivot is therefore in its final sorted index even though the two sides are not sorted. The k-th smallest key must lie on the side that still contains index k. Throwing the other side away cannot hide the answer. The loop ends when the pivot index equals k, so the value sitting there is the order statistic.

## A common mistake

The discarded side is not sorted, and it cannot contain the k-th smallest key.

## What it costs

A balanced pivot throws away a constant fraction of the range, and the expected cost of that recurrence is linear. This implementation does not choose a random pivot. It always uses the right end. An input that always puts an extreme key at the right end shrinks the range by one item and the time becomes quadratic. Extra memory is a handful of indexes. Sort the whole array when you need every order statistic. Select when you need one. Expected time is Θ(n), and extra memory is O(1).

## Run it

```python
from bitsandbytes.sorting.selection_and_radix import quickselect
print(quickselect([3, 1, 4, 2], 0))
# prints: 1
```

## Practice and next step

Open Inversion counting next. Inversion counting measures how far a list is from sorted while it merges.
