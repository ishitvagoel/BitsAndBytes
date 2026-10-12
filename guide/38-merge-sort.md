---
title: Merge sort
slug: merge-sort
order: 38
status: present
module: bitsandbytes.sorting.merge_sort
---

## The idea

merge_sort([3, 1, 4, 2]) returns [1, 2, 3, 4]. The first split is [3, 1] and [4, 2].

Merge sort splits the list in half, sorts each half, and merges the two sorted runs. The midpoint is len(values) // 2, integer division, so the halves differ by at most one item. The merge walks the two fronts and appends the smaller one. When the keys are equal it appends the left front, so equal keys keep the order they had in the input. The library merge_sort([3, 1, 4, 2]) returns [1, 2, 3, 4] and does not modify the input list.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Split | left = [3, 1] | Split into [3, 1] and [4, 2]. |
| Split | left = [3] | Split into [3] and [1]. |
| Take | output = [1] | The merge takes 1. The output is [1]. |
| Take | output = [1, 3] | The merge takes 3. The output is [1, 3]. |
| Split | left = [4] | Split into [4] and [2]. |
| Take | output = [2] | The merge takes 2. The output is [2]. |
| Take | output = [2, 4] | The merge takes 4. The output is [2, 4]. |
| Take | output = [1] | The merge takes 1. The output is [1]. |
| Take | output = [1, 2] | The merge takes 2. The output is [1, 2]. |
| Take | output = [1, 2, 3] | The merge takes 3. The output is [1, 2, 3]. |
| Take | output = [1, 2, 3, 4] | The merge takes 4. The output is [1, 2, 3, 4]. |

## Why it is correct

A list of length 0 or 1 is already sorted, which is the base case. If both halves are sorted, the merge is sorted because every output item is the smaller remaining front. Nothing still in either run is smaller than that item. Stability follows from taking the left run on a tie. The left run holds the earlier original items of that key. The split keeps original order inside each half, and the recursive sorts are themselves stable.

## A common mistake

Taking the right run on a tie moves an equal key in front of an earlier equal key.

## What it costs

The recurrence is T(n) = 2 T(n/2) + Θ(n). There are Θ(log n) levels and Θ(n) work merging on each level, so the time is Θ(n log n) for every input order. Each level allocates new lists holding n items, so extra memory is Θ(n), plus Θ(log n) for the call stack. The sort is stable and it always pays the full n log n cost, including on sorted input.

## Run it

```python
from bitsandbytes.sorting.merge_sort import merge_sort
print(merge_sort([3, 1, 4, 2]))
# prints: [1, 2, 3, 4]
```

## Practice and next step

Open Quicksort and partition next. Quicksort sorts in place and shows what an unlucky pivot costs.
