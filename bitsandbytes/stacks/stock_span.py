"""Stock span: how many consecutive earlier prices are still ``<=`` today.

The span at day ``i`` is the number of days ending at ``i`` whose price is
less than or equal to ``prices[i]``. A decreasing stack stores the indexes
of prices that are still candidates for a strictly higher later day. When
today is greater than or equal to the price on top, that day is inside
today's span and is popped. The new top is the nearest earlier day that
today does not cover, and the span is the distance to it.

The same counting argument as next-greater applies: each day is pushed once
and popped at most once.
"""

from __future__ import annotations

from collections.abc import Sequence


def stock_spans(prices: Sequence[int]) -> list[int]:
    """Return the span ending at each day.

    A single day has span 1. Equal prices count, so a run of identical
    prices grows the span by one each day.

    Cost
    ----
    Let n be ``len(prices)``. The outer loop runs n times. The inner loop
    pops, and each index is pushed once and popped at most once, so those
    pops total at most n over the whole call. Each step computes a
    subtraction in O(1). Time is O(n). A day-by-day scan backward would
    instead sum up to ``n(n + 1) / 2`` comparisons, O(n²). The stack stores
    at most n indexes: O(n) extra memory. The returned list is the result
    and also holds n integers.
    """

    spans: list[int] = []
    # Indexes of a strictly decreasing run of prices. The top is the nearest
    # earlier day that might still sit outside today's span.
    candidates: list[int] = []
    for index, price in enumerate(prices):
        while candidates and prices[candidates[-1]] <= price:
            candidates.pop()
        if not candidates:
            # Nothing to the left is strictly higher, so the span reaches
            # the first day.
            span = index + 1
        else:
            span = index - candidates[-1]
        spans.append(span)
        candidates.append(index)
    return spans
