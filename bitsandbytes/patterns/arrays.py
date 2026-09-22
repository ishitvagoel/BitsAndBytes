"""Array patterns: two pointers, sliding window, prefix sums, monotonic queue."""

from __future__ import annotations

from collections import deque
from collections.abc import Sequence


def two_sum_sorted(sorted_values: Sequence[int], target: int) -> tuple[int, int] | None:
    """Return indices of two values summing to ``target`` on a sorted array.

    Cost
    ----
    O(n) time, O(1) memory.
    """

    left = 0
    right = len(sorted_values) - 1
    while left < right:
        total = sorted_values[left] + sorted_values[right]
        if total == target:
            return left, right
        if total < target:
            left += 1
        else:
            right -= 1
    return None


def longest_unique_substring_length(text: str) -> int:
    """Return length of the longest substring without repeating characters.

    Cost
    ----
    O(n) sliding window; each index enters and leaves once.
    """

    last_seen: dict[str, int] = {}
    best = 0
    start = 0
    for index, char in enumerate(text):
        if char in last_seen and last_seen[char] >= start:
            start = last_seen[char] + 1
        last_seen[char] = index
        best = max(best, index - start + 1)
    return best


class PrefixSum:
    """Prefix sums for O(1) range queries on a fixed array."""

    def __init__(self, values: Sequence[int]) -> None:
        """Build prefix totals.

        Cost
        ----
        O(n) time and memory.
        """

        self._totals = [0]
        for value in values:
            self._totals.append(self._totals[-1] + value)

    def range_sum(self, start: int, end: int) -> int:
        """Return sum of ``values[start:end]`` (end exclusive).

        Cost
        ----
        O(1).
        """

        return self._totals[end] - self._totals[start]


def sliding_window_maximum(values: Sequence[int], window: int) -> list[int]:
    """Return the maximum in each sliding window of size ``window``.

    Cost
    ----
    O(n) with a monotonic deque storing candidate indices.
    """

    if window < 1:
        raise ValueError("window must be at least 1.")
    deque_indices: deque[int] = deque()
    output: list[int] = []
    for index, value in enumerate(values):
        while deque_indices and values[deque_indices[-1]] <= value:
            deque_indices.pop()
        deque_indices.append(index)
        front = index - window + 1
        if deque_indices[0] < front:
            deque_indices.popleft()
        if index >= window - 1:
            output.append(values[deque_indices[0]])
    return output
