"""Selection sort.

For each position, scan the rest of the list, remember the index of the
extreme value, and swap once. The previous version swapped on every
improvement inside the inner loop. That still ordered the values, but it did
more writes than selection sort and was harder to tell apart from bubble sort.

Time: O(n^2) comparisons regardless of input order. O(1) extra memory.
Not stable. Sorts in place and returns the same list.
"""

from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def selection_sort(values: list[T], *, reverse: bool = False) -> list[T]:
    """Sort ``values`` in place.

    ``reverse=False`` sorts ascending. ``reverse=True`` sorts descending, which
    replaces the old ``asc`` flag so the call matches ``sorted(..., reverse=)``.

    Cost
    ----
    Let n be ``len(values)``. The outer loop runs ``n - 1`` times. On step
    ``i`` (``i`` from 0) the inner loop compares ``n - 1 - i`` candidates, so
    the comparison count is always ``(n - 1) + (n - 2) + ... + 1 = n(n - 1) / 2``.
    Input order does not change that sum: best, typical, and worst time are
    all O(n²). At most one swap happens per outer index, which is O(n) writes
    and does not change the bound. A handful of indexes is O(1) extra memory.
    """

    last_index = len(values) - 1
    for index in range(last_index):
        selected = index
        for candidate in range(index + 1, len(values)):
            # One comparison direction covers both orders: look for a strictly
            # smaller item when ascending, and a strictly larger one otherwise.
            if reverse:
                outranks = values[selected] < values[candidate]
            else:
                outranks = values[candidate] < values[selected]
            if outranks:
                selected = candidate
        if selected != index:
            values[index], values[selected] = values[selected], values[index]
    return values
