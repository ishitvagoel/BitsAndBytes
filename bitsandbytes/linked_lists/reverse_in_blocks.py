"""Reverse a linear linked list in successive blocks of ``k`` nodes.

``1..15`` reversed in blocks of 4 becomes

``4 3 2 1 | 8 7 6 5 | 12 11 10 9 | 15 14 13``.

The tail block is reversed too when it is shorter than ``k``. Pass
``reverse_remainder=False`` to leave that tail in its original order, which
is the usual "reverse nodes in k-group" interview variant.
"""

from __future__ import annotations

from typing import TypeVar

from bitsandbytes.linked_list import LinkedList, Node

T = TypeVar("T")


def reverse_in_blocks(
    lst: LinkedList[T],
    k: int,
    *,
    reverse_remainder: bool = True,
) -> None:
    """Reverse every block of ``k`` nodes in ``lst``.

    ``k`` of 1 leaves the list unchanged. A non-positive ``k`` is rejected.

    Cost
    ----
    There are about n / k blocks. Counting a block looks at k nodes, and
    reversing it rewrites k pointers. Across every block the counts and the
    reversals each touch each node a constant number of times, so both are
    O(n), not O(n * k). ``require_linear`` and ``refresh`` are O(n). Total
    time O(n). The anchor and a few references are O(1) extra memory.
    """

    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive integer.")
    lst.require_linear()
    if lst.head is None or k == 1:
        return

    anchor: Node[T] = Node(lst.head.data, lst.head)
    group_previous = anchor
    while group_previous.next is not None:
        available = _count_available(group_previous.next, k)
        if available < k and not reverse_remainder:
            break
        new_head, new_tail, following = _reverse_prefix(group_previous.next, available)
        group_previous.next = new_head
        new_tail.next = following
        group_previous = new_tail

    lst.head = anchor.next
    lst.refresh()


def _count_available(node: Node[T] | None, limit: int) -> int:
    """Count nodes from ``node``, stopping at ``limit``.

    Cost
    ----
    The loop runs at most ``limit`` times and each step follows one ``next``.
    Time O(limit), extra memory O(1).
    """

    available = 0
    while node is not None and available < limit:
        node = node.next
        available += 1
    return available


def _reverse_prefix(
    head: Node[T] | None,
    count: int,
) -> tuple[Node[T], Node[T], Node[T] | None]:
    """Reverse ``count`` nodes starting at ``head``.

    Returns the new head, the new tail (the old head), and the first node
    that was not part of the prefix.

    Cost
    ----
    The loop runs ``count`` times. Each iteration rewrites one ``next``:
    O(count) time, O(1) extra memory.
    """

    previous: Node[T] | None = None
    current = head
    for _ in range(count):
        assert current is not None
        upcoming = current.next
        current.next = previous
        previous = current
        current = upcoming
    assert previous is not None and head is not None
    return previous, head, current
