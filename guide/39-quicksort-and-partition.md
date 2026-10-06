---
title: Quicksort and partition
slug: quicksort-and-partition
order: 39
status: present
module: bitsandbytes.sorting.quick_sort
---

## Use a pivot to divide the work

Partition places values on either side of a pivot, then quicksort recursively sorts those ranges. The partition invariant separates values already known to be no greater than the pivot from the unprocessed suffix.

**By the end of this overview, you can** explain why balanced partitions give O(n log n) expected behavior and why repeated extreme pivots can cost O(n²).

With roughly balanced splits, there are O(log n) levels and O(n) partition work per level. If each pivot leaves an empty side, the recursion has a linear number of levels and scans `n`, then `n-1`, and so on: O(n²). Lomuto partition is not stable. A three-way partition can avoid repeated work when many keys equal the pivot.

## Practice and next step

Partition `[4, 2, 4, 1, 4]` around 4 and trace the equal values. Then compare the resulting recursive ranges with a sorted input. See [the repository quicksort tests](https://github.com/ishitvagoel/BitsAndBytes/blob/master/tests/test_search_and_sort_extras.py).
