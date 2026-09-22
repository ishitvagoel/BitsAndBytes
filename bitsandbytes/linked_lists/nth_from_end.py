"""Reach the nth node from the end without measuring the list first.

Keep two pointers ``n`` nodes apart and walk them together. When the leader
falls off the end, the trailer is the nth node from the tail. That is one
pass, which is the same cost as counting the length and then walking
``length - n``, but the gap removes the subtraction and makes "remove the nth
from the end" a natural next step.

``n`` is 1-based: ``1`` is the tail. An anchor node in front of the head lets
removal treat the real head like any other node. The anchor's stored value is
never read.

Time O(n), extra memory O(1).
"""

from __future__ import annotations

from typing import TypeVar

from bitsandbytes.linked_list import LinkedList, Node

T = TypeVar("T")


def nth_from_end(lst: LinkedList[T], n: int) -> Node[T]:
    """Return the node ``n`` places from the tail, counting the tail as 1.

    Cost
    ----
    Let L be the length. The leader first takes ``n`` steps, then both
    pointers take ``L - n`` steps together. Total steps: n + 2 * (L - n),
    which is O(L). Each step is O(1). Extra memory is the two references:
    O(1). Counting the length first and then walking ``L - n`` is also O(L);
    the gap removes the subtraction but not the linear scan.
    """

    _require_positive(n)
    lst.require_linear()
    leader = lst.head
    for _ in range(n):
        if leader is None:
            raise ValueError("n is larger than the list.")
        leader = leader.next

    trailer = lst.head
    while leader is not None:
        assert trailer is not None and trailer.next is not None
        leader = leader.next
        trailer = trailer.next
    if trailer is None:
        raise ValueError("n is larger than the list.")
    return trailer


def remove_nth_from_end(lst: LinkedList[T], n: int) -> T:
    """Remove the nth node from the tail and return its value.

    Cost
    ----
    Same two-pointer walk as ``nth_from_end``: O(L) steps for a list of
    length L, each O(1). The unlink and ``refresh`` are another O(L) walk.
    Total time O(L). The anchor is one extra node: O(1) extra memory.
    """

    _require_positive(n)
    lst.require_linear()
    if lst.head is None:
        raise ValueError("n is larger than the list.")

    # The anchor is not part of the list. ``leader`` starts here so that
    # after ``n`` steps it sits on the nth node, and the trailer can stop
    # on the node *before* the one to delete.
    anchor: Node[T] = Node(lst.head.data, lst.head)
    leader: Node[T] | None = anchor
    for _ in range(n):
        if leader is None or leader.next is None:
            raise ValueError("n is larger than the list.")
        leader = leader.next

    trailer = anchor
    while leader.next is not None:
        leader = leader.next
        assert trailer.next is not None
        trailer = trailer.next

    removed = trailer.next
    assert removed is not None
    trailer.next = removed.next
    removed.next = None
    lst.head = anchor.next
    lst.refresh()
    return removed.data


def _require_positive(n: int) -> None:
    """Reject a non-positive or non-integer ``n``.

    Cost
    ----
    A constant number of type and range checks: O(1) time, O(1) extra memory.
    """

    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("n must be a positive integer.")
