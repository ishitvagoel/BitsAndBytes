"""Largest rectangle inside a histogram.

Each bar is a candidate for the shortest bar of some rectangle. That
rectangle extends left and right until a strictly shorter bar. A stack of
indexes keeps bar heights increasing from bottom to top. When a shorter bar
arrives, every taller bar on the stack ends here: its right edge is the new
index, and its left edge is the index now underneath it.

A sentinel index of -1 stands for "no bar to the left", so the width formula
does not special-case an empty stack. Bars still on the stack after the scan
extend all the way to the last index.

Worked trace on ``[2, 1, 5, 6, 2, 3]`` when index 4 (height 2) arrives:

* Pop index 3 (height 6): the bar still underneath is index 2, so the width is
  ``4 - 2 - 1 = 1`` and the area is 6.
* Pop index 2 (height 5): the bar underneath is index 1, so the width is
  ``4 - 1 - 1 = 2`` and the area is 10 (best so far).
* Push index 4. Later pops finish bars still on the stack at the right edge.
"""

from __future__ import annotations

from collections.abc import Sequence


def largest_rectangle(heights: Sequence[int]) -> int:
    """Return the area of the largest rectangle that fits in ``heights``.

    An empty histogram has area 0. A bar of height 0 contributes nothing and
    also stops rectangles from crossing it.

    Cost
    ----
    Let n be ``len(heights)``. The first loop runs n times. Each index is
    pushed once and popped at most once, either in that loop or in the
    final drain, so the pops across both loops total at most n. Each pop
    computes one width and one area in O(1). Time is O(n). Checking every
    pair of left and right edges would be ``n(n + 1) / 2`` ranges, O(n²).
    The stack holds at most n indexes plus the sentinel: O(n) extra memory.
    """

    # -1 is not a bar. It lets ``index - left - 1`` be the width when a
    # rectangle reaches the first column.
    pending: list[int] = [-1]
    best = 0
    for index, height in enumerate(heights):
        while pending[-1] != -1 and heights[pending[-1]] >= height:
            best = max(best, _area(heights, pending, index))
        pending.append(index)

    # Bars left on the stack are not blocked on the right. Their right edge
    # is just past the last column.
    right = len(heights)
    while pending[-1] != -1:
        best = max(best, _area(heights, pending, right))
    return best


def _area(heights: Sequence[int], pending: list[int], right: int) -> int:
    """Pop one finished bar and return the rectangle it limits.

    Cost
    ----
    One pop, two subtractions, and one multiplication. O(1) time and O(1)
    extra memory. ``right`` is the first index the popped bar does not cover.
    """

    top = pending.pop()
    width = right - pending[-1] - 1
    return heights[top] * width
