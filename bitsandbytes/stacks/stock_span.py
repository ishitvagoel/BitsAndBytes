"""Stock span: how many consecutive earlier prices are still ``<=`` today.

The span at day ``i`` is the number of days ending at ``i`` whose price is
less than or equal to ``prices[i]``. A decreasing
:class:`~bitsandbytes.stacks.algorithm_stack.AlgorithmStack` stores the
indexes of prices that are still candidates for a strictly higher later day.

The same counting argument as next-greater applies: each day is pushed once
and popped at most once.
"""

from __future__ import annotations

from collections.abc import Sequence

from bitsandbytes.stacks.algorithm_stack import AlgorithmStack


def stock_spans(prices: Sequence[int]) -> list[int]:
    """Return the span ending at each day.

    A single day has span 1. Equal prices count, so a run of identical
    prices grows the span by one each day.

    Cost
    ----
    Let n be ``len(prices)``. The outer loop runs n times. Each index is
    pushed once and popped at most once, so those pops total at most n.
    Time is O(n). The ``AlgorithmStack`` holds at most n indexes: O(n)
    extra memory besides the result list.
    """

    spans: list[int] = []
    candidates: AlgorithmStack[int] = AlgorithmStack()
    for index, price in enumerate(prices):
        while not candidates.is_empty and prices[candidates.peek()] <= price:
            candidates.pop()
        if candidates.is_empty:
            span = index + 1
        else:
            span = index - candidates.peek()
        spans.append(span)
        candidates.push(index)
    return spans
