"""Insertion sort.

Take the next unsorted value and shift the sorted prefix right until the hole
is where that value belongs. Shifting, rather than swapping on every step,
moves each preceding element once.

Time: O(n^2), best case O(n) on sorted input. O(1) extra memory.
Stable, because an equal key stops the shift (the comparison is strict ``<``).
Sorts in place and returns the same list.
"""

from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def insertion_sort(values: list[T]) -> list[T]:
    """Sort ``values`` in ascending order in place.

    Cost
    ----
    Let n be ``len(values)``. The outer loop runs ``n - 1`` times. On step
    ``i`` the inner loop shifts the sorted prefix of length ``i`` until it
    finds the hole. Each shift is O(1). Worst case (reverse sorted) shifts
    ``i`` times on step ``i``, and ``1 + 2 + ... + (n - 1) = n(n - 1) / 2``,
    so time is O(n²). Average input shifts about half the prefix, which is
    the same sum divided by 2, still O(n²). Best case (already sorted) never
    enters the inner loop: ``n - 1`` comparisons, O(n). The hole index and
    the key are O(1) extra memory.
    """

    for index in range(1, len(values)):
        key = values[index]
        hole = index - 1
        while hole >= 0 and key < values[hole]:
            values[hole + 1] = values[hole]
            hole -= 1
        values[hole + 1] = key
    return values
