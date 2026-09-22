"""Sort a stack using one extra stack.

No random access and no second data structure beyond that stack. Each item
is moved to the extra stack, which keeps larger values above smaller ones.
If the extra stack's top is larger than the item being inserted, those
larger values move back to the input until the hole is on top, then the
item is pushed. That is insertion sort, with the extra stack as the sorted
prefix.

When the input is empty the extra stack has the largest value on top.
Pouring it back onto the input reverses that order, so the smallest value
ends on top and ``pop`` yields non-decreasing values.
"""

from __future__ import annotations

from typing import TypeVar

from bitsandbytes.stacks.algorithm_stack import AlgorithmStack
from bitsandbytes.stacks.stack import Stack

T = TypeVar("T")


def sort_stack(stack: Stack[T]) -> Stack[T]:
    """Sort ``stack`` so the smallest item is on top. Returns the same stack.

    Uses an :class:`~bitsandbytes.stacks.algorithm_stack.AlgorithmStack` as
    the extra stack so the lesson is not tied to a capacity limit. The input
    ``stack`` must still have room for items moved back during insertion.
    Ties keep the item that was already on the extra stack above the new
    one only when it is strictly larger; equal items are not moved again.

    Cost
    ----
    Let n be ``len(stack)``. The outer loop pops each of the n items once.
    Inserting item ``k`` may pop every value already on the extra stack and
    later push them again. In the worst case (input pops in ascending order,
    so each new item is smaller than everything already sorted) that scan
    walks ``k - 1`` items. The sum is ``0 + 1 + ... + (n - 1) = n(n - 1) / 2``,
    so worst-case time is O(n²). Each move is one ``pop`` and one ``push``,
    both O(1). Worst case happens when pops from the input arrive in strictly
    decreasing order (each new item is smaller than everything on the extra
    stack). Best case (strictly increasing pop order) never rewinds: O(n).
    The extra stack holds every item by
    the end of the first loop, so extra memory is O(n). The final pour is
    another n pops and n pushes, O(n), which does not change the bound.
    """

    ordered: AlgorithmStack[T] = AlgorithmStack()
    while not stack.is_empty:
        current = stack.pop()
        # Move strictly larger sorted values back. They belong above
        # ``current`` once ``current`` has been pushed.
        while not ordered.is_empty and ordered.peek() > current:
            stack.push(ordered.pop())
        ordered.push(current)
    while not ordered.is_empty:
        stack.push(ordered.pop())
    return stack
