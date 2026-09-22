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
    """Return a new list containing ``values`` in ascending order."""

    if len(values) < 2:
        return list(values)

    # Floor division is required: a float midpoint is not a valid slice index.
    midpoint = len(values) // 2
    left = merge_sort(values[:midpoint])
    right = merge_sort(values[midpoint:])
    return _merge(left, right)


def _merge(left: list[T], right: list[T]) -> list[T]:
    """Merge two ascending lists into one new ascending list."""

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
