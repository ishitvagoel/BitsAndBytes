"""Next greater element to the right, using a monotonic stack.

For each position, the answer is the nearest later value that is strictly
greater, or ``None`` when no later value qualifies. A decreasing stack of
indexes waits for that greater value. When a larger value arrives, every
index it beats is popped and answered. Indexes that are still waiting at the
end have no greater element.

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


def next_greater(values: Sequence[int]) -> list[int | None]:
    """Return the next strictly greater value to the right of each item.

    Cost
    ----
    Let n be ``len(values)``. The result list is allocated once: O(n).
    The outer loop runs n times. The inner loop pops the stack, and each
    index is appended once and popped at most once, so the inner loop runs
    at most n times across the whole call, not n times per index. Each body
    is O(1). Time is O(n) + O(n) = O(n), where a nested scan of the right
    side would have been ``1 + 2 + ... + n = n(n + 1) / 2``, which is O(n²).
    The stack holds at most n indexes, so extra memory is O(n).
    """

    answer: list[int | None] = [None] * len(values)
    # Indexes whose next greater value has not been seen. Their values are
    # strictly decreasing from bottom to top: a larger value would already
    # have resolved the smaller indexes underneath it.
    pending: list[int] = []
    for index, value in enumerate(values):
        while pending and values[pending[-1]] < value:
            answer[pending.pop()] = value
        pending.append(index)
    return answer
