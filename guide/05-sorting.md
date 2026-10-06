---
title: Sorting
slug: sorting
order: 5
status: present
module: bitsandbytes.sorting.bubble_sort, bitsandbytes.sorting.selection_sort, bitsandbytes.sorting.insertion_sort, bitsandbytes.sorting.merge_sort, bitsandbytes.sorting.quick_sort
---

This legacy page is the overview map. Start with [comparison sorts](./comparison-sorts.md), then follow [merge sort](./merge-sort.md) and [quicksort and partition](./quicksort-and-partition.md). For ranks and non-comparison methods, see [the sorting extras overview](./sorting-extras.md).

* `sorting/bubble_sort.py` — O(n²) worst and average, O(n) best on sorted input, O(1) extra memory. Stable.
* `sorting/selection_sort.py` — O(n²) for every input order. Not stable.
* `sorting/insertion_sort.py` — O(n²) worst and average, O(n) best. Stable.
* `sorting/merge_sort.py` — O(n log n) time, O(n) extra memory. Stable.
* `sorting/quick_sort.py` — Lomuto partition: expected O(n log n), worst O(n²), including an all-equal list. `quick_sort_three_way` handles duplicates in O(n) when every key matches. Not stable.

## Industry

A working engineer calls `list.sort`. Python's sorting howto names Timsort
and says it takes advantage of ordering already present in the data.
`list.sort` is guaranteed stable, and the time-complexity documentation
lists it as O(n log n) in the worst case. The quadratic sorts in this lesson
are the hand derivations of a worse bound.
