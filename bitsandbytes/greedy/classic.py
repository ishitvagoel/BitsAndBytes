"""Greedy algorithms with exchange arguments."""

from __future__ import annotations

import heapq
from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(order=True, slots=True)
class _Interval:
    finish: int
    start: int
    label: str = ""


def interval_scheduling_max_count(intervals: Sequence[tuple[int, int, str]]) -> int:
    """Return the size of a maximum set of non-overlapping intervals.

    Sort by finish time, then greedily take compatible intervals.

    Cost
    ----
    O(n log n) sort, O(n) scan, O(1) extra memory besides output count.
    """

    ordered = sorted(_Interval(finish, start, label) for start, finish, label in intervals)
    count = 0
    last_finish = float("-inf")
    for interval in ordered:
        if interval.start >= last_finish:
            count += 1
            last_finish = interval.finish
    return count


def fractional_knapsack_value(
    weights: Sequence[int],
    values: Sequence[int],
    capacity: int,
) -> float:
    """Return maximum value when fractions of items are allowed.

    Cost
    ----
    O(n log n) to sort by value/weight ratio, O(n) greedy fill.
    """

    ratios = sorted(
        (values[index] / weights[index], weights[index], values[index])
        for index in range(len(weights))
    )
    remaining = capacity
    total = 0.0
    for ratio, weight, value in ratios:
        if remaining <= 0:
            break
        take = min(weight, remaining)
        total += ratio * take
        remaining -= take
    return total


def huffman_codes(frequencies: dict[str, int]) -> dict[str, str]:
    """Return optimal prefix codes for symbol frequencies.

    Cost
    ----
    O(n log n) with a min-heap of n leaves, O(n) output size.
    """

    if not frequencies:
        return {}
    if len(frequencies) == 1:
        symbol = next(iter(frequencies))
        return {symbol: "0"}
    heap: list[tuple[int, int, dict[str, str]]] = []
    counter = 0
    for symbol, weight in frequencies.items():
        heapq.heappush(heap, (weight, counter, {symbol: ""}))
        counter += 1
    while len(heap) > 1:
        left_weight, _, left_codes = heapq.heappop(heap)
        right_weight, _, right_codes = heapq.heappop(heap)
        merged: dict[str, str] = {}
        for symbol, bits in left_codes.items():
            merged[symbol] = "0" + bits
        for symbol, bits in right_codes.items():
            merged[symbol] = "1" + bits
        heapq.heappush(heap, (left_weight + right_weight, counter, merged))
        counter += 1
    return heap[0][2]
