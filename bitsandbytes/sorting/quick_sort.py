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
    """Sort ``values`` in ascending order in place.

    Cost
    ----
    Let n be ``len(values)``. This only builds the pivot chooser, O(1), then
    calls ``_quick_sort`` on the whole range. Expected time is O(n log n) and
    worst-case time is O(n²); the recurrence is derived on ``_quick_sort``.
    The list is rearranged in place. Extra memory is the recursion stack:
    expected O(log n), worst case O(n).
    """

    choose = random.randint if rng is None else rng.randint
    _quick_sort(values, 0, len(values) - 1, choose)
    return values


def _quick_sort(
    values: list[T],
    start: int,
    end: int,
    choose: Chooser,
) -> None:
    """Sort ``values[start:end + 1]`` in place.

    Cost
    ----
    Let n be ``end - start + 1``. A range of length 0 or 1 returns in O(1).
    Otherwise one partition costs O(n), then the two sides are sorted. A
    balanced pivot gives ``T(n) = 2 T(n/2) + O(n) = O(n log n)``, which is
    the expected case for a random pivot. A pivot that always lands at an
    end gives ``T(n) = T(n - 1) + O(n) = O(n²)``. The call stack follows the
    deeper side: expected O(log n) frames, O(n) frames in that worst split.
    """

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

    Cost
    ----
    Let k be ``end - start``, the number of indexes scanned. Choosing the
    pivot and swapping it to the end is O(1). The loop runs k times and each
    body is one comparison and at most one swap, both O(1). The final pivot
    swap is O(1). Time is O(k). No extra list is allocated: O(1) memory.
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
