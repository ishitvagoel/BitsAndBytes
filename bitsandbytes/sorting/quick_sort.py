"""Quick sort with a random pivot (Lomuto partition).

Pick a random index, move it to the end, and walk the range once. Every value
less than or equal to the pivot is swapped into the left side. The pivot then
drops into the boundary and is in its final position. Recurse on the two sides.

A random pivot makes a sorted list of distinct keys expected O(n log n) instead
of the O(n^2) trap of always pivoting on the last element. Lomuto still sends
every equal key to the left of the pivot, so an all-equal list of length n
gives ``T(n) = T(n - 1) + O(n) = O(n^2)`` for any pivot index. Use
``quick_sort_three_way`` when duplicates are common. Extra memory is the
recursion stack, expected O(log n).

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
    the expected case for a random pivot on distinct keys. A pivot that always
    lands at an end gives ``T(n) = T(n - 1) + O(n) = O(n²)``. When every
    value equals the pivot, Lomuto leaves an empty right side every time, so
    the same ``T(n - 1) + O(n)`` recurrence applies. The call stack follows the
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


def quick_sort_three_way(
    values: list[T],
    *,
    rng: random.Random | None = None,
) -> list[T]:
    """Sort ``values`` in ascending order with a three-way partition.

    Equal keys are gathered in the middle, so an all-equal list is sorted in
    one partition pass instead of the Lomuto ``T(n - 1) + O(n)`` trap.

    Cost
    ----
    Let n be ``len(values)``. Each level scans its range once to split into
    less, equal, and greater. With many duplicates the equal middle shrinks
    the recursive work; an all-equal range finishes in O(n) time total for
    that range. Distinct keys behave like a usual quick sort: expected
    O(n log n), worst O(n²) if every split is lopsided. Extra memory is the
    recursion stack: expected O(log n), worst O(n). Not stable.
    """

    choose = random.randint if rng is None else rng.randint
    _quick_sort_three_way(values, 0, len(values) - 1, choose)
    return values


def _quick_sort_three_way(
    values: list[T],
    start: int,
    end: int,
    choose: Chooser,
) -> None:
    """Sort ``values[start:end + 1]`` with less / equal / greater buckets.

    Cost
    ----
    One call to ``_three_way_partition`` is O(end - start + 1). When the
    equal bucket has length k, only the less and greater sides recurse, so
    duplicate-heavy input avoids the Lomuto one-sided ``T(n - 1) + O(n)``
    recurrence. Distinct keys still follow the usual quick-sort bounds.
    """

    if start >= end:
        return
    less_end, greater_start = _three_way_partition(values, start, end, choose)
    _quick_sort_three_way(values, start, less_end - 1, choose)
    _quick_sort_three_way(values, greater_start + 1, end, choose)


def _three_way_partition(
    values: list[T],
    start: int,
    end: int,
    choose: Chooser,
) -> tuple[int, int]:
    """Partition into ``< pivot``, ``== pivot``, and ``> pivot``.

    Returns the inclusive equal range ``[less_end, greater_start]``.

    Cost
    ----
    Let k be ``end - start``. The index ``i`` advances at most k times, and
    each step does O(1) work. Swaps only move items among the three regions.
    Time O(k), extra memory O(1).
    """

    pivot_index = choose(start, end)
    pivot = values[pivot_index]
    values[start], values[pivot_index] = values[pivot_index], values[start]

    less = start
    greater = end
    index = start + 1
    while index <= greater:
        if values[index] < pivot:
            values[less], values[index] = values[index], values[less]
            less += 1
            index += 1
        elif values[index] > pivot:
            values[index], values[greater] = values[greater], values[index]
            greater -= 1
        else:
            index += 1
    return less, greater
