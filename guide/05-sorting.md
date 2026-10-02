---
title: Sorting
slug: sorting
order: 5
status: present
module: bitsandbytes.sorting.bubble_sort, bitsandbytes.sorting.selection_sort, bitsandbytes.sorting.insertion_sort, bitsandbytes.sorting.merge_sort, bitsandbytes.sorting.quick_sort
---

* `sorting/bubble_sort.py` — O(n²) worst and average, O(n) best on sorted input, O(1) extra memory. Stable.
* `sorting/selection_sort.py` — O(n²) for every input order. Not stable.
* `sorting/insertion_sort.py` — O(n²) worst and average, O(n) best. Stable.
* `sorting/merge_sort.py` — O(n log n) time, O(n) extra memory. Stable.
* `sorting/quick_sort.py` — Lomuto partition: expected O(n log n), worst O(n²), including an all-equal list. `quick_sort_three_way` handles duplicates in O(n) when every key matches. Not stable.
