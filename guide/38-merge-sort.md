---
title: Merge sort
slug: merge-sort
order: 38
status: present
module: bitsandbytes.sorting.merge_sort
---

## Split, sort and merge

Merge sort divides a sequence into smaller pieces, sorts each piece, and merges two sorted runs. Its correctness follows from the merge step: repeatedly choose the smaller run head, then append the remaining suffix when one run empties.

**By the end of this overview, you can** derive O(n log n) time from the recursion levels and identify the extra merge storage.

For `n` values, there are O(log n) split levels. Each level merges O(n) total values, so time is O(n log n). The array implementation uses O(n) auxiliary memory for merging. It can be stable by choosing the left item when keys compare equal. Unlike quicksort, its worst-case time does not depend on pivot balance.

## Practice and next step

Merge `[1, 4, 7]` with `[2, 3, 8]`, recording the chosen head each time. Count how many items are moved at that level. Compare with [the implementation tests](https://github.com/ishitvagoel/BitsAndBytes/blob/master/tests/test_sorting.py) and continue to [quicksort and partition](./quicksort-and-partition.md).
