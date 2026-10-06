---
title: Sorting extras
slug: sorting-extras
order: 12
status: present
module: bitsandbytes.sorting.selection_and_radix
---

This legacy page is the implementation map. Use the focused pages for [counting and radix sorts](./noncomparison-sorts.md), [order-statistic selection](./order-statistic-selection.md), [binary search on a feasible answer](./binary-search-on-answer.md), and [inversion counting](./inversion-counting.md).

* `sorting/selection_and_radix.py` — comparison lower bound, counting and LSD radix sorts, quickselect, binary search on the answer, inversion count.

## Industry

A working engineer does not sort the whole input when only the smallest few
values are required. Python's sorting howto points at `heapq.nsmallest` for
that job: one pass that keeps only the requested number of elements. Digit
keys are the other case in this lesson, counting sort and LSD radix, because
a comparison lower bound does not apply to them.
