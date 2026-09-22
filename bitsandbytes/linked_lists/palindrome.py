"""Detect whether a linked list is a palindrome, in O(1) extra memory.

Find the end of the first half with a slow and a fast pointer, reverse the
second half, and compare the two sides. The second half is reversed again
before returning, so the list the caller passed in is unchanged.

An odd-length list keeps its middle node in the first half. The comparison
stops when the shorter second half ends, so the middle value is not paired
with anything. Empty and single-node lists are palindromes.

The previous recursive version returned a ``(bool, node)`` pair and crashed
on an empty list because it read through a sentinel that this package no
longer uses.
"""

from __future__ import annotations

from typing import TypeVar

from bitsandbytes.linked_list import LinkedList, Node

T = TypeVar("T")


def is_palindrome(lst: LinkedList[T]) -> bool:
    """Return whether the values in ``lst`` read the same forwards and backwards."""

    lst.require_linear()
    if lst.head is None or lst.head.next is None:
        return True

    first_half_end = _end_of_first_half(lst.head)
    second_head = _reverse(first_half_end.next)
    try:
        return _same_prefix(lst.head, second_head)
    finally:
        # Reverse the second half back so the call is not destructive.
        first_half_end.next = _reverse(second_head)


def _end_of_first_half(head: Node[T]) -> Node[T]:
    """Return the last node of the first half.

    On an odd-length list that node is the middle. On an even-length list it
    is the last node of the left half. The fast pointer moves two steps, so
    it reaches the end when the slow pointer has covered half the nodes.
    """

    slow = head
    fast = head
    while fast.next is not None and fast.next.next is not None:
        assert slow.next is not None
        slow = slow.next
        fast = fast.next.next
    return slow


def _reverse(head: Node[T] | None) -> Node[T] | None:
    previous: Node[T] | None = None
    current = head
    while current is not None:
        upcoming = current.next
        current.next = previous
        previous = current
        current = upcoming
    return previous


def _same_prefix(left: Node[T] | None, right: Node[T] | None) -> bool:
    """Compare values until the right-hand chain ends."""

    while right is not None:
        if left is None or left.data != right.data:
            return False
        left = left.next
        right = right.next
    return True
