---
title: Inversion counting
slug: inversion-counting
order: 43
status: present
module: bitsandbytes.sorting.selection_and_radix
---

## The idea

The list 3, 1, 4, 2 hides 3 inversions.

An inversion is a pair of indexes i < j whose values are out of order, value i greater than value j. inversion_count on 3, 1, 4, 2 returns 3. The pairs are 3 before 1, 3 before 2, and 4 before 2. A sorted array has zero inversions. A reversed array has one inversion per pair. The library counts them while it merges, the same split merge sort uses. Inside one sorted run there are no new inversions. Every inversion that still matters has one endpoint in the left run and one in the right run. When the merge takes from the right run while the left run still has a smaller-index key waiting. That left key and every key still in the left run form inversions with the key just taken.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Cross | count = 1 | Taking 1 adds 1 inversions. The total is 1. |
| Cross | count = 1 | Taking 2 adds 1 inversions. The total is 1. |
| Cross | count = 3 | Taking 2 adds 1 inversions. The total is 3. |

## Why it is correct

The merge already knows both runs are sorted. If the right front is smaller, it is smaller than every remaining left key, not only the left front. Adding the number of remaining left keys counts those inversions in one step. Keys taken from the left form no cross inversion with the current right front. Splitting into halves and adding the inversions inside each half counts every pair exactly once. A pair inside a half is counted by the recursive call. A pair that crosses the midpoint is counted by the merge.

## A common mistake

A pair that is already in order is not an inversion, even when the values are neighbors.

## What it costs

The recurrence matches merge sort. A logarithmic number of levels each do linear work, so the time is n log n. Extra memory is the merged runs, which is linear, plus the call stack. Checking every pair directly is quadratic and needs no extra array. Use the merge when you want the count and a sorted copy together. The count is also a measure of how far the input is from sorted. The count is Θ(n log n) time and uses Θ(n) extra memory.

## Run it

```python
from bitsandbytes.sorting.selection_and_radix import inversion_count
print(inversion_count([3, 1, 4, 2]))
# prints: 3
```

## Practice and next step

Open Hash tables with chaining next. Hash chaining stores a collision as a list inside one bucket.
