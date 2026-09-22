"""Comparison sorts.

Each function documents whether it sorts in place. Ordering uses ``<``.
Quick sort's partition is the exception: values equal to the pivot stay on
its left, which keeps that scan to a single pass.
"""

from bitsandbytes.sorting.bubble_sort import bubble_sort
from bitsandbytes.sorting.insertion_sort import insertion_sort
from bitsandbytes.sorting.merge_sort import merge_sort
from bitsandbytes.sorting.quick_sort import quick_sort, quick_sort_three_way
from bitsandbytes.sorting.selection_sort import selection_sort

__all__ = [
    "bubble_sort",
    "insertion_sort",
    "merge_sort",
    "quick_sort",
    "quick_sort_three_way",
    "selection_sort",
]
