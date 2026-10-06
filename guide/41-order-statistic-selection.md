---
title: Order-statistic selection
slug: order-statistic-selection
order: 41
status: present
module: bitsandbytes.sorting.selection_and_radix
---

## Find one rank without sorting everything

The `k`th smallest value is an order statistic. Quickselect partitions around a pivot and continues only in the side containing rank `k`, unlike quicksort, which sorts both sides.

**By the end of this overview, you can** explain why expected quickselect work is O(n) and state its worst case.

With random-like pivot splits, the active range shrinks enough that total work is expected O(n). Repeatedly choosing an extreme pivot can still produce O(n²). The implementation mutates the input list, so callers must account for that behavior. Sorting is a better choice when many ranks or a fully ordered result are needed; selection is useful for one rank.

## Practice and next step

For `[7, 2, 5, 1, 9]`, identify the values smaller and larger than a pivot of 5, then decide which side contains the 1st-smallest value. See [the repository selection tests](https://github.com/ishitvagoel/BitsAndBytes/blob/master/tests/test_search_and_sort_extras.py).
