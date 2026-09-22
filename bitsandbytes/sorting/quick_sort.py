"""Quick sort with a random pivot (Lomuto partition).

Pick a random index, move it to the end, and walk the range once. Every value
less than or equal to the pivot is swapped into the left side. The pivot then
drops into the boundary and is in its final position. Recurse on the two sides.

A random pivot makes the sorted-input case expected O(n log n) instead of the
O(n^2) trap of always pivoting on the last element. The worst case is still
O(n^2). Extra memory is the recursion stack, expected O(log n).

Not stable. Sorts in place and returns the same list. Pass ``rng`` to control
the pivot choices in tests.
"""

from __future__ import annotations

import random
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")

Chooser = Callable[[int, int], int]


def quick_sort(values: list[T], *, rng: random.Random | None = None) -> list[T]:
    """Sort ``values`` in ascending order in place."""

    choose = random.randint if rng is None else rng.randint
    _quick_sort(values, 0, len(values) - 1, choose)
    return values


def _quick_sort(
    values: list[T],
    start: int,
    end: int,
    choose: Chooser,
) -> None:
    # One element, or an empty range, is already partitioned.
    if start >= end:
        return
    boundary = _partition(values, start, end, choose)
    _quick_sort(values, start, boundary - 1, choose)
    _quick_sort(values, boundary + 1, end, choose)


def _partition(values: list[T], start: int, end: int, choose: Chooser) -> int:
    """Place a random pivot in its final index and return that index.

    After this returns, every index before the pivot holds a value ``<=`` pivot
    and every index after it holds a value ``>`` pivot.
    """

    pivot_index = choose(start, end)
    values[end], values[pivot_index] = values[pivot_index], values[end]
    pivot = values[end]

    # ``boundary`` is the next slot that should receive a value <= pivot.
    boundary = start
    for index in range(start, end):
        if values[index] <= pivot:
            values[boundary], values[index] = values[index], values[boundary]
            boundary += 1

    values[boundary], values[end] = values[end], values[boundary]
    return boundary
