"""Merge sort.

Split the sequence in half, sort each half, then merge by always taking the
smaller front value. The midpoint uses floor division. The Python 2 code used
``/``, which on Python 3 produces a float and cannot slice a list.

Ties prefer the left half, so equal keys keep their original relative order.

Time: O(n log n). Extra memory: O(n) for the merged halves.
Stable. Returns a new list and does not mutate the input.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


def merge_sort(values: Sequence[T]) -> list[T]:
    """Return a new list containing ``values`` in ascending order.

    Cost
    ----
    Let n be ``len(values)``. A list shorter than 2 returns in O(1). Otherwise
    the work is two recursive calls on n/2 plus one merge of n items:
    ``T(n) = 2 T(n/2) + O(n)``, with ``T(1) = O(1)``. Unrolling gives
    ``log2(n)`` levels and O(n) work on each level, so time is O(n log n) for
    every input order. Each level allocates new lists that together hold n
    items, and the recursion is ``log2(n)`` frames deep. Extra memory is O(n)
    for the halves, plus O(log n) for the call stack.
    """

    if len(values) < 2:
        return list(values)

    # Floor division is required: a float midpoint is not a valid slice index.
    midpoint = len(values) // 2
    left = merge_sort(values[:midpoint])
    right = merge_sort(values[midpoint:])
    return _merge(left, right)


def _merge(left: list[T], right: list[T]) -> list[T]:
    """Merge two ascending lists into one new ascending list.

    Cost
    ----
    Let a be ``len(left)`` and b be ``len(right)``. The loop runs once per
    item taken from either side, at most ``a + b`` times, and each step
    appends one value in amortized O(1). The two ``extend`` calls copy the
    leftovers, which were not yet counted, so every element is written
    exactly once. Time is O(a + b). The result list is new and holds
    ``a + b`` references: O(a + b) extra memory.
    """

    merged: list[T] = []
    left_index = 0
    right_index = 0
    while left_index < len(left) and right_index < len(right):
        # Take from the right only when it is strictly smaller. An equal key
        # stays with the left half, which is what makes the sort stable.
        if right[right_index] < left[left_index]:
            merged.append(right[right_index])
            right_index += 1
        else:
            merged.append(left[left_index])
            left_index += 1

    merged.extend(left[left_index:])
    merged.extend(right[right_index:])
    return merged
