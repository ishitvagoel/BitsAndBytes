"""Bubble sort.

Walk the unsorted prefix and swap adjacent values that are out of order.
After each pass the largest remaining value is at the end of that prefix, so
the next pass is one step shorter. A pass that swaps nothing is already
sorted, and the scan stops.

Time: O(n^2) comparisons, best case O(n) on sorted input. O(1) extra memory.
Stable. Sorts in place and returns the same list.
"""

from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def bubble_sort(values: list[T]) -> list[T]:
    """Sort ``values`` in ascending order in place."""

    # ``end`` is the last index still being compared. It shrinks because the
    # tail of the list is already in its final position.
    for end in range(len(values) - 1, 0, -1):
        swapped = False
        for index in range(end):
            if values[index + 1] < values[index]:
                values[index], values[index + 1] = values[index + 1], values[index]
                swapped = True
        if not swapped:
            break
    return values
