---
title: Quicksort and partition
slug: quicksort-and-partition
order: 39
status: present
module: bitsandbytes.sorting.quick_sort
---

## The idea

Partition of [3, 1, 4, 2] with pivot 2 leaves [1, 2, 4, 3] before the recursive calls.

Quicksort picks a pivot and partitions the range. Every value before the pivot is at most the pivot. Every value after it is greater, and then the two sides are sorted. The library's partition swaps the chosen pivot to the end and scans once. boundary is the next slot that should receive a value at most the pivot. For pivot 2 at the end of [3, 1, 4, 2], the scan swaps 1 to index 0. The next swap places 2 at index 1, leaving [1, 2, 4, 3]. The recursive calls sort the two sides. quick_sort on this input returns [1, 2, 3, 4]. The pivot index itself is random unless you pass a Random instance.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| pivot | array = [3, 1, 4, 2] | Pivot 2 sits at index 3. |
| swap | array = [1, 3, 4, 2] | Swap index 1 with the boundary at 0. |
| pivot | array = [1, 2, 4, 3] | Pivot 3 sits at index 3. |

## Why it is correct

The partition invariant is that every index before boundary holds a value ≤ pivot. Every index from boundary to the scan cursor holds a value > pivot. It is true before the scan because that region is empty. Seeing a value > pivot extends the right region without moving boundary. Seeing a value ≤ pivot swaps it into the boundary slot and advances the boundary, which restores the invariant. The final swap puts the pivot at boundary. Everything before it is ≤ pivot and everything after it is > pivot, so the pivot is in its final sorted index.

## A common mistake

The two sides are not sorted when the pivot lands. Only the pivot index is final.

## What it costs

One partition of k items is Θ(k) time and O(1) extra memory. If every pivot splits off one item, the recurrence is T(n) = T(n - 1) + Θ(n). That shape is Θ(n²), and the call stack is Θ(n) deep. Balanced pivots give T(n) = 2 T(n/2) + Θ(n), which is Θ(n log n) time and Θ(log n) stack. The sort is not stable, because the swaps move equal keys past each other. A three-way partition gathers equals in the middle so a run of duplicate keys does not fall into the n² case.

## Run it

```python
import random
from bitsandbytes.sorting.quick_sort import quick_sort
print(quick_sort([3, 1, 4, 2], rng=random.Random(0)))
# prints: [1, 2, 3, 4]
```

## Practice and next step

Open Binary search next. Binary search uses a sorted list and throws away half of the remaining range.
