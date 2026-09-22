"""Detect whether a linked list is a palindrome, in O(1) extra memory.

Find the end of the first half with the slow/fast split in ``middle.py``,
reverse the second half, and compare the two sides. The second half is
reversed again before returning, so the list the caller passed in is unchanged.

An odd-length list keeps its middle node in the first half. The comparison
stops when the shorter second half ends, so the middle value is not paired
with anything. Empty and single-node lists are palindromes.

The previous recursive version returned a ``(bool, node)`` pair and crashed
on an empty list because it read through a sentinel that this package no
longer uses.

Worked trace on ``[1, 2, 2, 1]``: ``end_of_first_half`` stops at the first
``2``. Reverse the suffix ``2 → 1``, compare ``1,2`` with ``2,1``, then
reverse the suffix back so the list reads ``1 → 2 → 2 → 1`` again.
"""

from __future__ import annotations

from typing import TypeVar

from bitsandbytes.linked_list import LinkedList, Node
from bitsandbytes.linked_lists.middle import end_of_first_half

T = TypeVar("T")


def is_palindrome(lst: LinkedList[T]) -> bool:
    """Return whether the values in ``lst`` read the same forwards and backwards.

    Cost
    ----
    ``require_linear`` and ``end_of_first_half`` are each O(n). Reversing the
    second half touches at most n / 2 nodes, and comparing the halves does
    the same. Restoring the second half is one more O(n) reverse. A constant
    number of O(n) passes is O(n) time. Only a few node references are
    stored: O(1) extra memory. The recursive palindrome used O(n) call-stack
    frames; this one does not.
    """

    lst.require_linear()
    if lst.head is None or lst.head.next is None:
        return True

    first_half_end = end_of_first_half(lst.head)
    second_head = _reverse(first_half_end.next)
    try:
        return _same_prefix(lst.head, second_head)
    finally:
        # Reverse the second half back so the call is not destructive.
        first_half_end.next = _reverse(second_head)


def _reverse(head: Node[T] | None) -> Node[T] | None:
    """Reverse the chain at ``head`` and return the new head.

    Cost
    ----
    k nodes in the chain produce k iterations, each one pointer write.
    Time O(k), extra memory O(1).
    """

    previous: Node[T] | None = None
    current = head
    while current is not None:
        upcoming = current.next
        current.next = previous
        previous = current
        current = upcoming
    return previous


def _same_prefix(left: Node[T] | None, right: Node[T] | None) -> bool:
    """Compare values until the right-hand chain ends.

    Cost
    ----
    Let k be the length of the right chain. The loop runs at most k times
    and each comparison is O(1). Time O(k), extra memory O(1). It stops at
    the first mismatch, so a difference at the front is O(1).
    """

    while right is not None:
        if left is None or left.data != right.data:
            return False
        left = left.next
        right = right.next
    return True
