"""Binary search on a sorted sequence.

After the comparison sorts, a sorted array is useful only if you can reach
one index in logarithmic time. Each step compares the middle element with
the target and discards half the remaining range.

Worked trace (``binary_search`` on ``[1, 3, 5, 7, 9]``, target ``7``):

* Range ``[0, 4]``, middle index 2, value 5. ``7 > 5``, search ``[3, 4]``.
* Range ``[3, 4]``, middle index 3, value 7. Match at index 3.

``lower_bound`` is the first index whose value is ``>=`` target. ``upper_bound``
is the first index whose value is ``>`` target. Their difference is the number
of matching values. For ``[1, 2, 2, 2, 3]`` and target ``2``, the bounds are
1 and 4, so there are ``4 - 1 = 3`` matches.

Industry
--------
A working engineer searches a sorted list with ``bisect.bisect_left``, which
returns the insertion point to the left of any matching entries. The
``bisect`` documentation states that this search is O(log n). ``insort`` is
O(n) only because the following list insertion moves elements.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TypeVar

T = TypeVar("T")


# BEGIN LEARNING EXCERPT: binary-search
def binary_search(sorted_values: Sequence[T], target: T) -> int:
    """Return the index of ``target``, or ``-1`` if it is absent.

    ``sorted_values`` must be non-decreasing under ``<``.

    Cost
    ----
    Let n be ``len(sorted_values)``. For n >= 1, each iteration halves the
    remaining range, so there are at most ``floor(log2(n)) + 1`` iterations.
    An empty sequence takes no iterations. Each iteration uses at most two
    value comparisons and O(1) index arithmetic. Time is O(log n) for
    non-empty input.
    A few integer indexes are stored: O(1) extra memory.
    """

    # TRACE:initialize
    left = 0
    right = len(sorted_values) - 1
    # TRACE:compare-left
    while left <= right:
        middle = left + (right - left) // 2
        middle_value = sorted_values[middle]
        if middle_value < target:
            # TRACE:narrow-left
            left = middle + 1
        # TRACE:compare-right
        elif target < middle_value:
            # TRACE:narrow-right
            right = middle - 1
        # TRACE:return-match
        else:
            return middle
    # TRACE:return-absent
    return -1
# END LEARNING EXCERPT: binary-search


def _binary_search_trace_impl(
    sorted_values: Sequence[T],
    target: T,
    trace_sink: Callable[[dict[str, object]], None],
) -> int:
    trace_sink({
        "left": 0,
        "right": len(sorted_values) - 1,
        "middle": None,
        "inspected": None,
        "message": (
            f"Start with every index from 0 through {len(sorted_values) - 1} as a possible answer."
            if sorted_values else "The list is empty, so there are no indexes to inspect."
        ),
        "result": "range",
        "codeStep": "initialize",
    })

    left = 0
    right = len(sorted_values) - 1
    while left <= right:
        middle = left + (right - left) // 2
        middle_value = sorted_values[middle]
        if middle_value < target:
            trace_sink({
                "left": left,
                "right": right,
                "middle": middle,
                "inspected": middle,
                "message": f"{middle_value} is smaller than {target}. Sorted order means indexes {left} through {middle} are too small; the next step removes them.",
                "result": "continue",
                "codeStep": "compare-left",
            })
            next_left = middle + 1
            trace_sink({
                "left": next_left,
                "right": right,
                "middle": None,
                "inspected": middle,
                "message": f"{middle_value} is too small. Because the list is sorted, indexes {left} through {middle} are too small; keep indexes {next_left} through {right}.",
                "result": "continue",
                "codeStep": "narrow-left",
            })
            left = next_left
        elif target < middle_value:
            trace_sink({
                "left": left,
                "right": right,
                "middle": middle,
                "inspected": middle,
                "message": f"{middle_value} is larger than {target}. Sorted order means indexes {middle} through {right} are too large; the next step removes them.",
                "result": "continue",
                "codeStep": "compare-right",
            })
            next_right = middle - 1
            trace_sink({
                "left": left,
                "right": next_right,
                "middle": None,
                "inspected": middle,
                "message": f"{middle_value} is too large. Because the list is sorted, indexes {middle} through {right} are too large; keep indexes {left} through {next_right}.",
                "result": "continue",
                "codeStep": "narrow-right",
            })
            right = next_right
        else:
            trace_sink({
                "left": left,
                "right": right,
                "middle": middle,
                "inspected": middle,
                "message": f"Index {middle} contains {middle_value}. The target is found.",
                "result": "found",
                "codeStep": "return-match",
            })
            return middle
    trace_sink({
        "left": left,
        "right": right,
        "middle": None,
        "inspected": None,
        "message": f"The possible range is empty, so {target} is not in this list.",
        "result": "missing",
        "codeStep": "return-absent",
    })
    return -1


def binary_search_trace(sorted_values: Sequence[T], target: T) -> tuple[int, list[dict[str, object]]]:
    """Run binary search and collect pointer/message states for a lesson trace."""

    frames: list[dict[str, object]] = []
    result = _binary_search_trace_impl(sorted_values, target, frames.append)
    return result, frames


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
    One comparison direction changes: move right unless ``target < value``.
    Only ``<`` is needed, as for the other search functions. Still O(log n)
    time and O(1) extra memory.
    """

    left = 0
    right = len(sorted_values)
    while left < right:
        middle = left + (right - left) // 2
        if target < sorted_values[middle]:
            right = middle
        else:
            left = middle + 1
    return left
