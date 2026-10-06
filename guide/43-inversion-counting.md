---
title: Inversion counting
slug: inversion-counting
order: 43
status: present
module: bitsandbytes.sorting.selection_and_radix
---

## Count out-of-order pairs during a merge

An inversion is a pair of positions `i < j` whose values are out of order: `values[i] > values[j]`. A quadratic double loop is simple, but merge sort can count many inversions at once.

**By the end of this overview, you can** explain why choosing a right-run value before the remaining left-run values counts a block of inversions.

During merge, if the next right value is smaller than the next left value, it is smaller than every remaining value in the sorted left run. Add the number of those left values to the count, then continue merging. The divide-and-conquer recurrence is the same shape as merge sort, so time is O(n log n), with O(n) extra buffer memory.

## Practice and next step

Count inversions in `[2, 4, 1, 3]` by listing each pair, then trace the merge where the 1 moves before 2 and 4. Compare with [the repository tests](https://github.com/ishitvagoel/BitsAndBytes/blob/master/tests/test_search_and_sort_extras.py).
