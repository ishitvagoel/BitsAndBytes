"""Binary search on a sorted sequence.

After the comparison sorts, a sorted array is useful only if you can reach
one index in logarithmic time. Each step compares the middle element with
the target and discards half the remaining range.

Worked trace (``binary_search`` on ``[1, 3, 5, 7, 9]``, target ``7``):

* Range ``[0, 4]``, middle index 2, value 5. ``7 > 5``, search ``[3, 4]``.
* Range ``[3, 4]``, middle index 3, value 7. Match at index 3.

``lower_bound`` is the first index whose value is ``>=`` target. ``upper_bound``
is the first index whose value is ``>`` target. On duplicates they differ by
one index.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


def binary_search(sorted_values: Sequence[T], target: T) -> int:
    """Return the index of ``target``, or ``-1`` if it is absent.

    ``sorted_values`` must be non-decreasing under ``<``.

    Cost
    ----
    Let n be ``len(sorted_values)``. Each iteration halves the remaining
    range, so there are at most ``floor(log2(n)) + 1`` iterations. Each
    body is one comparison and O(1) index arithmetic. Time is O(log n).
    A few integer indexes are stored: O(1) extra memory.
    """

    left = 0
    right = len(sorted_values) - 1
    while left <= right:
        middle = left + (right - left) // 2
        middle_value = sorted_values[middle]
        if middle_value < target:
            left = middle + 1
        elif target < middle_value:
            right = middle - 1
        else:
            return middle
    return -1


def lower_bound(sorted_values: Sequence[T], target: T) -> int:
    """Return the first index ``i`` with ``sorted_values[i] >= target``.

    If every value is smaller than ``target``, return ``len(sorted_values)``.

    Cost
    ----
    Same halving argument as ``binary_search``: O(log n) time, O(1) extra
    memory. The loop keeps the invariant that the answer lies in ``[left, right]``.
    """

    left = 0
    right = len(sorted_values)
    while left < right:
        middle = left + (right - left) // 2
        if sorted_values[middle] < target:
            left = middle + 1
        else:
            right = middle
    return left


def upper_bound(sorted_values: Sequence[T], target: T) -> int:
    """Return the first index ``i`` with ``sorted_values[i] > target``.

    Cost
    ----
    One comparison direction changes: test ``<=`` instead of ``<``. Still
    O(log n) time and O(1) extra memory.
    """

    left = 0
    right = len(sorted_values)
    while left < right:
        middle = left + (right - left) // 2
        if sorted_values[middle] <= target:
            left = middle + 1
        else:
            right = middle
    return left
