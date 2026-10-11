---
title: Inversion counting
slug: inversion-counting
order: 43
status: present
module: bitsandbytes.sorting.selection_and_radix
---

## The idea

An inversion is a pair of indexes i < j whose values are out of order, value i greater than value j. inversion_count on 3, 1, 4, 2 returns 3. The pairs are 3 before 1, 3 before 2, and 4 before 2. A sorted array has zero inversions. A reversed array has one inversion per pair. The library counts them while it merges, the same split merge sort uses. Inside one sorted run there are no new inversions. Every inversion that still matters has one endpoint in the left run and one in the right run. When the merge takes from the right run while the left run still has a smaller-index key waiting. That left key and every key still in the left run form inversions with the key just taken.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Pairs | count = 3 | Three pairs are out of order in 3, 1, 4, 2. |

## Why it is correct

The merge already knows both runs are sorted. If the right front is smaller, it is smaller than every remaining left key, not only the left front. Adding the number of remaining left keys counts those inversions in one step. Keys taken from the left form no cross inversion with the current right front. Splitting into halves and adding the inversions inside each half counts every pair exactly once. A pair inside a half is counted by the recursive call. A pair that crosses the midpoint is counted by the merge.

## What it costs

The recurrence matches merge sort. A logarithmic number of levels each do linear work, so the time is n log n. Extra memory is the merged runs, which is linear, plus the call stack. Checking every pair directly is quadratic and needs no extra array. Use the merge when you want the count and a sorted copy together. The count is also a measure of how far the input is from sorted.

## Run it

```python
from bitsandbytes.sorting.selection_and_radix import inversion_count
print(inversion_count([3, 1, 4, 2]))
# prints: 3
```

## Practice and next step

Answer the checkpoints, then open Hash tables with chaining. The checkpoint stays in this browser.
