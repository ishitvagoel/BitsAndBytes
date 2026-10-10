---
title: Merge sort
slug: merge-sort
order: 38
status: present
module: bitsandbytes.sorting.merge_sort
---

## The idea

Merge sort splits the list in half, sorts each half, and merges the two sorted runs. The midpoint is len(values) // 2, integer division, so the halves differ by at most one item. The merge walks the two fronts and appends the smaller one. When the keys are equal it appends the left front, so equal keys keep the order they had in the input. The library merge_sort([3, 1, 4, 2]) returns [1, 2, 3, 4] and does not modify the input list.

## A worked trace

| Step | State | What changed |
| --- | --- | --- |
| Split | left = [3, 1], right = [4, 2] | The midpoint is 2. The halves are [3, 1] and [4, 2]. |
| Sort halves | left = [1, 3], right = [2, 4] | Each half of length 2 is sorted. The runs are [1, 3] and [2, 4]. |
| Take 1 | output = [1] | Fronts are 1 and 2. Take 1. |
| Take 2 | output = [1, 2] | Fronts are 3 and 2. Take 2. |
| Take 3 and 4 | output = [1, 2, 3, 4] | 3 leaves, then 4. The merged list is sorted. |

## Why it is correct

A list of length 0 or 1 is already sorted, which is the base case. If both halves are sorted, the merge is sorted because every output item is the smaller remaining front, so nothing still in either run is smaller than it. Stability follows from taking the left run on a tie. The left run holds the earlier original items of that key, because the split keeps original order inside each half and the recursive sorts are themselves stable.

## What it costs

The recurrence is T(n) = 2 T(n/2) + Θ(n). There are Θ(log n) levels and Θ(n) work merging on each level, so the time is Θ(n log n) for every input order. Each level allocates new lists holding n items, so extra memory is Θ(n), plus Θ(log n) for the call stack. The sort is stable and it always pays the full n log n cost, including on sorted input.

## Practice and next step

Answer the checkpoint on this page, then use Next for the following lesson. The checkpoint stays in this browser.
