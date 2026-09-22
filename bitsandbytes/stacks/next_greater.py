"""Next greater element to the right, using a monotonic stack.

For each position, the answer is the nearest later value that is strictly
greater, or ``None`` when no later value qualifies. A decreasing
:class:`~bitsandbytes.stacks.algorithm_stack.AlgorithmStack` of indexes waits
for that greater value. When a larger value arrives, every index it beats is
popped and answered. Indexes that are still waiting at the end have no
greater element.

Each index is pushed once and popped at most once, so the nested loop does
not make the whole scan quadratic.

Worked trace on ``[2, 1, 2, 4, 3]`` (stack holds indexes, bottom to top):

* Index 0 (2): stack ``[0]``.
* Index 1 (1): no pop; stack ``[0,1]``.
* Index 2 (2): pop 1, answer[1]=2; stack ``[0,2]``.
* Index 3 (4): pop 2 and 0, answer[2]=4, answer[0]=4; stack ``[3]``.
* Index 4 (3): no pop; stack ``[3,4]``. Index 4 stays unanswered.
"""

from __future__ import annotations

from collections.abc import Sequence

from bitsandbytes.stacks.algorithm_stack import AlgorithmStack


def next_greater(values: Sequence[int]) -> list[int | None]:
    """Return the next strictly greater value to the right of each item.

    Cost
    ----
    Let n be ``len(values)``. The result list is allocated once: O(n).
    The outer loop runs n times. The inner loop pops the stack, and each
    index is pushed once and popped at most once, so those pops total at
    most n across the whole call. Each body is O(1). Time is O(n). The
    ``AlgorithmStack`` holds at most n indexes: O(n) extra memory.
    """

    answer: list[int | None] = [None] * len(values)
    pending: AlgorithmStack[int] = AlgorithmStack()
    for index, value in enumerate(values):
        while not pending.is_empty and values[pending.peek()] < value:
            answer[pending.pop()] = value
        pending.push(index)
    return answer
