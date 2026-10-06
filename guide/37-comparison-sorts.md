---
title: Comparison sorts
slug: comparison-sorts
order: 37
status: present
module: bitsandbytes.sorting.bubble_sort, bitsandbytes.sorting.insertion_sort, bitsandbytes.sorting.selection_sort
---

## Sort by comparing neighboring or selected values

Bubble, insertion and selection sort are useful for understanding sorting invariants and small-input behavior. They all have O(n²) worst-case time, but their best cases, stability and swap patterns differ.

**By the end of this overview, you can** distinguish the sorted-prefix invariant in insertion sort from selection sort's repeated minimum choice.

Insertion sort grows a sorted prefix by shifting larger values right until the next item fits. It is stable and takes O(n) time on already sorted input, but O(n²) in the worst case. Selection sort repeatedly selects the remaining minimum and swaps it into place; it always makes Θ(n²) comparisons and is not stable in this implementation. Bubble sort swaps adjacent inversions; with an early-exit flag it can take O(n) time on sorted input and is stable.

## Practice and next step

Trace insertion sort on `[3, 1, 2]`, marking the sorted prefix after each pass. Then compare its equal-key order with selection sort. See [the repository sorting tests](https://github.com/ishitvagoel/BitsAndBytes/blob/master/tests/test_sorting.py).

Continue to [merge sort](./merge-sort.md) for a predictable O(n log n) comparison sort.
